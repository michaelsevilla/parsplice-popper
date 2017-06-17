FROM ubuntu:trusty

ARG DEBIAN_FRONTEND=noninteractive
ENV PATH=$PATH:/opt/bin
COPY patches/* /root/
COPY Makefile.cfg /root/

# install deps
RUN apt-get update -y && \
    apt-get install -y wget git make g++ gfortran vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* debian/

# install leveldb
RUN wget https://github.com/google/leveldb/archive/v1.14.tar.gz && \
    tar xzvf v1.14.tar.gz && \
    cd leveldb-1.14 && \
    make

# install mpi
RUN wget http://www.mpich.org/static/downloads/3.1/mpich-3.1.tar.gz && \
    tar xzf mpich-3.1.tar.gz && \
    cd mpich-3.1 && \ 
    ./configure --prefix=/opt --enable-thread-cs=per-object && \
    git apply /root/mpi.diff && \
    make && \
    make install

# install mdhim
RUN git clone https://github.com/mdhim/mdhim-tng.git && \
    cd mdhim-tng && \
    cp /root/Makefile.cfg . && \
    git apply /root/mdhim.diff && \
    make && \
    cd tests && \
    make
