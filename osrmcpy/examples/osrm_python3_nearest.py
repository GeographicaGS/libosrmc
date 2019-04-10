import sys

from osrmcpy import OSRM, Coordinate


# Example User Code
def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        sys.exit('Usage: {} [OSRM data base path]'.format(sys.argv[0]))

    osrm = OSRM(sys.argv[1].encode('utf-8') if len(sys.argv) >= 2 else None, True)

    # Berlin
    # coord = Coordinate(id=None, longitude=13.14117, latitude=52.41445)
    # coord = Coordinate(id=None, longitude=13.55747, latitude=52.61437)
    # Ireland
    # coord = Coordinate(id=None, longitude=-6.346509195699211, latitude=53.36407603954265)
    # coord = Coordinate(id=None, longitude=-6.35272995922493, latitude=53.283447477339756)
    # coord = Coordinate(id=None, longitude=-6.278496849370723, latitude=53.321071624603135)
    # coord = Coordinate(id=None, longitude=-6.21116379, latitude=53.43477538)
    coord = Coordinate(id=None, longitude=-6.24003956, latitude=53.37190879)
    # coord = Coordinate(id=None, longitude=-6.462316552050708, latitude=53.31210678760515)

    nearest = osrm.nearest(coord)
    nearest_excl = osrm.nearest(coord, exclude='motorway')

    if nearest:
        print('Latitude: {0}, Longitude: {1}'.format(nearest.latitude, nearest.longitude))
        print('Latitude: {0}, Longitude: {1} - Excluded'.format(nearest_excl.latitude, nearest_excl.longitude))

    else:
        print('No nearest coordinates found')


if __name__ == '__main__':
    main()
