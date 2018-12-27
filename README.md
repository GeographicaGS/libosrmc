# libosrmc

This repository is Geographica version of libosrmc, focused only on Python 3 binding (osrmcpy). This repository is a fork of https://github.com/daniel-j-h/libosrmc , which is a C wrapper around the C++ libosrm library, useful for writing FFI bindings and guaranteeing ABI stability.

## Using with Docker

### Building

First you must build Docker container:

```
$ docker-compose build
```

### Up and running

Up Docker container:
```
$ docker-compose up
```

And and use these examples through JupyterLab in ```http://localhost:8888```:
- notebooks/osrmcpy_compute_matrix.ipynb.
- notebooks/osrmcpy_compute_route.ipynb.
- notebooks/osrmcpy_compute_nearest.ipynb.

Before to use examples you must prepare test datasets (see Data processing).


### Data preprocessing

There are two preprocessing pipelines to use OSRM:
- MLD: Multi-Level Dijkstra.
- CH: Contraction Hierarchies. You should use CH when performance is important.

Preprocessing pipelines to generate test data:

- CH pipeline example:
```
$ docker-compose exec osrmcpy-jupyter bash -c 'cd data && ./preprocessing_monaco.sh'
```

- MLD pipeline example:
```
$ docker-compose exec osrmcpy-jupyter bash -c 'cd data && ./preprocessing_monaco.sh MLD'
```

You have scripts in data folder to generate test datasets for three locations:
- Monaco (little)
- Berlin (medium)
- Ireland (moderately large)


## Building without Docker

First you need to build and install [osrm-backend](https://github.com/Project-OSRM/osrm-backend).

Second you need to build and install C/C++ interface to OSRM.

```
$ cd libosrmc
$ make
$ sudo make install
$ sudo ldconfig
```

This compiles the `libosrmc.so` shared object and installs it into `/usr/local` (you may have to `export LD_LIBRARY_PATH="/usr/local/lib"`) or install to `/usr/lib`.
The library's interface `osrmc.h` gets installed into `/usr/local/include/osrmc/osrmc.h`.
You can modify defaults via `config.mk`.

Last you can install Python3 binding:

```
$ python -m pip install .
```

You can test it with this examples:
- osrmcpy/examples/osrm_python3_matrix.py.
- osrmcpy/examples/osrm_python3_route.py.
- osrmcpy/examples/osrm_python3_nearest.py.

## License

Copyright © 2018 Cayetano Benavent - Geographica (Python3 binding; more functionalities to C/C++ Interface)

Copyright © 2016 Daniel J. Hofmann (Creator of libosrmc project)

Distributed under the MIT License (MIT).
