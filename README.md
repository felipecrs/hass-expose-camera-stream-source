<p align="center">
⭐<b>Please star this integration in GitHub if it helps you!</b>⭐
</p>

# Expose Camera Stream Source

_A Home Assistant integration to expose an API for retrieving the camera stream source URL._

It allows to [import](#importing-cameras-from-home-assistant-to-go2rtc-or-frigate) Tuya, Nest and possibly other cameras from Home Assistant to [go2rtc](https://github.com/alexxit/go2rtc) or [Frigate](https://github.com/blakeblackshear/frigate).

Note, however, that **this integration will only work if you are already able to view your camera stream in Home Assistant through [HLS](https://www.home-assistant.io/integrations/stream/)**.

**For cameras that exclusively work through WebRTC** this integration will not help. It is the case for [certain Nest and Tuya cameras](https://github.com/felipecrs/hass-expose-camera-stream-source/issues/5), for example.

Here are some alternatives:

- Nest WebRTC-only cameras are supported natively in go2rtc through the [Nest source](https://github.com/AlexxIT/go2rtc?tab=readme-ov-file#source-nest).
- Tuya WebRTC-only cameras are not supported by Home Assistant, but native support in go2rtc is being worked on by @seydx, and you can [try it already](https://github.com/AlexxIT/go2rtc/issues/315#issuecomment-2905955963).
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

## Importing cameras from Home Assistant to go2rtc or Frigate

This integration can be used to import cameras from Home Assistant to [go2rtc](https://github.com/alexxit/go2rtc) or [Frigate](https://github.com/blakeblackshear/frigate).

> [!IMPORTANT]  
> Before importing to go2rtc, let's make sure a stream source is available for your camera. Simply run this command in the [Terminal](https://github.com/hassio-addons/addon-ssh) or [VS Code add-on](https://github.com/hassio-addons/addon-vscode):
>
> ```console
> curl -fsSL http://supervisor/core/api/camera_stream_source/camera.my_camera -H "Authorization: Bearer ${SUPERVISOR_TOKEN}"
> ```
>
> **Replacing** `camera.my_camera` with your camera entity ID.
> 
> If you have **no access to add-ons**, you will need to replace `${SUPERVISOR_TOKEN}` with your Home Assistant long-lived access token and `http://supervisor/core` with the IP address or URL of your Home Assistant. Read below for more details. If you are on Windows, you can run that command in PowerShell by changing `curl` to `curl.exe`.
>
> After running it, it should output an RTSP or HTTP URL.
>
> **If it did not**, sorry but stream source is not available for your camera.
> 
> **If it did, copy this URL and try to play it in [VLC](https://www.videolan.org/vlc/)**.
> 
> Be quick though, some URLs expire after a few seconds if no connection is made. You can generate a new one by running the command again.
>
> **If it does not play in VLC**, it will not play in go2rtc or Frigate either. Sorry.

Here is an example of how to do it in your go2rtc configuration file:

```yaml
# go2rtc.yaml

streams:
  my_camera:
    - 'echo:curl -fsSL http://supervisor/core/api/camera_stream_source/camera.my_camera -H "Authorization: Bearer ${SUPERVISOR_TOKEN}"'
```

Or, **if you are using Frigate**, here is how you can do the same in your Frigate configuration file:

```yaml
# config.yml

go2rtc:
  streams:
    my_camera:
      - 'echo:curl -fsSL http://supervisor/core/api/camera_stream_source/camera.my_camera -H "Authorization: Bearer ${SUPERVISOR_TOKEN}"'

cameras:
  my_camera:
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/my_camera?video
          input_args: preset-rtsp-restream-low-latency
          roles:
            - detect
```

**Replacing** `camera.my_camera` with your Home Assistant camera entity ID.

Note that **you do not need to replace `${SUPERVISOR_TOKEN}` or make any further changes** if you are running go2rtc through the [WebRTC integration](https://github.com/AlexxIT/WebRTC), [go2rtc add-on](https://github.com/AlexxIT/go2rtc#go2rtc-home-assistant-add-on), or [Frigate add-on](https://docs.frigate.video/frigate/installation#home-assistant-addon).

**Otherwise**, you need to replace `${SUPERVISOR_TOKEN}` with your Home Assistant long-lived access token. To generate one:

1. Go to your Home Assistant profile page: [![Open your Home Assistant instance and show your Home Assistant user's profile.](https://my.home-assistant.io/badges/profile.svg)](https://my.home-assistant.io/redirect/profile/)
2. Scroll down to _Long-Lived Access Token_, and click in _Create Token_.
3. Give it a name, like `go2rtc` and press _Ok_.

**Additionally**, you need to replace `http://supervisor/core` with the IP address or URL of your Home Assistant instance. Example:

```yaml
streams:
  my_camera:
    - 'echo:curl -fsSL http://192.168.1.10:8123/api/camera_stream_source/camera.my_camera -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4ZDljNzU4NjM2OGQ0NzI0YmJhZjVlODBmZDdjODMwMiIsImlhdCI6MTc0ODA0OTc4OSwiZXhwIjoyMDYzNDA5Nzg5fQ.RmV0VN43byRA-azB8N7jUn2j7W9LRppJlzQ1aOQcnFc"'
```

## Bonus: importing Tuya cameras to go2rtc without Home Assistant

> [!NOTE]
> This is obsolete since native support for Tuya cameras in go2rtc is being worked on by @seydx, and you can [try it already](https://github.com/AlexxIT/go2rtc/issues/315#issuecomment-2905955963).

<details>
<summary>Click to here to show anyway</summary>

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

</details>
