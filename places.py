import urllib.parse


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
  used_positions = []

  priority = {
    "city": 1,
    "town": 2,
    "village": 3,
    "suburb": 4,
    "hamlet": 5,
    "neighbourhood": 6
  }

  sorted_places = sorted(
    places,
    key=lambda place: priority.get(place.get("type"), 99)
  )

  for place in sorted_places:
    name = place.get("name")
    place_type = place.get("type", "").lower()

    if not name:
      continue

    if place_type not in [
      "city",
      "town",
      "village",
      "suburb",
      "hamlet",
      "neighbourhood"
    ]:
      continue

    x = place["x"]
    y = place["y"]

    if place_type == "city":
      minimum_distance = 120
      pixel_size = 38
      marker_size = 32
      marker_color = "#d7191c"
      text_color = "#9b111e"
      offset_x = 25
      offset_y = -16

    elif place_type == "town":
      minimum_distance = 95
      pixel_size = 32
      marker_size = 28
      marker_color = "#ff8c00"
      text_color = "#b34700"
      offset_x = 22
      offset_y = -14

    elif place_type == "village":
      minimum_distance = 70
      pixel_size = 26
      marker_size = 23
      marker_color = "#ffd43b"
      text_color = "#222222"
      offset_x = 20
      offset_y = -12

    elif place_type == "suburb":
      minimum_distance = 55
      pixel_size = 22
      marker_size = 19
      marker_color = "#7b61ff"
      text_color = "#3f2f7f"
      offset_x = 17
      offset_y = -10

    else:
      minimum_distance = 45
      pixel_size = 20
      marker_size = 15
      marker_color = "#2ca25f"
      text_color = "#1f5132"
      offset_x = 15
      offset_y = -9

    too_close = False

    for old_x, old_y in used_positions:
      dx = old_x - x
      dy = old_y - y

      if (dx * dx + dy * dy) ** 0.5 < minimum_distance:
        too_close = True
        break

    if too_close:
      continue

    used_positions.append((x, y))

    labels.append({
      "id": label_id,
      "name": name + " Marker",
      "type": place_type,
      "x": x - marker_size / 2,
      "y": y - marker_size / 2,
      "width": marker_size,
      "height": marker_size,
      "rotation": 0,
      "visible": True,
      "text": {
        "text": "●",
        "pixelsize": marker_size,
        "color": marker_color,
        "bold": True,
        "wrap": False
      }
    })

    label_id += 1

    labels.append({
      "id": label_id,
      "name": name + " Label",
      "type": place_type,
      "x": x + offset_x,
      "y": y + offset_y,
      "width": 320,
      "height": 45,
      "rotation": 0,
      "visible": True,
      "text": {
        "text": name,
        "pixelsize": pixel_size,
        "color": text_color,
        "bold": True,
        "wrap": False
      }
    })

    label_id += 1

  return labels


def createWikipediaAreas(places):
  areas = []
  area_id = 1

  for place in places:
    name = place.get("name", "")

    if not name:
      continue

    wikipedia_name = urllib.parse.quote(
      name.replace(" ", "_")
    )

    wikipedia_url = (
      "https://de.wikipedia.org/wiki/"
      + wikipedia_name
    )

    areas.append({
      "id": area_id,
      "name": name + " Wikipedia",
      "type": "area",
      "class": "area",
      "x": place["x"] - 32,
      "y": place["y"] - 32,
      "width": 64,
      "height": 64,
      "rotation": 0,
      "visible": True,
      "properties": [
        {
          "name": "openWebsite",
          "type": "string",
          "value": wikipedia_url
        },
        {
          "name": "openWebsiteTrigger",
          "type": "string",
          "value": "onaction"
        },
        {
          "name": "openWebsiteTriggerMessage",
          "type": "string",
          "value": "Leertaste drücken, um Wikipedia zu öffnen"
        },
        {
          "name": "openWebsiteClosable",
          "type": "bool",
          "value": True
        }
      ]
    })

    area_id += 1

  return areas