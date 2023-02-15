<p align="center">
⭐<b>Please star this integration in GitHub if it helps you!</b>⭐
</p>

# Expose Camera Stream Source

_Home Assistant integration to expose an API to retrieve the camera stream source URL._

For example, it allows you to [import](#importing-cameras-from-home-assistant-to-go2rtc-and-frigate) Tuya, Nest and possibly other cameras to go2rtc and Frigate.

Note, however, that this will only work if you are already able to view your camera stream in Home Assistant using [HLS](https://www.home-assistant.io/integrations/stream/). For cameras that exclusively only work via WebRTC (through the [RTSPToWebRTC Home Assistant integration](https://www.home-assistant.io/integrations/rtsp_to_webrtc/)), this method will not help. It is the case for [some specific Nest and Tuya cameras](https://github.com/felipecrs/hass-expose-camera-stream-source/issues/5), for example. If that is your case, I suggest you create an [issue in go2rtc](https://github.com/AlexxIT/go2rtc/issues) as it is possible that go2rtc can be improved to support importing your camera stream directly, without a intermediary project like this.

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

## Importing cameras from Home Assistant to go2rtc

This integration can be used to import cameras from Home Assistant to [go2rtc](https://github.com/alexxit/go2rtc) and [Frigate](https://github.com/blakeblackshear/frigate), **including cameras which does not expose an RTSP feed by default, like some Tuya and Nest cameras**.

## When go2rtc is installed as an add-on

<details>
  <summary>Click here to show</summary>

If you are running go2rtc as an add-on in Home Assistant, the process is a little simpler (if not, check [here](#when-go2rtc-is-running-via-docker)). Here's an example of the go2rtc configuration:

```yaml
# go2rtc.yaml

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

When go2rtc is not running as a Home Assistant add-on, you need to prepare a script and mount it to the go2rtc container. Here is how the script should look like:

```bash
#!/usr/bin/env bash

set -eu

HA_TOKEN="${HA_TOKEN:?"HA_TOKEN is not set, make sure to have this environment variable set with your Home Assisant long-lived token."}"
entity_id="${1}"

exec curl -fsSL -H "Authorization: Bearer ${HA_TOKEN}" "http://192.168.1.10:8123/api/camera_stream_source/${entity_id}"
```

Where `192.168.1.10` is your Home Assistant's IP address.

Paste the content above in a file named `get_ha_stream.sh`. For this example, we will store the file at your home folder (`~/get_ha_stream.sh`). Then give it execution permission with the following command:

```console
chmod +x ~/get_ha_stream.sh
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
      - "~/go2rtc.yaml:/config/go2rtc.yaml"
+     - "~/get_ha_stream.sh:/config/get_ha_stream.sh"
+   environment:
+     HA_TOKEN: paste-your-token-here
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

When go2rtc is not running as a Home Assistant add-on neither via an add-on, but as part of the WebRTC integration, you need to prepare a script in your `/config` folder.

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

Paste the content above in a file named `get_ha_stream.sh`, and place it in Home Assistant's `/config` folder. Do not forget to put your long-lived access token in the script's placeholder.

Then, give it execution permission with the following command:

```console
chmod +x ~/get_ha_stream.sh
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
