FROM debian:stable
MAINTAINER  <coolsidd>
WORKDIR /project
COPY discourse_docker /project
RUN apt-get update
RUN apt-get install docker python3 python3-pip git -y
CMD ["bash"]
