rm -rf test_berlin
mkdir test_berlin
cd test_berlin

echo '--Downloading OSM file...'
wget http://download.geofabrik.de/europe/germany/berlin-latest.osm.pbf

echo '--Processing - osm-extract...'
osrm-extract --profile=/usr/local/share/osrm/profiles/car.lua berlin-latest.osm.pbf

echo '--Processing - osm-partition...'
osrm-partition berlin-latest.osrm

echo '--Processing - osm-customize...'
osrm-customize berlin-latest.osrm

echo '--Processing - osrm-contract...'
osrm-contract berlin-latest.osrm

# echo '--Starting http server - osm-routed...'
# osrm-routed --algorithm=MLD berlin-latest.osrm
