FROM python:3.6.7

# Environment
ENV OSRM_VERSION 5.22.0
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV BUILD_DIR /usr/src

WORKDIR /usr/local/app

# Sources
ADD https://github.com/Project-OSRM/osrm-backend/archive/v${OSRM_VERSION}.tar.gz ${BUILD_DIR}
ADD . ${BUILD_DIR}

# Install OSRM dependencies
RUN apt-get -qq update
RUN apt-get -qqy install --no-install-recommends \
    build-essential \
    wget cmake pkg-config \
    libbz2-dev libxml2-dev \
    libzip-dev libboost-all-dev \
    lua5.2 liblua5.2-dev libtbb-dev
RUN apt-get -qqy clean
RUN apt-get -qqy autoremove
RUN apt-get -qqy autoclean
RUN rm -rf /var/lib/apt/lists/*

# Compile and install OSRM
RUN cd ${BUILD_DIR} \
  && tar -xvf v${OSRM_VERSION}.tar.gz \
  && cd osrm-backend-${OSRM_VERSION} \
  && mkdir -p build \
  && cd build \
  && cmake .. -DCMAKE_BUILD_TYPE=Release \
  && cmake --build . -- -j $(nproc) \
  && cmake --build . --target install -- -j $(nproc)

# Install Python requirements
RUN cd ${BUILD_DIR} \
  && python -m pip install --no-cache-dir -r requirements.txt

# Compile and install Python OSRM binding
RUN cd ${BUILD_DIR} && cd libosrmc/ && ./build.sh
RUN cd ${BUILD_DIR} && python -m pip install .

# Clean
RUN rm -rf ${BUILD_DIR}/*
