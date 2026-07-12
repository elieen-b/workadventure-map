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
    "village": 3
  }

  sorted_places = sorted(
    places,
    key=lambda place: priority.get(place.get("type"), 99)
  )

  for place in sorted_places:
    name = place.get("name")
    place_type = place.get("type")

    if not name:
      continue

    if place_type not in ["city", "town", "village"]:
      continue

    x = place["x"]
    y = place["y"]

    minimum_distance = 180

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

    if place_type == "city":
      pixel_size = 20
      text_color = "#8b0000"
      offset_x = 18
      offset_y = -18

    elif place_type == "town":
      pixel_size = 18
      text_color = "#b34700"
      offset_x = 16
      offset_y = -16

    else:
      pixel_size = 15
      text_color = "#1d1d1d"
      offset_x = 14
      offset_y = -14

    labels.append({
      "id": label_id,
      "name": name + " Label",
      "type": "",
      "x": x + offset_x,
      "y": y + offset_y,
      "width": 250,
      "height": 30,
      "rotation": 0,
      "visible": True,
      "text": {
        "text": name,
        "pixelsize": pixel_size,
        "color": text_color,
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