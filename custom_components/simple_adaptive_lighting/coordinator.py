"""Coordinator for adaptive lighting values and apply logic."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.light import ATTR_BRIGHTNESS_PCT
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_ENABLED,
    CONF_MAX_BRIGHTNESS,
    CONF_MAX_KELVIN,
    CONF_MIN_BRIGHTNESS,
    CONF_MIN_KELVIN,
    CONF_TARGET_LIGHTS,
    DEFAULT_ENABLED,
    DEFAULT_MAX_BRIGHTNESS,
    DEFAULT_MAX_KELVIN,
    DEFAULT_MIN_BRIGHTNESS,
    DEFAULT_MIN_KELVIN,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class SimpleAdaptiveCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Maintain and refresh computed adaptive values."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.entry = entry
        self._enabled = bool(self._get_value(CONF_ENABLED, DEFAULT_ENABLED))

    @property
    def enabled(self) -> bool:
        return self._enabled

    async def async_set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        snapshot = self._build_snapshot()
        if self._enabled:
            snapshot["last_apply"] = await self._async_apply_to_lights(snapshot)
        self.async_set_updated_data(snapshot)

    async def async_apply_now(self) -> None:
        snapshot = self._build_snapshot()
        if self._enabled:
            snapshot["last_apply"] = await self._async_apply_to_lights(snapshot)
        self.async_set_updated_data(snapshot)

    async def _async_update_data(self) -> dict[str, Any]:
        snapshot = self._build_snapshot()
        if self._enabled:
            snapshot["last_apply"] = await self._async_apply_to_lights(snapshot)
        return snapshot

    def _get_value(self, key: str, default: Any) -> Any:
        return self.entry.options.get(key, self.entry.data.get(key, default))

    @staticmethod
    def _normalize_lights(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return []

    def _build_snapshot(self) -> dict[str, Any]:
        min_brightness = int(self._get_value(CONF_MIN_BRIGHTNESS, DEFAULT_MIN_BRIGHTNESS))
        max_brightness = int(self._get_value(CONF_MAX_BRIGHTNESS, DEFAULT_MAX_BRIGHTNESS))
        min_kelvin = int(self._get_value(CONF_MIN_KELVIN, DEFAULT_MIN_KELVIN))
        max_kelvin = int(self._get_value(CONF_MAX_KELVIN, DEFAULT_MAX_KELVIN))
        target_lights = self._normalize_lights(self._get_value(CONF_TARGET_LIGHTS, []))

        sun_state = self.hass.states.get("sun.sun")
        sun_elevation = float(sun_state.attributes.get("elevation", 0.0)) if sun_state else 0.0

        normalized = max(0.0, min(1.0, (sun_elevation + 6.0) / 51.0))
        brightness_pct = round(min_brightness + (max_brightness - min_brightness) * normalized)
        color_temp_kelvin = round(min_kelvin + (max_kelvin - min_kelvin) * normalized)

        if normalized <= 0.15:
            mode = "night"
        elif normalized >= 0.85:
            mode = "day"
        else:
            mode = "transition"

        return {
            "enabled": self._enabled,
            "mode": mode,
            "sun_elevation": sun_elevation,
            "brightness_pct": brightness_pct,
            "color_temp_kelvin": color_temp_kelvin,
            "target_lights": target_lights,
            "adjusted_lights": [],
            "last_apply": "idle",
        }

    async def _async_apply_to_lights(self, snapshot: dict[str, Any]) -> str:
        target_lights: list[str] = snapshot.get("target_lights", [])
        if not target_lights:
            return "skipped_no_targets"

        active_targets = [
            entity_id
            for entity_id in target_lights
            if (state := self.hass.states.get(entity_id)) and state.state == "on"
        ]
        snapshot["adjusted_lights"] = active_targets
        if not active_targets:
            return "skipped_all_off"

        service_data = {
            ATTR_ENTITY_ID: active_targets,
            ATTR_BRIGHTNESS_PCT: snapshot["brightness_pct"],
            "kelvin": snapshot["color_temp_kelvin"],
            "transition": 1,
        }
        await self.hass.services.async_call("light", "turn_on", service_data, blocking=True)
        return "applied"
