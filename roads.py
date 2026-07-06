import json
import urllib.request
import urllib.parse

mapWidth = 73
mapHeight = 89

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

