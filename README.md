# libosrmc

This repository is Geographica version of libosrmc, focused only on Python 3 binding (osrmcpy). This repository is a fork of https://github.com/daniel-j-h/libosrmc , which is a C wrapper around the C++ libosrm library, useful for writing FFI bindings and guaranteeing ABI stability.

### Docker

Build and up docker container:
```
$ docker-compose build
$ docker-compose up
```

Preprocessing pipeline to generate test data
```
$ docker-compose exec osrmcpy-jupyter bash -c 'cd data && ./preprocessing_monaco.sh'
```

##### Quick Start

    cd libosrmc
    make
    sudo make install
    sudo ldconfig

This compiles the `libosrmc.so` shared object and installs it into `/usr/local` (you may have to `export LD_LIBRARY_PATH="/usr/local/lib"`) or install to `/usr/lib`.
The library's interface `osrmc.h` gets installed into `/usr/local/include/osrmc/osrmc.h`.
You can modify defaults via `config.mk`.


##### License

Copyright © 2018 Cayetano Benavent - Geographica (Python3 binding; more functionalities to C Inteface)

Copyright © 2016 Daniel J. Hofmann (Creator of libosrmc project)

Distributed under the MIT License (MIT).
