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

## Importing Home Assistant cameras to go2rtc and/or Frigate (Supervised Installation)

This integration can be used to import Home Assistant cameras to [go2rtc](https://github.com/alexxit/go2rtc), including Tuya and Nest based cameras that are **not** ONVIF compliant.

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

Where `192.168.1.10` is your Home Assistant internal IP address (which is where the go2rtc add-on listens on).

## Importing Home Assistant cameras to go2rtc and/or Frigate (Docker Installation)

This integration can be used to import Home Assistant cameras to [go2rtc](https://github.com/alexxit/go2rtc), including Tuya and Nest based cameras that are **not** ONVIF compliant.

You need to be running go2rtc and home assistant as docker containers.

Add the following to the go2rtc docker-compose.yml

```yaml

volumes:
  - "~/go2rtc.yaml:/config/go2rtc.yaml"
  - "~/get_stream.sh:/config/get_stream.sh"
```
Create a file named get_stream.sh in the same folder with the following text:

```yaml

#!/usr/bin/env bash

set -eu

ACCESS_TOKEN="#long lived access token generated from home assistant#"
entity_id="${1}"

exec curl -fsSL -H "Authorization: Bearer ${ACCESS_TOKEN}" "http://192.168.1.10:8123/api/camera_stream_source/${entity_id}"

```
The following is an example go2rtc configuration:
```yaml
# go2rtc.yaml

streams:
  my_camera:
    - echo:bash /config/get_stream.sh camera.my_camera
```

You can then use the `my_camera` go2rtc stream in Frigate for object detection and/or recording:

```yaml
# frigate.yml

my_camera:
  ffmpeg:
    inputs:
      - path: rtsp://192.168.1.10:8554/my_camera
```

Where `192.168.1.10` is your Home Assistant / go2rtc internal IP address.


