"""
Custom integration to integrate expose_camera_stream_source with Home Assistant.

For more details about this integration, please refer to
https://github.com/felipecrs/expose_camera_stream_source
"""

import logging
from typing import Final
from homeassistant.components.camera import Camera, CameraView
from homeassistant.components.camera.const import DOMAIN as CAMERA_DOMAIN
from homeassistant.helpers.entity_component import EntityComponent
from aiohttp import web

DOMAIN: Final = "expose_camera_stream_source"
_LOGGER: logging.Logger = logging.getLogger(__package__)


def setup(hass, _config) -> bool:
    """Set up the integration."""
    component: EntityComponent[Camera] = hass.data[CAMERA_DOMAIN]

    if component is None:
        _LOGGER.error("Camera integration not initialized")
        return False

    hass.http.register_view(CameraStreamSourceView(component))

    # Return boolean to indicate that initialization was successful.
    return True


class CameraStreamSourceView(CameraView):
    """Camera view to get stream source."""

    url = "/api/camera_stream_source/{entity_id}"
    name = "api:camera:stream_source"
    requires_auth = True

    async def handle(self, request: web.Request, camera: Camera) -> web.Response:
        """Return the stream source."""
        stream_source = await camera.stream_source()
        if stream_source is None:
            raise web.HTTPNotFound()
        return web.Response(text=stream_source)
