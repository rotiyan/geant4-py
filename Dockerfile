FROM ubuntu:18.04
MAINTAINER Rohin Narayan <narayan@cern.ch>
SHELL ["/bin/bash", "-c"]
USER root
ENV DEBIAN_FRONTEND=noninteractive 
ENV G4VER=10.7.1
ENV ROOTVER=6.18.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    gcc\
    cmake\
    git\
    python python-tk \
    python3 python3-pip python3-yaml python3.6-dev ipython jupyter wget unzip wget vim-gtk curl\
    libxerces-c-dev qt4-dev-tools freeglut3-dev libmotif-dev tk-dev cmake libxpm-dev libxmu-dev libxi-dev \
    dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev libxft-dev libxext-dev gfortran libssl-dev libpcre3-dev \ 
    xlibmesa-glu-dev libglew1.5-dev libftgl-dev libmysqlclient-dev libfftw3-dev libcfitsio-dev \ 
    graphviz-dev libavahi-compat-libdnssd-dev libldap2-dev python-dev libxml2-dev libkrb5-dev libgsl0-dev libqt4-dev
RUN wget https://dl.bintray.com/boostorg/release/1.75.0/source/boost_1_75_0.zip && \
    unzip boost_1_75_0.zip && rm boost_1_75_0.zip && mv boost_1_75_0 boost && cd boost && \
    ./bootstrap.sh --with-python=$(which python3) —with-python-version=$(echo $(python3 --version) | cut -d " " -f2-) —with-python-root=/usr/local/lib/python3.6/ && \
    export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/local/include/python3.6/" && \
    ./b2 --with=all && \
    ./b2 install && \
    /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/boost.conf' && \
    ldconfig && \
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
RUN mkdir -p /app/geant4 &&\
    cd /app/geant4  &&\
    mkdir -p  /app/geant4/geant4-$G4VER-install && mkdir -p  /app/geant4/geant4-$G4VER-build && \
    cd /app/geant4/ && \
    wget https://github.com/Geant4/geant4/archive/v$G4VER.tar.gz --no-check-certificate &&\
    tar -xmvf  v$G4VER.tar.gz && mv geant4-$G4VER geant4-$G4VER-source &&  cd geant4-$G4VER-source && \ 
    cd  /app/geant4/geant4-$G4VER-build && \
    #export PYTHONPATH=$PYTHONPATH:/app/geant4/geant4-$G4VER-source/environments/g4py &&\
    #cmake -DCMAKE_INSTALL_PREFIX=/app/geant4/geant4-$G4VER-install /app/geant4/geant4-$G4VER-source && \
    #cmake -DGEANT4_INSTALL_DATA=ON -DGEANT4_USE_PYTHON=ON -DGEANT4_BUILD_MULTITHREADED=ON -DGEANT4_BUILD_TLS_MODEL=global-dynamic -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_RAYTRACER_X11=ON -DGEANT4_USE_NETWORKDAW=ON . &&\
    #cmake -DCMAKE_INSTALL_PREFIX=/app/geant4/geant4-$G4VER-install  /app/geant4/geant4-$G4VER-source && \
    cmake -DGEANT4_BUILD_MULTITHREADED=ON -DGEANT4_BUILD_TLS_MODEL=global-dynamic -DGEANT4_USE_PYTHON=ON -DGEANT4_USE_SYSTEM_EXPAT=OFF  -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_INSTALL_DATA=ON -DCMAKE_INSTALL_PREFIX=/app/geant4/geant4-$G4VER-install  /app/geant4/geant4-$G4VER-source && \
    make -j 24 && make install && \
    mkdir -p /app/root/ && cd /app/root && \
    wget https://root.cern/download/root_v$ROOTVER.source.tar.gz --no-check-certificate && tar -xmvf  root_v$ROOTVER.source.tar.gz &&\
    mkdir -p /app/root/root-$ROOTVER-build  && cd /app/root/root-$ROOTVER-build && \
    cmake -DPYTHON_EXECUTABLE=/usr/bin/python3 -Dhttp=ON /app/root/root-$ROOTVER/ &&\
    cmake --build . -- -j24 &&\
    mkdir -p /opt
ENV GEANT4_INSTALL=/app/geant4/geant4-$G4VER-install
ENV PYTHONPATH=$PYTHONPATH:/app/geant4/geant4-10.7.1-install/lib/python3.6/site-packages
#ENV G4PY=/app/geant4/geant4-$G4VER-source/environments/g4py
#ENV PYTHONPATH=$PYTHONPATH:$G4PY/lib:$G4PY/examples:$G4PY/tests
#RUN . /app/geant4/geant4-$G4VER-install/bin/geant4.sh && \
#    . /app/root/root-$ROOTVER-build/bin/thisroot.sh &&\
#    cd  /app/geant4/geant4-$G4VER-source/environments/g4py && mkdir -p build && cd build &&\
#    cmake .. && make -j24 && make install 

WORKDIR /home/g4user
ENTRYPOINT . /app/geant4/geant4-$G4VER-install/bin/geant4.sh && . /app/root/root-$ROOTVER-build/bin/thisroot.sh && /bin/bash
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && python get-pip.py && pip install jupyterlab
#RUN groupadd -r g4user && useradd -r -g g4user g4user 
