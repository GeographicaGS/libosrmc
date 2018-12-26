rm -rf test_ireland
mkdir test_ireland
cd test_ireland

echo '--Downloading OSM file...'
wget http://download.geofabrik.de/europe/ireland-and-northern-ireland-latest.osm.pbf

echo '--Processing - osm-extract...'
osrm-extract --profile=/usr/local/share/osrm/profiles/car.lua ireland-and-northern-ireland-latest.osm.pbf

echo '--Processing - osm-partition...'
osrm-partition ireland-and-northern-ireland-latest.osrm

echo '--Processing - osm-customize...'
osrm-customize ireland-and-northern-ireland-latest.osrm

echo '--Processing - osrm-contract...'
osrm-contract ireland-and-northern-ireland-latest.osrm

# echo '--Starting http server - osm-routed...'
# osrm-routed --algorithm=MLD ireland-and-northern-ireland-latest.osrm
