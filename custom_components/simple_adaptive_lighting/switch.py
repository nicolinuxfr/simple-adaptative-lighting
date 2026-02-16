"""Switch platform for Simple Adaptive Lighting."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up switch entity from config entry."""
    coordinator: SimpleAdaptiveCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SimpleAdaptiveMasterSwitch(coordinator, entry)])


class SimpleAdaptiveMasterSwitch(CoordinatorEntity[SimpleAdaptiveCoordinator], SwitchEntity):
    """Main runtime toggle for the adaptive controller."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: SimpleAdaptiveCoordinator, entry: ConfigEntry) -> None:
        """Initialize switch."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_master_switch"
        self._attr_name = entry.data.get(CONF_NAME, DEFAULT_NAME)

    @property
    def is_on(self) -> bool:
        """Return true if controller is enabled."""
        return self.coordinator.enabled

    async def async_turn_on(self, **kwargs) -> None:
        """Enable controller."""
        await self.coordinator.async_set_enabled(True)
        await self.coordinator.async_apply_now()

    async def async_turn_off(self, **kwargs) -> None:
        """Disable controller."""
        await self.coordinator.async_set_enabled(False)
