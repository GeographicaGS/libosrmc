import sys

import pandas as pd

from osrmcpy import OSRM, Coordinate


# Example User Code
def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        sys.exit('Usage: {} [OSRM data base path]'.format(sys.argv[0]))

    osrm = OSRM(sys.argv[1].encode('utf-8') if len(sys.argv) >= 2 else None, True)

    # Berlin
    # start = Coordinate(id=None, longitude=13.14117, latitude=52.41445)
    # end = Coordinate(id=None, longitude=13.55747, latitude=52.61437)
    # Ireland
    # start = Coordinate(id=None, longitude=-6.346509195699211, latitude=53.36407603954265)
    # end = Coordinate(id=None, longitude=-6.35272995922493, latitude=53.283447477339756)
    start = Coordinate(id=None, longitude=-6.278496849370723, latitude=53.321071624603135)
    end = Coordinate(id=None, longitude=-6.462316552050708, latitude=53.31210678760515)

    csv_path = "geometries_output.csv"
    route = osrm.route([start, end], csv_path.encode('utf-8'))

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
