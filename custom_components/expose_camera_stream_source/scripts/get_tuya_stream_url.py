#!/usr/bin/env python3

import sys
import time
import hmac
import hashlib
import http.client
import json


def get_tuya_stream_url(
    device_id, client_id, client_secret, tuya_base_url, stream_type="RTSP"
):
    encoded_empty_body = (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    t = str(int(time.time() * 1000))

    # Generate sign for token request
    path = "/v1.0/token?grant_type=1"
    sign_string = f"{client_id}{t}GET\n{encoded_empty_body}\n\n{path}"
    sign = (
        hmac.new(client_secret.encode(), sign_string.encode(), hashlib.sha256)
        .hexdigest()
        .upper()
    )

    # Request token
    headers = {
        "sign_method": "HMAC-SHA256",
        "client_id": client_id,
        "t": t,
        "mode": "cors",
        "Content-Type": "application/json",
        "sign": sign,
        "access_token": "",
    }

    conn = http.client.HTTPSConnection(tuya_base_url.replace("https://", ""))
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()
    if response.status != 200:
        raise Exception(f"Failed to get token: {response.status} {response.reason}")
    response_data = response.read()
    response_json = json.loads(response_data)
    if not response_json["success"]:
        raise Exception(
            f"Failed to get token: {response_json.get('msg', response_data)}"
        )
    access_token = response_json["result"]["access_token"]

    # Generate sign for stream URL request
    path = f"/v1.0/devices/{device_id}/stream/actions/allocate"
    body = json.dumps({"type": stream_type})
    encoded_body = hashlib.sha256(body.encode()).hexdigest()
    method = "POST"
    sign_string = f"{client_id}{access_token}{t}{method}\n{encoded_body}\n\n{path}"
    sign = (
        hmac.new(client_secret.encode(), sign_string.encode(), hashlib.sha256)
        .hexdigest()
        .upper()
    )

    # Request stream URL
    headers["access_token"] = access_token
    headers["sign"] = sign
    conn.request("POST", path, body=body, headers=headers)
    response = conn.getresponse()
    if response.status != 200:
        raise Exception(
            f"Failed to get stream URL: {response.status} {response.reason}"
        )
    response_data = response.read()
    response_json = json.loads(response_data)
    if not response_json["success"]:
        raise Exception(f"Failed to get url: {response_json.get('msg', response_data)}")
    url = response_json["result"]["url"]

    print(url)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: python3 get_tuya_stream_url.py <device id> <client id> <client secret> <tuya api base url> [stream type]"
        )
        sys.exit(1)

    device_id = sys.argv[1]
    client_id = sys.argv[2]
    client_secret = sys.argv[3]
    tuya_base_url = sys.argv[4]
    stream_type = sys.argv[5] if len(sys.argv) > 5 else "RTSP"

    get_tuya_stream_url(device_id, client_id, client_secret, tuya_base_url, stream_type)
