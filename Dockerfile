
FROM python:3.10.9-slim

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

RUN apt-get update && apt install fonts-dejavu-core rsync git jq moreutils -y && apt-get clean && apt-get install ffmpeg libsm6 libxext6 -y

RUN --mount=type=cache,target=/root/.cache/pip \
  git clone https://github.com/hhdem/stable-diffusion-webui && \
  cd stable-diffusion-webui
  # pip install -r requirements_versions.txt

# copy folder models/Stable-diffusion to /stable-diffusion-webui/models/Stable-diffusion
# COPY ./models/Stable-diffusion /stable-diffusion-webui/models/Stable-diffusion
# RUN ln -s ./models/Stable-diffusion/Dungeons_N_Waifu's_New_Version_2.2 /proj/suchka/image-generation/stable-diffusion-webui/models/Stable-diffusion/Dungeons_N_Waifu's_New_Version_2.2


ENV ROOT=/stable-diffusion-webui

WORKDIR ${ROOT}
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NVIDIA_VISIBLE_DEVICES=all
ENV CLI_ARGS=""
EXPOSE 5000
# ENTRYPOINT ["/docker/entrypoint.sh"]
# CMD python -u webapi.py --listen --port 5000 ${CLI_ARGS}
CMD CUDA_VISIBLE_DEVICES=1 ./webui.sh 

# sudo docker build -t sdapi . --no-cache
# sudo docker run --name sdapi --restart unless-stopped --gpus all -itd -p 10.0.0.1:5000:5000 sdapi
# sudo docker container ls -a
# sudo docker logs -f sdapi
# sudo docker container stop sdapi
# sudo docker container rm sdapi