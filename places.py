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