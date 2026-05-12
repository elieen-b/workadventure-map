These Python scripts generate maps for [Workadventurei](https://workadventu.re) from [OpenStreetMap](https://openstreetmap.org) island polygons.

Generate a single WA map
============================

First lookup the ID of the island relation to generate, e.g. for Hawai, the ID is [3403603](https://openstreetmap.org/relation/3403603). Note that an island relation consists of one or more ways (polygons) and the script expects the relation ID, not the way ID, even if there is only one way.

~~~py
python tile.py --polygon 3403603 --output JSON
~~~

You can get info on the parameters to be used  with `python tile.py --help`

Generated map images in PNG format will be saved in file "map.png" and overwritten if already existing (TODO change).

The script executes the following steps:

* download the polygon in GeoJSON format, potentially simplified, from <http://polygons.openstreetmap.fr>
* scale the coordinates to unify map sizes in number of tiles
* create an indexed map with the tile index derived from the topology of the tiles with regard to the outline
* create and output JSON for Tiled/WorkAdventure maps (depending on output opion)
* create and show PNG of Tiled/WorkAdventure map (depending on output opion)


Generate a set of maps
===============================

~~~py
python islandSelection.py
~~~

This will generate TileEd/WorkAdventure worlds for a preselected list of islands. They are given as a list with name, OSM ID and zoom. There is also a function to generate an index.html with all the islands, the links to the island in OpenStreetMap and the Wikipedia article. The generated list can be seen [here](https://hlg.github.io/wamap/).

Downloaded and generated JSON files will be saved in folder "selectedIslands" which is created in case it does not exist.

* `xxx_original.json` original polygon without geometric simplification 
* `xxx_simplified.json` simplified polygon with geometric simplification 
* `xxx-map.json` TileEd/WorkAdventure world with indexed tile map

## Lokaler Webserver
Im Projektordner starten:
python3 -m http.server 8080

Dann im Browser öffnen:
http://localhost:8080/index.html



