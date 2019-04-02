"""

The MIT License (MIT)

Copyright (c) 2016 Daniel J. Hofmann

Copyright (c) 2018 Cayetano Benavent - Geographica

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import ctypes as c

from collections import namedtuple
from contextlib import contextmanager

# Native Functions Bridge
lib = c.CDLL('libosrmc.so')

# Error handling
lib.osrmc_error_message.restype = c.c_char_p
lib.osrmc_error_message.argtypes = [c.c_void_p]

lib.osrmc_error_destruct.restype = None
lib.osrmc_error_destruct.argtypes = [c.c_void_p]


class osrmc_error(c.c_void_p):
    def __str__(self):
        return lib.osrmc_error_message(self).decode('utf-8')

    def __del__(self):
        lib.osrmc_error_destruct(self)


def osrmc_error_errcheck(result, func, arguments):
    if len(arguments) > 0 and type(arguments[-1]._obj) == osrmc_error and arguments[-1]._obj.value:
        raise RuntimeError(arguments[-1]._obj)
    return result


# Config
lib.osrmc_config_construct.restype = c.c_void_p
lib.osrmc_config_construct.argtypes = [c.c_char_p, c.c_bool, c.c_void_p]
lib.osrmc_config_construct.errcheck = osrmc_error_errcheck

lib.osrmc_config_destruct.restype = None
lib.osrmc_config_destruct.argtypes = [c.c_void_p]

# OSRM
lib.osrmc_osrm_construct.restype = c.c_void_p
lib.osrmc_osrm_construct.argtypes = [c.c_void_p, c.c_void_p]
lib.osrmc_osrm_construct.errcheck = osrmc_error_errcheck

lib.osrmc_osrm_destruct.restype = None
lib.osrmc_osrm_destruct.argtypes = [c.c_void_p]

# Generic Param Handling
lib.osrmc_params_add_coordinate.restype = None
lib.osrmc_params_add_coordinate.argtypes = [c.c_void_p, c.c_float, c.c_float, c.c_void_p]
lib.osrmc_params_add_coordinate.errcheck = osrmc_error_errcheck

# Route Params
lib.osrmc_route_params_construct.restype = c.c_void_p
lib.osrmc_route_params_construct.argtypes = [c.c_void_p]
lib.osrmc_route_params_construct.errcheck = osrmc_error_errcheck

lib.osrmc_route_params_add_steps.restype = c.c_void_p
lib.osrmc_route_params_add_steps.argtypes = [c.c_void_p, c.c_int]

lib.osrmc_route_params_add_overview_full.restype = c.c_void_p
lib.osrmc_route_params_add_overview_full.argtypes = [c.c_void_p, c.c_int]

lib.osrmc_route_params_add_continue_straight.restype = c.c_void_p
lib.osrmc_route_params_add_continue_straight.argtypes = [c.c_void_p, c.c_int]

lib.osrmc_route_params_destruct.restype = None
lib.osrmc_route_params_destruct.argtypes = [c.c_void_p]

# Route
lib.osrmc_route.restype = c.c_void_p
lib.osrmc_route.argtypes = [c.c_void_p, c.c_void_p, c.c_void_p]
lib.osrmc_route.errcheck = osrmc_error_errcheck

lib.osrmc_route_response_destruct.restype = None
lib.osrmc_route_response_destruct.argtypes = [c.c_void_p]

lib.osrmc_route_response_distance.restype = c.c_float
lib.osrmc_route_response_distance.argtypes = [c.c_void_p, c.c_void_p]
lib.osrmc_route_response_distance.errcheck = osrmc_error_errcheck

lib.osrmc_route_response_duration.restype = c.c_float
lib.osrmc_route_response_duration.argtypes = [c.c_void_p, c.c_void_p]
lib.osrmc_route_response_duration.errcheck = osrmc_error_errcheck

lib.osrmc_route_response_geometry.restype = c.c_char_p
lib.osrmc_route_response_geometry.argtypes = [c.c_void_p, c.c_void_p]
lib.osrmc_route_response_geometry.errcheck = osrmc_error_errcheck

lib.osrmc_route_response_geometry_legs.restype = c.c_void_p
lib.osrmc_route_response_geometry_legs.argtypes = [c.c_void_p, c.c_char_p, c.c_void_p]
lib.osrmc_route_response_geometry_legs.errcheck = osrmc_error_errcheck

# Table Params
lib.osrmc_table_params_construct.restype = c.c_void_p
lib.osrmc_table_params_construct.argtypes = [c.c_void_p]
lib.osrmc_table_params_construct.errcheck = osrmc_error_errcheck

lib.osrmc_table_params_destruct.restype = None
lib.osrmc_table_params_destruct.argtypes = [c.c_void_p]

# Table
lib.osrmc_table.restype = c.c_void_p
lib.osrmc_table.argtypes = [c.c_void_p, c.c_void_p, c.c_void_p]
lib.osrmc_table.errcheck = osrmc_error_errcheck

lib.osrmc_table_response_destruct.restype = None
lib.osrmc_table_response_destruct.argtypes = [c.c_void_p]

lib.osrmc_table_response_duration.restype = c.c_float
lib.osrmc_table_response_duration.argtypes = [c.c_void_p, c.c_ulong, c.c_ulong, c.c_void_p]
lib.osrmc_table_response_duration.errcheck = osrmc_error_errcheck

lib.osrmc_table_response_distance.restype = c.c_float
lib.osrmc_table_response_distance.argtypes = [c.c_void_p, c.c_ulong, c.c_ulong, c.c_void_p]
lib.osrmc_table_response_distance.errcheck = osrmc_error_errcheck

# Nearest Params
lib.osrmc_nearest_params_construct.restype = c.c_void_p
lib.osrmc_nearest_params_construct.argtypes = [c.c_void_p]
lib.osrmc_nearest_params_construct.errcheck = osrmc_error_errcheck

lib.osrmc_nearest_params_destruct.restype = None
lib.osrmc_nearest_params_destruct.argtypes = [c.c_void_p]

# Nearest
lib.osrmc_nearest.restype = c.c_void_p
lib.osrmc_nearest.argtypes = [c.c_void_p, c.c_void_p, c.c_void_p]
lib.osrmc_nearest.errcheck = osrmc_error_errcheck

lib.osrmc_nearest_response_destruct.restype = None
lib.osrmc_nearest_response_destruct.argtypes = [c.c_void_p]

lib.osrmc_nearest_response_coordinates.restype = c.c_void_p
lib.osrmc_nearest_response_coordinates.argtypes = [c.c_void_p, c.c_float * 2, c.c_void_p]
lib.osrmc_nearest_response_coordinates.errcheck = osrmc_error_errcheck


# Python Library Interface
@contextmanager
def scoped_config(base_path):
    config = lib.osrmc_config_construct(base_path, c.byref(osrmc_error()))
    yield config
    lib.osrmc_config_destruct(config)


@contextmanager
def scoped_osrm(config):
    osrm = lib.osrmc_osrm_construct(config, c.byref(osrmc_error()))
    yield osrm
    lib.osrmc_osrm_destruct(osrm)


@contextmanager
def scoped_route_params():
    params = lib.osrmc_route_params_construct(c.byref(osrmc_error()))
    yield params
    lib.osrmc_route_params_destruct(params)


@contextmanager
def scoped_route(osrm, params):
    route = lib.osrmc_route(osrm, params, c.byref(osrmc_error()))
    yield route
    lib.osrmc_route_response_destruct(route)


@contextmanager
def scoped_table_params():
    params = lib.osrmc_table_params_construct(c.byref(osrmc_error()))
    yield params
    lib.osrmc_table_params_destruct(params)


@contextmanager
def scoped_table(osrm, params):
    route = lib.osrmc_table(osrm, params, c.byref(osrmc_error()))
    yield route
    lib.osrmc_table_response_destruct(route)


@contextmanager
def scoped_nearest_params():
    params = lib.osrmc_nearest_params_construct(c.byref(osrmc_error()))
    yield params
    lib.osrmc_nearest_params_destruct(params)


@contextmanager
def scoped_nearest(osrm, params):
    nearest = lib.osrmc_nearest(osrm, params, c.byref(osrmc_error()))
    yield nearest
    lib.osrmc_nearest_response_destruct(nearest)


Coordinate = namedtuple('Coordinate', 'id longitude latitude')
Route = namedtuple('Route', 'distance duration geometry')
Table = list


class OSRM:
    def __init__(self, base_path, contraction=False):
        self.config = None
        self.osrm = None

        self.config = lib.osrmc_config_construct(base_path, contraction, c.byref(osrmc_error()))
        assert self.config

        self.osrm = lib.osrmc_osrm_construct(self.config, c.byref(osrmc_error()))
        assert self.osrm

    def __del__(self):
        if self.osrm:
            lib.osrmc_osrm_destruct(self.osrm)
        if self.config:
            lib.osrmc_config_destruct(self.config)

    def route(self, coordinates, csv_path=None, full_geom=True, continue_straight=True):
        with scoped_route_params() as params:
            assert params

            lib.osrmc_route_params_add_continue_straight(params, int(continue_straight))
            lib.osrmc_route_params_add_overview_full(params, int(full_geom))

            add_steps = 1 if csv_path else 0
            lib.osrmc_route_params_add_steps(params, add_steps)

            for coordinate in coordinates:
                lib.osrmc_params_add_coordinate(params, coordinate.longitude, coordinate.latitude, c.byref(osrmc_error()))

            with scoped_route(self.osrm, params) as route:
                if route:
                    distance = lib.osrmc_route_response_distance(route, c.byref(osrmc_error()))
                    duration = lib.osrmc_route_response_duration(route, c.byref(osrmc_error()))
                    geometry = lib.osrmc_route_response_geometry(route, c.byref(osrmc_error()))

                    if csv_path:
                        lib.osrmc_route_response_geometry_legs(route, csv_path, c.byref(osrmc_error()))

                    return Route(distance=distance, duration=duration, geometry=geometry)
                else:
                    return None

    def table(self, coordinates, sources=None):
        with scoped_table_params() as params:
            assert params

            for coordinate in coordinates:
                lib.osrmc_params_add_coordinate(params, coordinate.longitude, coordinate.latitude, c.byref(osrmc_error()))

            with scoped_table(self.osrm, params) as table:
                if table:
                    n = len(coordinates)
                    src_idxs = sources if sources else range(n)
                    return Table([(coordinates[s].id, coordinates[t].id,
                                   lib.osrmc_table_response_duration(table, s, t, c.byref(osrmc_error())),
                                   lib.osrmc_table_response_distance(table, s, t, c.byref(osrmc_error()))
                                   ) for t in range(n)] for s in src_idxs)
                else:
                    return None

    def nearest(self, coordinate):
        with scoped_nearest_params() as params:
            assert params

            lib.osrmc_params_add_coordinate(params, coordinate.longitude, coordinate.latitude, c.byref(osrmc_error()))

            with scoped_nearest(self.osrm, params) as nearest:
                if nearest:
                    nearest_coord = (c.c_float * 2)()
                    lib.osrmc_nearest_response_coordinates(nearest, nearest_coord, c.byref(osrmc_error()))
                    return Coordinate(id=None, latitude=nearest_coord[0], longitude=nearest_coord[1])
                else:
                    return None
