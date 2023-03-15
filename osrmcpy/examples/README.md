# Point to point routes

The point-to-point script is a simple command line script that needs the start and end point longitude and latitude coordinates of the route, and the path to the OSRM database:

In case you need help on how to use the script you can use the `-h/--help` flag:
```bash
$ python ./osrm_python3_route.py --help
usage: Point-to-Point route. [-h] -s START START -e END END -O OSRM

Computes a point to point route optimization.

optional arguments:
  -h, --help            show this help message and exit
  -s START START, --start START START
                        Route start point as coordinates (longitude, latitude)
                        tuple.
  -e END END, --end END END
                        Route end point as coordinates (longitude, latitude)
                        tuple.
  -O OSRM, --osrm OSRM  OSRM data base path.
```
## Example of usage:
```bash
python ./osrm_python3_route.py --start -8.9 53.3 --end -9.1 53.2  --osrm <Path_to_OSRM_database>
```
