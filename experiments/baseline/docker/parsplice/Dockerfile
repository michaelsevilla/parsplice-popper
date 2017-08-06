FROM ubuntu:xenial

# install deps
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    echo "--> parsplice deps" && \
    apt-get -y --no-install-recommends install \
      build-essential pkg-config cmake python gcc cmake-data g++ git wget \
      gfortran libblas-dev python-numpy python3-numpy libopenmpi-dev \
      libboost-all-dev liblapack-dev && \
    echo "--> pbs deps" && \
    apt-get -y --no-install-recommends install \
      openssh-server torque-server torque-client torque-mom torque-pam && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install custom leveldb and toy example to start shared memory perf counters
RUN mkdir -p /etc/riak && \
    touch /etc/riak/perf_counters && \
    git config --global http.sslVerify false && \
    git clone https://github.com/michaelsevilla/leveldb.git /leveldb && \
    cd /leveldb && \
    make -j24 && \
    make tools && \
    git clone https://github.com/dazfuller/LevelDB-Sample.git /sample && \
    cd /sample && \
    sed -i 's/-lleveldb/-lleveldb -I\/leveldb\/include -I\/leveldb -L\/leveldb /g' Makefile && \
    sed -i 's/-lsnappy//g' Makefile && \
    make

# install custom packages
ADD src/deps /usr/local/exaalt_deps
RUN cd /usr/local/exaalt_deps && \
    tar xzf boost_1_62_0.tar.gz && \
    tar xzf db-6.2.23.tar.gz && \
    tar xzf nauty26r7.tar.gz && \
    tar xjf eigen-eigen-26667be4f70b.tar.bz2 && \
    echo "--> db deps" && \
    cd /usr/local/exaalt_deps/db-6.2.23/build_unix && \
    ../dist/configure --enable-stl --enable-cxx --prefix=/usr/local/ && \
    make -j24 && \
    make install && \
    echo "--> nauty deps" && \
    cd /usr/local/exaalt_deps/nauty26r7 && \
    ./configure --prefix=/usr/local/ && \
    make -j24 && \
    cp nauty.a /usr/local/lib/libnauty.a && \
    mkdir /usr/local/include/nauty && \
    cp *.h /usr/local/include/nauty && \
    echo "--> eighen deps" && \
    cd /usr/local/exaalt_deps/eigen-eigen-26667be4f70b && \
    cp -r Eigen /usr/local/include/.

# install LANL LATTE package
RUN git clone https://github.com/lanl/LATTE.git /usr/local/LATTE && \
    cd /usr/local/LATTE && \
    cp ./makefiles/makefile.CHOICES.gfort.lapack.lmp makefile.CHOICES && \
    make -j24 && \
    cp /usr/local/LATTE/liblatte.a /usr/local/lib/.

# install LANL LAMMPS package
RUN git clone https://rjzamora:Phishy_217@gitlab.com/exaalt/lammps.git /usr/local/lammps && \
    cd /usr/local/lammps && \
    git checkout exaalt && \
    git pull origin exaalt  && \
    cd /usr/local/lammps/lib/latte && \
    cp Makefile.lammps.gfortran Makefile.lammps && \
    cd /usr/local/lammps/src && \
    make yes-latte -j24 && \
    make yes-molecule -j24 && \
    make yes-manybody -j24 && \
    make yes-kspace -j24 && \
    make yes-snap -j24 && \
    make yes-misc -j24 && \
    cp MAKE/MACHINES/Makefile.ubuntu_simple MAKE/Makefile.mpi && \
    ln -s /usr/local/LATTE/ /root/LATTE && \
    cd /usr/local/lammps/src && \
    make mpi -j24 && \
    make mpi mode=lib && \
    cp /usr/local/lammps/src/liblammps_mpi.a /usr/local/lib/. && \
    mkdir /usr/local/include/lammps && \
    cp /usr/local/lammps/src/*.h /usr/local/include/lammps/.

# make this container deployable with SSH (based on ivotron/openmpi:v2.0.2)
ADD .ssh /root/.ssh
RUN mkdir -p /var/run/sshd && \
    sed -i "s/UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config && \
    sed -i "s/UsePAM.*/UsePAM no/g" /etc/ssh/sshd_config && \
    sed -i "s/PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config && \
    mkdir -p /root/.ssh && \
    echo 'Host *' > /root/.ssh/config && \
    echo 'StrictHostKeyChecking no' >> /root/.ssh/config && \
    echo 'LogLevel quiet' >> /root/.ssh/config && \
    chmod 600 /root/.ssh/config /root/.ssh/id_rsa && \
    wget --no-check-certificate https://raw.githubusercontent.com/ivotron/docker-openssh/d1db8b1c29b532896b8a91009820f732dcae6b79/entrypoint.sh && \
    mv entrypoint.sh /root/.ssh/ && chmod 750 /root/.ssh/entrypoint.sh && \
    wget --no-check-certificate https://raw.githubusercontent.com/ivotron/docker-openssh/d1db8b1c29b532896b8a91009820f732dcae6b79/stopsshd && \
    mv stopsshd /usr/bin/ && chmod 750 /usr/bin/stopsshd

# install a leveldb perf counter designed for graphite
RUN git clone https://github.com/michaelsevilla/leveldb.git /myleveldb && \
    cd /myleveldb && \
    git checkout graphite && \
    make && \
    make tools

# install parsplice
ENV COMPILER     "mpic++"
ENV local_PREFIX /usr/local/
ENV super_PREFIX /usr/
ENV bldir_PREFIX /builds/exaalt/parsplice/build/
ENV latte_PATH   /usr/local/LATTE
ADD src /parsplice
RUN cd /parsplice && \
    mkdir build && \
    cd build && \
    cmake \
      -DCMAKE_INCLUDE_PATH=${local_PREFIX}/include/:${global_PREFIX}/include/:/usr/include \
      -DCMAKE_BINARY_DIR=${bldir_PREFIX} \
      -DEXTRA_FLAGS="-I${latte_PATH}/src -I/leveldb -I/leveldb/include" \
      -DEXTRA_LINK_FLAGS="-fopenmp ${latte_PATH}/src/latte_c_bind.o ${latte_PATH}/liblatte.a -lgfortran  -llapack -lblas -lleveldb -L/leveldb" \
      -DCMAKE_LIBRARY_PATH=${local_PREFIX}/lib:${global_PREFIX}/lib/:/leveldb \
      -DCMAKE_CXX_COMPILER=${COMPILER} \
      -DCMAKE_INSTALL_PREFIX=/root \
      /parsplice && \
    make -j24 && \
    make install && \
    cp -r /parsplice/sample-input/UO2/* /root/ && \
    ldconfig

ADD entrypoint.sh /usr/bin
RUN chmod 750 /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
