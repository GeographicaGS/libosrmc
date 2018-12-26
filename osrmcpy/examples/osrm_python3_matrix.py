import sys
import random

import numpy as np
import pandas as pd

from osrmcpy import OSRM, Coordinate


# Example User Code
def main():
    random.seed(19)

    if '--help' in sys.argv or '-h' in sys.argv:
        sys.exit('Usage: {} [OSRM data base path]'.format(sys.argv[0]))

    osrm = OSRM(sys.argv[1].encode('utf-8') if len(sys.argv) >= 2 else None, False)

    # Somewhere in an area in Monaco..
    # bottom_left = Coordinate(longitude=7.413194, latitude=43.731056)
    # top_right = Coordinate(longitude=7.421639, latitude=43.735440)
    # Berlin
    # bottom_left = Coordinate(id=None, longitude=13.14117, latitude=52.41445)
    # top_right = Coordinate(id=None, longitude=13.55747, latitude=52.61437)
    # Ireland - Dublin
    bottom_left = Coordinate(id=None, longitude=-6.57013, latitude=53.23382)
    top_right = Coordinate(id=None, longitude=-6.23988, latitude=53.39977)

    random_coordinate = lambda n: Coordinate(id=n, longitude=random.uniform(bottom_left.longitude, top_right.longitude),
                                             latitude=random.uniform(bottom_left.latitude, top_right.latitude))

    coordinates = [random_coordinate(i) for i in range(100)]
    table = osrm.table(coordinates)
    df_table = pd.DataFrame(np.array(table).reshape(-1, 4), columns=['from', 'to', 'duration', 'distance'])
    print(df_table.head(20))
    print(df_table.shape)

    # if table:
    #     print('Table')
    #     for row in table:
    #         for duration in row:
    #             print('{0:.0f}s\t'.format(duration), end='')
    #             print(duration)
    #         print()

    print('Computed...')

    # print(table)
    # print(table.head(20))
    # print(df.head())
    # print('Matrix size: {}'.format(len(table)))
    # print(table)
    # with open('coordinates.csv', 'w') as f:
    #     f.write('id,lat,lon\n')
    #     for coor in coordinates:
    #         f.write('{0},{1},{2}\n'.format(coor.id, coor.latitude, coor.longitude))
    # else:
    #     print('No table found')


if __name__ == '__main__':
    main()
