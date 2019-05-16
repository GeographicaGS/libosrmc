# libosrmc

This repository is Geographica version of libosrmc, focused only on Python 3 binding (osrmcpy). This repository is a fork of https://github.com/daniel-j-h/libosrmc , which is a C wrapper around the C++ libosrm library, useful for writing FFI bindings and guaranteeing ABI stability.

## Using with Docker

### Building

First you must build base Docker image:

```
$ cd docker
$ docker build --pull -t geographica/osrmcpy:latest .
```

#### Running with Jupyter

You must build your Docker container with Docker-Compose:

```
$ docker-compose build osrmcpy-jupyter
```

This container exposes the internal port 8888 to the host port 8889.

#### Running without Jupyter

You must build your Docker container with Docker-Compose:

```
$ docker-compose build osrmcpy
```

This container exposes the internal port 5000 to the host port 5050.

### Jupyter up and running

Up Docker container:
```
$ docker-compose up osrmcpy-jupyter
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
$ docker-compose exec osrmcpy bash -c 'cd data && ./preprocessing_monaco.sh'
```

- MLD pipeline example:
```
$ docker-compose exec osrmcpy bash -c 'cd data && ./preprocessing_monaco.sh MLD'
```

You have scripts in data folder to generate test datasets for three locations:
- Monaco (little)
- Berlin (medium)
- Ireland (moderately large)
- Spain (large)
- France (extra large)

#### Notes on procesing data

Here is the information related to the performance procesing the data for France

```
8 x Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
Mem:       16GB
Swap:       2GB

france-latest.osm.pbf  3.43G

--Processing - osm-extract...
RAM: peak bytes used: 12157050880
time: 13m23.498s

--Processing - osrm-contract...
RAM: peak bytes used: 5705818112
time: 40m27.110s

france_osrm_ch/ 7.5G
```

### Using the API

Launch the API pointing to an osrm file
```
$ docker-compose run --service-ports osrmcpy osrm-routed ./data/osrm/france_osrm_ch/france-latest.osrm
```

Example
```
http://localhost:5050/table/v1/car/3.081427,48.809148;3.243775,48.811817;3.228700,48.759358;3.230363,48.800354?sources=0&annotations=distance,duration
```

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
