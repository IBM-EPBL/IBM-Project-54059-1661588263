FROM ubuntu:latest
RUN  apt-get update
RUN  apt-get install -y python3 python3-pip
ARG requirements
ARG workspace
RUN mkdir ${workspace}
COPY . /${workspace}
RUN pip3 install -r /${workspace}/${requirements}
WORKDIR ${workspace}
ENTRYPOINT [ "flask" , "run" ]