"""Config flow for Simple Adaptive Lighting."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import selector

from .const import (
    CONF_ENABLED,
    CONF_MAX_BRIGHTNESS,
    CONF_MAX_KELVIN,
    CONF_MIN_BRIGHTNESS,
    CONF_MIN_KELVIN,
    CONF_NAME,
    CONF_TARGET_LIGHTS,
    DEFAULT_ENABLED,
    DEFAULT_MAX_BRIGHTNESS,
    DEFAULT_MAX_KELVIN,
    DEFAULT_MIN_BRIGHTNESS,
    DEFAULT_MIN_KELVIN,
    DEFAULT_NAME,
    DOMAIN,
)


def _normalize_user_input(user_input: dict[str, Any]) -> dict[str, Any]:
    parsed = dict(user_input)
    raw_lights = parsed.get(CONF_TARGET_LIGHTS, [])
    if isinstance(raw_lights, str):
        parsed[CONF_TARGET_LIGHTS] = [item.strip() for item in raw_lights.split(",") if item.strip()]
    elif isinstance(raw_lights, list):
        parsed[CONF_TARGET_LIGHTS] = [str(item).strip() for item in raw_lights if str(item).strip()]
    else:
        parsed[CONF_TARGET_LIGHTS] = []
    return parsed


def _schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_NAME, default=defaults.get(CONF_NAME, DEFAULT_NAME)): str,
            vol.Optional(
                CONF_TARGET_LIGHTS,
                default=defaults.get(CONF_TARGET_LIGHTS, []),
            ): selector(
                {
                    "entity": {
                        "multiple": True,
                        "filter": [{"domain": "light"}],
                    }
                }
            ),
            vol.Required(
                CONF_MIN_BRIGHTNESS,
                default=defaults.get(CONF_MIN_BRIGHTNESS, DEFAULT_MIN_BRIGHTNESS),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
            vol.Required(
                CONF_MAX_BRIGHTNESS,
                default=defaults.get(CONF_MAX_BRIGHTNESS, DEFAULT_MAX_BRIGHTNESS),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=100)),
            vol.Required(
                CONF_MIN_KELVIN,
                default=defaults.get(CONF_MIN_KELVIN, DEFAULT_MIN_KELVIN),
            ): vol.All(vol.Coerce(int), vol.Range(min=1500, max=10000)),
            vol.Required(
                CONF_MAX_KELVIN,
                default=defaults.get(CONF_MAX_KELVIN, DEFAULT_MAX_KELVIN),
            ): vol.All(vol.Coerce(int), vol.Range(min=1500, max=10000)),
            vol.Required(
                CONF_ENABLED,
                default=defaults.get(CONF_ENABLED, DEFAULT_ENABLED),
            ): bool,
        }
    )


class SimpleAdaptiveLightingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            parsed = _normalize_user_input(user_input)
            return self.async_create_entry(title=parsed[CONF_NAME], data=parsed)

        return self.async_show_form(step_id="user", data_schema=_schema({}))

    @staticmethod
    def async_get_options_flow(config_entry):
        return SimpleAdaptiveLightingOptionsFlow(config_entry)


class SimpleAdaptiveLightingOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            parsed = _normalize_user_input(user_input)
            return self.async_create_entry(title="", data=parsed)

        defaults = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_schema(defaults))
