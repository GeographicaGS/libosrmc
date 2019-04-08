rm -rf test_spain
mkdir test_spain
cd test_spain

echo '--Downloading OSM file...'
wget http://download.geofabrik.de/europe/spain-latest.osm.pbf

echo '--Processing - osm-extract...'
osrm-extract --profile=/usr/local/share/osrm/profiles/car.lua spain-latest.osm.pbf

if [ "$1" = 'MLD' ]; then
  echo '--Processing - osm-partition...'
  osrm-partition spain-latest.osrm

  echo '--Processing - osm-customize...'
  osrm-customize spain-latest.osrm

  echo '--Finished MLD pipeline...'
else
  echo '--Processing - osrm-contract...'
  osrm-contract spain-latest.osrm

  echo '--Finished CH pipeline...'
fi

# echo '--Starting http server - osm-routed...'
# osrm-routed --algorithm=MLD spain-latest.osrm
