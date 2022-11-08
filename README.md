# Expose Camera Stream Source

_Home Assistant integration to expose an API to retrieve the camera stream source URL._

## Installation

Easiest install is via [HACS](https://hacs.xyz/):

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=felipecrs&repository=hass-expose-camera-stream-source&category=integration)

1. Click the button above, and install this integration via HACS
2. Restart Home Assistant.
3. Add the following to your `configuration.yaml` file:

    ```yaml
    expose_camera_stream_source:
    ```
4. Restart Home Assistant.

## Importing Home Assistant cameras to go2rtc and/or Frigate

This integration can be used to import Home Assistant cameras to [go2rtc](https://github.com/alexxit/go2rtc), including Tuya based cameras that are ONVIF compliant.

You need to be running go2rtc as add-on in Home Assistant. Here's an example of the configuration:

```yaml
# go2rtc.yaml

streams:
  my_camera:
    - echo:bash /config/custom_components/expose_camera_stream_source/get_stream.sh camera.my_camera
```

The `get_stream.sh` script is included by this integration. You can use it to get the stream source URL for any camera in Home Assistant from inside of any add-on.

You can then use the `my_camera` go2rtc stream in Frigate for object detection and/or recording:

```yaml
# frigate.yml

my_camera:
  ffmpeg:
    inputs:
      - path: rtsp://192.168.1.10:8554/my_camera
```
