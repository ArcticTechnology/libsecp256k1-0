FROM ubuntu:20.04
COPY . /libsecp
WORKDIR /libsecp

RUN bash ./require.sh && rm -rf /var/lib/apt/list/*
CMD bash ./compiler.sh