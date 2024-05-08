from typing import Any, Dict, Optional
from collections.abc import Callable

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity

from homeassistant.const import (
    CONF_API_KEY, 
    CONF_NAME, 
    )

from .const import DOMAIN
from .coordinator import PlexDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Callable,
) -> None:
    coordinator: PlexDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([PlexRecentlyAddedSensor(coordinator, config_entry)], update_before_add=True)



class PlexRecentlyAddedSensor(CoordinatorEntity[PlexDataCoordinator], SensorEntity):
    def __init__(self, coordinator: PlexDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME].capitalize() + " " if len(config_entry.data[CONF_NAME]) > 0 else ""}Plex Recently Added'
        self._api_key = config_entry.data[CONF_API_KEY]

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{self._api_key}_Plex_Recently_Added'

    @property
    def state(self) -> Optional[str]:
        """Return the value of the sensor."""
        return "Online" if 'online' in self._coordinator.data and self._coordinator.data['online'] else "Offline"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self._coordinator.data['data']