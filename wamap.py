mapWidth=73
mapHeight=89
tileSize= 32
exit="map.json"

import json
import urllib.request
import urllib.parse

osmRoads = []

def exitLayer(name, layerId, exitTile, exitCoords, exitUrl, visible=True):
  data = [0] * (mapWidth*mapHeight)
  for (x,y) in exitCoords:
    data[y*mapHeight+x] = exitTile
  layer = tileLayer(name, layerId, data, visible)
  layer["properties"] = [{
      "name":"exitSceneUrl",
      "type":"string",
      "value": exitUrl
  }]
  return layer

def linkLayer(name, layerId, linkTile, linkCoords, linkUrl, visible=True):
  data = [0] * (mapWidth*mapHeight)
  for (x,y) in linkCoords:
    data[y*mapHeight+x] = linkTile
  layer = tileLayer(name, layerId, data, visible)
  layer["properties"] = [{
      "name":"openWebsite",
      "type":"string",
      "value": linkUrl
  }]
  return layer

def tileLayer(name, layerId, data, visible=True):
  layer = baseLayer(name, layerId, "tilelayer", visible)
  layer["data"] = data
  return layer 

def imageLayer(name, layerId, image, visible=True):
  layer = baseLayer(name, layerId, "imageLayer", visible)
  layer["image"] = image
  return layer 

def objectLayer(name, layerId, objects, visible=True):
  layer = baseLayer(name, layerId, "objectgroup", visible)
  layer["objects"] = objects
  return layer

def baseLayer(name, layerId, layerType, visible=True):
  return {
    "name": name,
    "id": layerId,
    "x":0,
    "y":0,
    "width":mapWidth,
    "height":mapHeight,
    "visible": visible,
    "opacity":1,
    "type": layerType
  }
def defaultPlaces():

  return [
    {
      "id": 1,
      "name": "Bergen",
      "type": "village",
      "x": 500,
      "y": 500,
      "width": 16,
      "height": 16,
      "point": True

    },
    {
      "id": 2,
      "name": "Sassnitz",
      "type": "town",
      "x": 60,
      "y": 40,
      "width": 20,
      "height": 20,
      "point": True
    }
  ]

def createPlaceLabels(places):
  labels = []
  label_id = 1

  for place in places:
    if not place.get("name"):
      continue

    labels.append({
      "id": label_id,
      "name": place["name"] + " Label",
      "type": "text",
      "x": place["x"] + 8,
      "y": place["y"] - 8,
      "text": place["name"]
    })

    label_id += 1

  return labels

def create_osm_roads():
  print("OSM roads loader started")
  return []

def get_bounds_from_geojson(filename):
  with open(filename) as f:
    geojson = json.load(f)

  coordinates = []

  def collect(data):
    if isinstance(data, list):
      if len(data) == 2 and isinstance(data[0], (int, float)):
        coordinates.append(data)
      else:
        for item in data:
          collect(item)

  for geometry in geojson["geometries"]:
    collect(geometry["coordinates"])

  lons = [p[0] for p in coordinates]
  lats = [p[1] for p in coordinates]

  return (min(lons), min(lats), max(lons), max(lats))

def create_overpass_query(bounds):
  south = bounds[1]
  west = bounds[0]
  north = bounds[3]
  east = bounds[2]

  return f"""
[out:json];
(
  way["highway"~"motorway|trunk|primary|secondary|tertiary"]({south},{west},{north},{east});
);
out geom;
"""

def download_osm_roads(query):
  url = "https://overpass-api.de/api/interpreter"
  data = urllib.parse.urlencode({"data": query}).encode("utf-8")
  request = urllib.request.Request(
    url,
    data=data,
    headers={"User-Agent": "team-9-workadventure-inselszenario"}
  )

  with urllib.request.urlopen(request) as response:
    return json.load(response)

def lonlat_to_pixel(lon, lat, bounds):
  min_lon, min_lat, max_lon, max_lat = bounds
  canvas_width = mapWidth * 8
  canvas_height = mapHeight * 8
  x = int((lon - min_lon) / (max_lon - min_lon) * canvas_width)
  y = int((max_lat - lat) / (max_lat - min_lat) * canvas_height)
  x += 50
  y += 30
  return x, y

