
FROM python:3.10.9-slim

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

RUN apt-get update && apt install fonts-dejavu-core rsync git jq moreutils -y && apt-get clean


RUN --mount=type=cache,target=/root/.cache/pip \
  git clone https://github.com/hhdem/stable-diffusion-webui && \
  cd stable-diffusion-webui && \
  pip install -r requirements_versions.txt

ENV ROOT=/stable-diffusion-webui

WORKDIR ${ROOT}
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NVIDIA_VISIBLE_DEVICES=all
ENV CLI_ARGS=""
EXPOSE 5000
# ENTRYPOINT ["/docker/entrypoint.sh"]
# CMD python -u webapi.py --listen --port 5000 ${CLI_ARGS}
CMD ./webui.sh
