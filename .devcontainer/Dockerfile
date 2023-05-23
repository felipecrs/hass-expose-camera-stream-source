FROM ghcr.io/ludeeus/devcontainer/integration:stable

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir -p /config && chown -R vscode:vscode /config

USER vscode

RUN container install

RUN pip install --upgrade pip

RUN --mount=type=bind,source=requirements_dev.txt,target=/tmp/requirements_dev.txt \
     pip install -r /tmp/requirements_dev.txt
