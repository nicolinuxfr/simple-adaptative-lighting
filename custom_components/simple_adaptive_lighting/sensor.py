"""Sensor platform for Simple Adaptive Lighting."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_NAME, DEFAULT_NAME, DOMAIN
from .coordinator import SimpleAdaptiveCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SimpleAdaptiveCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SimpleAdaptiveStatusSensor(coordinator, entry)])


class SimpleAdaptiveStatusSensor(CoordinatorEntity[SimpleAdaptiveCoordinator], SensorEntity):
    """Expose current adaptive profile with rich attributes."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:theme-light-dark"

    def __init__(self, coordinator: SimpleAdaptiveCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status_sensor"
        self._attr_name = f"{entry.data.get(CONF_NAME, DEFAULT_NAME)} status"

    @property
    def native_value(self) -> str:
        return self.coordinator.data.get("mode", "unknown")

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data or {}
        return {
            "enabled": data.get("enabled"),
            "sun_elevation": data.get("sun_elevation"),
            "brightness_pct": data.get("brightness_pct"),
            "brightness_unit": PERCENTAGE,
            "color_temp_kelvin": data.get("color_temp_kelvin"),
            "target_lights": data.get("target_lights", []),
            "adjusted_lights": data.get("adjusted_lights", []),
            "last_apply": data.get("last_apply", "idle"),
        }