def roadStyle(road_type):
  if road_type in ["motorway", "trunk", "primary"]:
    return 6, "#d95f02"
  elif road_type in ["secondary", "tertiary"]:
    return 4, "#7570b3"
  else:
    return 2, "#666666"

def create_road_objects(osm_data, bounds):
  roads = []
  road_id = 1

  for element in osm_data["elements"]:
    if element.get("type") != "way":
      continue

    geometry = element.get("geometry", [])
    if len(geometry) < 2:
      continue

    tags = element.get("tags", {})
    road_name = tags.get("name", "OSM road")
    road_type = tags.get("highway", "road")
    road_width, road_color = roadStyle(road_type)

    polyline = []
    for point in geometry:
      x, y = lonlat_to_pixel(point["lon"], point["lat"], bounds)
      polyline.append({"x": x, "y": y})

    road = {
      "id": road_id,
      "name": road_name,
      "type": road_type,
      "x": 0,
      "y": 0,
      "lineWidth": road_width,
      "color": road_color,
      "polyline": polyline,
      "geometry": geometry
    }

    roads.append(road)
    road_id += 1

  return roads

def create_road_label_objects(roads):
  labels = []
  label_id = 1

  for road in roads:
    name = road.get("name", "")

    if name == "" or name == "OSM road":
      continue

    polyline = road.get("polyline", [])

    if len(polyline) == 0:
      continue

    middle_index = len(polyline) // 2
    middle_point = polyline[middle_index]

    labels.append({
      "id": label_id,
      "name": name + " Label",
      "type": "text",
      "x": middle_point["x"],
      "y": middle_point["y"],
      "text": name
    })

    label_id += 1

  return labels

def island(data, start, places=None, roads=None, roadLabels=None):
  if places is None:
    places = []
  if roads is None:
    roads = []
  if roadLabels is None:
    roadLabels = []
  if roadLabels is None:
    roadLabels = create_road_label_objects(roads)

  return {
    "compressionlevel":-1,
    "version":1.4,
    "type":"map",
    "width":mapWidth,
    "height":mapHeight,
    "infinite":False,
    "orientation":"orthogonal",
    "renderorder":"right-down",
    "tilewidth":tileSize,
    "tileheight":tileSize,
    "tilesets":[{
      "columns":4,
      "firstgid":1,
      "image":"beachline.png",
      "imageheight":512,
      "imagewidth":128,
      "margin":0,
      "name":"Beachline",
      "spacing":0,
      "tilecount":62,
      "tileheight":tileSize,
      "tilewidth":tileSize,
      "tiles":[{
        "id":0,
        "properties":[{
          "name":"collides",
          "type":"bool",
          "value":True
        }]
      }]
    }],
    "layers": [
      # exitLayer("exit", 2, 1, [], exit),
      # linkLayer("link", 3, 1, (), "https:\/\/hlg.github.io\/wamap\/caleidoscope\/index.html"),
      # imageLayer("image", 4, "..\/..\/Downloads\/Ruegen2.png", visible=False), 
      tileLayer("start", 1, start),
      tileLayer("tiles", 2, data),
      objectLayer("floorLayer", 4, []),
      objectLayer("places", 5, places),
      objectLayer("roads", 6, roads),

      objectLayer("roadLabels", 8, roadLabels, visible=False),

      objectLayer("placeLabels", 7, createPlaceLabels(places))
    ]
  }

if __name__ == "__main__":
  import json
  import sys

  bounds = get_bounds_from_geojson("osm-ruegen.geojson")
  query = create_overpass_query(bounds)
  osm_data = download_osm_roads(query)
  roads = create_road_objects(osm_data, bounds)
  roadLabels = create_road_label_objects(roads)  
  print(len(roads))
  
  dataFile = len(sys.argv)>1 and sys.argv[1] or "island-data-1434381.json"
  with open(dataFile) as dataJson:
    data = json.load(dataJson)
    index = [d+1 for d in data["index"]]
  mapWidth = data["width"]
  mapHeight = data["height"]
  start = [2 if d1==2 and d2>2  else 0 for (d1,d2) in zip(index[:-1],index[1:])] + [0]
  tiled = island(index, start, roads=roads)
  with open(dataFile.replace('data', 'map'),'w') as f:
    json.dump(tiled, f, indent=4)

