'''Script to calculate a point-to-point route.'''
import argparse
import pathlib

import pandas as pd
from osrmcpy import OSRM, Coordinate


def parse_command():
    """Create a parser for this script."""
    parser = argparse.ArgumentParser(
        prog='Point-to-Point route.',
        description='Computes a point to point route optimization.',
    )

    parser.add_argument(
        '-s', '--start',
        required=True,
        nargs=2,
        type=float,
        help='Route start point as coordinates (longitude, latitude) tuple.',
    )
    parser.add_argument(
        '-e', '--end',
        required=True,
        nargs=2,
        type=float,
        help='Route end point as coordinates (longitude, latitude) tuple.',
    )
    parser.add_argument(
        '-O', '--osrm',
        required=True,
        type=pathlib.Path,
        help='OSRM data base path.'
    )

    return parser


def main():
    parser = parse_command()
    args = parser.parse_args()

    osrm_path = str(args.osrm.resolve())
    route_start = args.start
    route_end = args.end

    osrm = OSRM(osrm_path.encode('utf-8'), True)

    start = Coordinate(id=None, longitude=route_start[0], latitude=route_start[1])
    end = Coordinate(id=None, longitude=route_end[0], latitude=route_end[1])

    csv_path = "geometries_output.csv"
    route = osrm.route([start, end], csv_path=csv_path.encode('utf-8'))

    if route:
        print(route)
        print('Distance: {0:.0f} meters'.format(route.distance))
        print('Duration: {0:.0f} seconds'.format(route.duration))
        print('Geometry: {0}'.format(route.geometry))

        df_geoms = pd.read_csv(csv_path, names=['id', 'distance', 'duration', 'polyline_geom'])
        print(df_geoms.head(25))

    else:
        print('No route found')


if __name__ == '__main__':
    main()
