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