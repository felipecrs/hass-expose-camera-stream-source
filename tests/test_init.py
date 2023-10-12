"""Test expose_camera_stream_source."""


from http import HTTPStatus
from unittest.mock import patch


async def test_camera_stream_source_api(hass, hass_client):
    """Test camera stream source HTTP API."""

    # TODO: fix AttributeError: 'NoneType' object has no attribute 'app'

    client = await hass_client()

    with patch(
        "homeassistant.components.demo.camera.DemoCamera.stream_source",
        return_value="rtsp://test.url",
    ):
        response = await client.get("/api/camera_stream_source/camera.demo_camera")
        assert response.status == HTTPStatus.OK
        assert await response.text() == "rtsp://test.url"

    with patch(
        "homeassistant.components.demo.camera.DemoCamera.stream_source",
        return_value=None,
    ):
        response = await client.get("/api/camera_stream_source/camera.demo_camera")
        assert response.status == HTTPStatus.NOT_FOUND
