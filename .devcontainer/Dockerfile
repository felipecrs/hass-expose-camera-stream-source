FROM ghcr.io/ludeeus/devcontainer/integration:stable

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir -p /config && chown -R vscode:vscode /config

USER vscode

RUN container install

# Currently failing due to gcc
# RUN --mount=type=bind,source=requirements_dev.txt,target=/tmp/requirements_dev.txt \
#     --mount=type=bind,source=requirements_test.txt,target=/tmp/requirements_test.txt \
#     pip install -r /tmp/requirements_dev.txt -r /tmp/requirements_test.txt
