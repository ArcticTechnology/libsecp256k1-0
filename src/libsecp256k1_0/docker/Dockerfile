FROM ubuntu:20.04
COPY . /home/ubuntu/libsecp256k1
WORKDIR /home/ubuntu/libsecp256k1

RUN bash ./require.sh && rm -rf /var/lib/apt/list/*
RUN ["chmod", "+x", "compiler.sh"]
RUN ["chmod", "+x", "make_libsecp256k1.sh"]
CMD bash ./compiler.sh