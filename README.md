<p align="center">
⭐<b>Please star this integration in GitHub if it helps you!</b>⭐
</p>

# Expose Camera Stream Source

_Home Assistant integration to expose an API to retrieve the camera stream source URL._

For example, it allows you to [import](#importing-cameras-from-home-assistant-to-go2rtc-and-frigate) Tuya, Nest and possibly other cameras to go2rtc and Frigate.

Note, however, that **this integration will only work if you are already able to view your camera stream in Home Assistant using [HLS](https://www.home-assistant.io/integrations/stream/)**.

**For cameras that exclusively only work via WebRTC** (through the [RTSPToWebRTC Home Assistant integration](https://www.home-assistant.io/integrations/rtsp_to_webrtc/)), this method will not help. It is the case for [some specific Nest and Tuya cameras](https://github.com/felipecrs/hass-expose-camera-stream-source/issues/5), for example.

If that is your case:

- Nest WebRTC-native cameras are supported natively in go2rtc, see [here](https://github.com/AlexxIT/go2rtc?tab=readme-ov-file#source-nest) for more details.
- Tuya WebRTC-native cameras are not supported either by Home Assistant or go2rtc. If you need it, you can express your interest in:
  - https://github.com/AlexxIT/go2rtc/issues/315 (being worked on by @seydx, but you can [try it already](https://github.com/AlexxIT/go2rtc/issues/315#issuecomment-2905955963))
- Cameras that only support still images can be added to go2rtc through [this method](https://github.com/felipecrs/hass-expose-camera-stream-source/issues/53).

## Installation

Easiest install is via [HACS](https://hacs.xyz/):

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=felipecrs&repository=hass-expose-camera-stream-source&category=integration)

1. Click the button above, and install this integration via HACS. Do **not** try to configure it yet.
2. Restart Home Assistant.
3. Add the following to your `configuration.yaml` file:

   ```yaml
   expose_camera_stream_source:
   ```

4. Restart Home Assistant again.

Now the integration should be active.

## Importing cameras from Home Assistant to go2rtc and Frigate

This integration can be used to import cameras from Home Assistant to [go2rtc](https://github.com/alexxit/go2rtc) and [Frigate](https://github.com/blakeblackshear/frigate), **including cameras which does not expose a RTSP feed by default, like some Tuya and Nest cameras**.

### When go2rtc is running within the Frigate add-on

<details>
  <summary>Click here to show</summary>

If you are running go2rtc within the Frigate add-on, you can use the following configuration:

> [!IMPORTANT]
> If using Frigate 0.16 Beta or newer, change the paths below from `/config/` to `/homeassistant/`.

```yaml
# /config/frigate.yaml

go2rtc:
  streams:
    my_camera:
      - echo:bash /config/custom_components/expose_camera_stream_source/get_stream.sh camera.my_camera

cameras:
  my_camera:
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/my_camera?video
          input_args: preset-rtsp-restream-low-latency
          roles:
            - detect
```

Where `camera.my_camera` is the Home Assistant entity ID for the camera that you want to import the stream from.

</details>

### When go2rtc is running within Frigate via docker

<details>
  <summary>Click here to show</summary>

When go2rtc is running within Frigate via docker, you need to prepare a Bash script to mount it to the Frigate container. Here is how the script should look like:

```bash
#!/usr/bin/env bash

set -eu

HA_TOKEN="${HA_TOKEN:?"HA_TOKEN is not set, make sure to have this environment variable set with your Home Assisant long-lived token."}"
entity_id="${1}"

exec curl -fsSL -H "Authorization: Bearer ${HA_TOKEN}" "http://192.168.1.10:8123/api/camera_stream_source/${entity_id}"
```

Where `192.168.1.10` is your Home Assistant's IP address.

Paste the content above in a file named `get_ha_stream.sh`, and place it in your Frigate's `config` directory, beside your `frigate.yaml`. Then, give it execution permission with the following command:

```console
chmod +x /path/to/your/config/get_ha_stream.sh
```

You will also need a long-lived access token from Home Assistant. To generate one:

1. Go to your Home Assistant profile page: [![Open your Home Assistant instance and show your Home Assistant user's profile.](https://my.home-assistant.io/badges/profile.svg)](https://my.home-assistant.io/redirect/profile/)
2. Scroll down to _Long-Lived Access Token_, and click in _Create Token_.
3. Give it a name, like `go2rtc` and press _Ok_.
4. Copy your generated access token and save it. We will need it soon.

Now, you need to make sure your token is added as the `HA_TOKEN` environment variable. If you use Docker Compose, you just need to add something like the below in your configuration:

```diff
# docker-compose.yaml

services:
  frigate:
    image: ghcr.io/blakeblackshear/frigate:stable
    volumes:
      - /path/to/your/config:/config
+   environment:
+     HA_TOKEN: paste-your-long-lived-access-token-here
```

And here is an example of the Frigate configuration:

```yaml
# frigate.yaml

go2rtc:
  streams:
    my_camera:
      - echo:/config/get_ha_stream.sh camera.my_camera

cameras:
  my_camera:
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/my_camera?video
          input_args: preset-rtsp-restream-low-latency
          roles:
            - detect
```

Where `camera.my_camera` is the Home Assistant entity ID for the camera that you want to import the stream from.

</details>

### When go2rtc is installed as an add-on

<details>
  <summary>Click here to show</summary>

If you are running go2rtc as an add-on in Home Assistant, the process is a little simpler (if not, check [here](#when-go2rtc-is-running-via-docker)). Here's an example of the go2rtc configuration:

```yaml
# /config/go2rtc.yaml

streams:
  my_camera:
    - echo:bash /config/custom_components/expose_camera_stream_source/get_stream.sh camera.my_camera
```

Where `camera.my_camera` is the Home Assistant entity ID for the camera that you want to import the stream from.

The `get_stream.sh` script is included by this integration. You can use it to get the stream source URL for any camera in Home Assistant from inside of any add-on.

Then, you can consume your go2rtc's `my_camera` stream in other applications like Frigate or other NVRs:

- `rtsp://192.168.1.10:8554/my_camera`

Where `192.168.1.10` is the IP which you can access the go2rtc interfaces (for add-on users it's the same IP as your Home Assistant).

> **Tip:** Try to first play the RTSP link above in VLC before adding to Frigate or other NVRs, to ensure everything is working up to this point.

</details>

### When go2rtc is running via docker

<details>
  <summary>Click here to show</summary>

When go2rtc is not running as a Home Assistant add-on, you need to prepare a Bash script and mount it to the go2rtc container. Here is how the script should look like:

```bash
#!/usr/bin/env bash

set -eu

HA_TOKEN="${HA_TOKEN:?"HA_TOKEN is not set, make sure to have this environment variable set with your Home Assisant long-lived token."}"
entity_id="${1}"

exec curl -fsSL -H "Authorization: Bearer ${HA_TOKEN}" "http://192.168.1.10:8123/api/camera_stream_source/${entity_id}"
```

Where `192.168.1.10` is your Home Assistant's IP address.

Paste the content above in a file named `get_ha_stream.sh`, and place it beside your `go2rtc.yaml`. Then, give it execution permission with the following command:

```console
chmod +x /path/to/your/get_ha_stream.sh
```

You will also need a long-lived access token from Home Assistant. To generate one:

1. Go to your Home Assistant profile page: [![Open your Home Assistant instance and show your Home Assistant user's profile.](https://my.home-assistant.io/badges/profile.svg)](https://my.home-assistant.io/redirect/profile/)
2. Scroll down to _Long-Lived Access Token_, and click in _Create Token_.
3. Give it a name, like `go2rtc` and press _Ok_.
4. Copy your generated access token and save it. We will need it soon.

Now, you need to make sure the script you created earlier is mounted in the go2rtc container, and your token is added as the `HA_TOKEN` environment variable. If you use Docker Compose, you just need to add something like the below in your configuration:

```diff
# docker-compose.yaml

services:
  go2rtc:
    image: alexxit/go2rtc
    network_mode: host
    restart: always
    volumes:
      - /path/to/your/go2rtc.yaml:/config/go2rtc.yaml
+     - /path/to/your/get_ha_stream.sh:/config/get_ha_stream.sh
+   environment:
+     HA_TOKEN: paste-your-long-lived-access-token-here
```

And here is an example of the go2rtc configuration:

```yaml
# go2rtc.yaml

streams:
  my_camera:
    - echo:/config/get_ha_stream.sh camera.my_camera
```

Where `camera.my_camera` is the Home Assistant entity ID for the camera that you want to import the stream from.

Then, you can consume your go2rtc's `my_camera` stream in other applications like Frigate or other NVRs:

- `rtsp://192.168.1.10:8554/my_camera`

Where `192.168.1.10` is the IP which you can access the go2rtc interfaces (for add-on users it's the same IP as your Home Assistant).

> **Tip:** Try to first play the RTSP link above in VLC before adding to Frigate or other NVRs, to ensure everything is working up to this point.

</details>

### When go2rtc is running via the WebRTC integration

<details>
  <summary>Click here to show</summary>

When go2rtc is not running as a Home Assistant add-on neither via an add-on, but as part of the WebRTC integration, you need to prepare a Bash script in your `/config` directory.

First, you will need a long-lived access token from Home Assistant. To generate one:

1. Go to your Home Assistant profile page: [![Open your Home Assistant instance and show your Home Assistant user's profile.](https://my.home-assistant.io/badges/profile.svg)](https://my.home-assistant.io/redirect/profile/)
2. Scroll down to _Long-Lived Access Token_, and click in _Create Token_.
3. Give it a name, like `go2rtc` and press _Ok_.
4. Copy your generated access token and save it. We will need it soon.

Then, you can create the script. Here is how the script should look like:

```bash
#!/usr/bin/env bash

set -eu

HA_TOKEN="<put your long-lived access token here>"
entity_id="${1}"

exec curl -fsSL -H "Authorization: Bearer ${HA_TOKEN}" "http://127.0.0.1:8123/api/camera_stream_source/${entity_id}"
```

Paste the content above in a file named `get_ha_stream.sh`, and place it in Home Assistant's `/config` directory. Do not forget to put your long-lived access token in the script's placeholder.

Then, give it execution permission with the following command:

```console
chmod +x /config/get_ha_stream.sh
```

And here is an example of the go2rtc configuration:

```yaml
# go2rtc.yaml

streams:
  my_camera:
    - echo:/config/get_ha_stream.sh camera.my_camera
```

Where `camera.my_camera` is the Home Assistant entity ID for the camera that you want to import the stream from.

Then, you can consume your go2rtc's `my_camera` stream in other applications like Frigate or other NVRs:

- `rtsp://192.168.1.10:8554/my_camera`

Where `192.168.1.10` is the IP which you can access the go2rtc interfaces (for add-on users it's the same IP as your Home Assistant).

> **Tip:** Try to first play the RTSP link above in VLC before adding to Frigate or other NVRs, to ensure everything is working up to this point.

</details>

## Bonus: importing Tuya cameras to go2rtc without Home Assistant

This repository also provides a script that is able to operate without Home Assistant, allowing you to import Tuya cameras to go2rtc without the need of Home Assistant.

It also allows you to select between _RTSP_ and _HLS_ streams, which is not possible with the Home Assistant integration (which is always _RTSP_).

Script: [get_tuya_stream_url.py](./custom_components/expose_camera_stream_source/scripts/get_tuya_stream_url.py)

Usage: `Usage: python3 get_tuya_stream_url.py <device id> <client id> <client secret> <tuya api base url> [stream type]`

Example:

```console
$ python3 get_tuya_stream_url.py <device id> <client id> <client secret> https://openapi.tuyaus.com RTSP
rtsps://ebf0345643b3de54904xgqs:OIB97AMHY7LG8TW6@aws-tractor2.tuyaus.com:443/v1/proxy/echo_show/d91271489ccd46331be3e4f3fa65b5a8893c0799bef1485ba

$ python3 get_tuya_stream_url.py <device id> <client id> <client secret> https://openapi.tuyaus.com HLS
https://aws-tractor2.tuyaus.com:8033/hls/348ceb3cbe1c4429b849c546c924af9bb5f053cd858ae65e0e3bf.m3u8
```

And it can be integrated with go2rtc in the same way as the Home Assistant integration:

```yaml
# go2rtc.yaml

streams:
  my_camera:
    - echo:python3 /path/to/your/get_tuya_stream_url.py <device id> <client id> <client secret> https://openapi.tuyaus.com RTSP
```
