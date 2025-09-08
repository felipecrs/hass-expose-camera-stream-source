import logging
from homeassistant.components.camera import Camera, CameraView
from homeassistant.components.camera.const import DOMAIN as CAMERA_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.config_entries import ConfigEntry
from aiohttp import web

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    component: EntityComponent[Camera] = hass.data[CAMERA_DOMAIN]

    if component is None:
        _LOGGER.error("Camera integration not initialized")
        return False

    hass.http.register_view(CameraStreamSourceView(component))

    # Return boolean to indicate that initialization was successful.
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # This integration doesn't create any entities, so no cleanup needed
    return True


class CameraStreamSourceView(CameraView):
    url = "/api/camera_stream_source/{entity_id}"
    name = "api:camera:stream_source"
    requires_auth = True

    async def handle(self, request: web.Request, camera: Camera) -> web.Response:
        stream_source = await camera.stream_source()
        if stream_source is None:
            raise web.HTTPNotFound()
        return web.Response(text=stream_source)
