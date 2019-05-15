rm -rf test_france
mkdir test_france
cd test_france

echo '--Downloading OSM file...'
time wget -rc http://download.geofabrik.de/europe/france-latest.osm.pbf
cp download.geofabrik.de/europe/france-latest.osm.pbf .

echo '--Processing - osm-extract...'
time osrm-extract --profile=/usr/local/share/osrm/profiles/car.lua france-latest.osm.pbf

if [ "$1" = 'MLD' ]; then
  echo '--Processing - osm-partition...'
  osrm-partition france-latest.osrm

  echo '--Processing - osm-customize...'
  osrm-customize france-latest.osrm

  echo '--Finished MLD pipeline...'
else
  echo '--Processing - osrm-contract...'
  time osrm-contract france-latest.osrm

  echo '--Finished CH pipeline...'
fi

# echo '--Starting http server - osm-routed...'
# osrm-routed --algorithm=MLD france-latest.osrm
