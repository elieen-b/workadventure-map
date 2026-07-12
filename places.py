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

    minimum_distance = 80

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
      pixel_size = 28
      text_color = "#c62828"
      marker_color = "#d7191c"
      offset_x = 22
      offset_y = -14

    elif place_type == "town":
      pixel_size = 24
      text_color = "#c45100"
      marker_color = "#ff8c00"
      offset_x = 20
      offset_y = -12

    else:
      pixel_size = 20
      text_color = "#202020"
      marker_color = "#f2c94c"
      offset_x = 18
      offset_y = -12

    labels.append({
      "id": label_id,
      "name": name + " Marker",

      "type": "",

      "x": x - 7,

      "y": y - 15,

      "width": 24,

      "height": 24,

      "rotation": 0,

      "visible": True,

      "text": {

        "text": "●",

        "pixelsize": 18,

        "color": marker_color,

        "bold": True,

        "wrap": False

      }

    })

    label_id += 1

    # Ortsname

    labels.append({
      "id": label_id,
      "name": name + " Marker",
      "type": "",
      "x": x - 7,
      "y": y - 15,
      "width": 24,
      "height": 24,
      "rotation": 0,
      "visible": True,
      "text": {
        "text": "●",
        "pixelsize": 18,
        "color": marker_color,
        "bold": True,
        "wrap": False
      }
    })
    label_id += 1

    # Ortsname
    labels.append({
      "id": label_id,
      "name": name + " Label",
      "type": "",
      "x": x + offset_x,
      "y": y + offset_y,
      "width": 300,
      "height": 40,
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