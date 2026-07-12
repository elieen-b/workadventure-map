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

  for place in places:
    if not place.get("name"):
      continue

    labels.append({
      "id": label_id,
      "name": place["name"] + " Label",
      "type": "",
      "x": place["x"] + 8,
      "y": place["y"] - 8,
      "width": 200,
      "height": 20,
      "rotation": 0,
      "visible": True,
      "text": {
        "text": place["name"],
        "pixelsize": 16,
        "color": "#000000",
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