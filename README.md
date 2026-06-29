These Python scripts generate maps for [Workadventurei](https://workadventu.re) from [OpenStreetMap](https://openstreetmap.org) island polygons.
## Projekt einrichten
Für das Projekt wird Python 3 verwendet.
```bash
python3 --version
```
Virtuelle Umgebung erstellen:
```bash
python3 -m venv venv
```
Virtuelle Umgebung aktivieren:
```bash
source venv/bin/activate
```
Pakete installieren:
```bash
pip install -r requirements.txt
```
Der Ordner `venv/` wird über `.gitignore` nicht in GitLab hochgeladen.
 
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


## Sprint 1 – Umgesetzte Funktionen

### US-01: Inselkarte aus OpenStreetMap erzeugen

Mit dem Skript tile.py kann aus einer OpenStreetMap-Relation eine WorkAdventure-kompatible Karte erzeugt werden.

Beispiel:

bash python tile.py --polygon 3403603 --output JSON 

Das Skript führt folgende Schritte aus:

1. Herunterladen der Inselgeometrie von OpenStreetMap.
2. Skalierung der Koordinaten auf eine feste Tile-Größe.
3. Erzeugung eines Tile-Indexes für Wasser, Land und Küstenlinien.
4. Erzeugung einer JSON-Datei für Tiled und WorkAdventure.
5. Erzeugung einer Vorschaukarte als PNG.

Ergebnis:

- island-data-1434381.json
- island-map-1434381.json
- map.png

---

### US-02: Karte im Browser anzeigen

Die erzeugte JSON-Datei kann lokal im Browser dargestellt werden.

Webserver starten:

bash python3 -m http.server 8080 

Browser öffnen:

text http://localhost:8080/index.html 

Die Karte wird auf einem HTML5-Canvas dargestellt.

Farben:

- Blau = Wasser
- Grün = Land
- Braun = Küstenlinie

Standardmäßig wird beim Start die Datei ruegen-map.json geladen.

---

### US-03: Beliebige JSON-Datei auswählen

Zusätzlich wurde eine Dateiauswahl implementiert.

Der Benutzer kann über den Button „Datei auswählen“ eine beliebige JSON-Karte laden.

Getestete Karten:

- Rügen
- Bali
- Amrum
- sylt

Bei ungültigen Dateien wird eine Fehlermeldung angezeigt.

---

### US-04: Deployment und Nutzung dokumentieren

Ziel dieser User Story war die Dokumentation der notwendigen Schritte zum Starten und Testen der Anwendung.

#### Lokalen Webserver starten

Im Projektordner:

bash python3 -m http.server 8080 

#### Browser öffnen

text http://localhost:8080/index.html 

Dadurch wird die Browseransicht der Karte geladen.

#### WorkAdventure verwenden

Die erzeugten Karten können zusätzlich über GitHub Pages veröffentlicht und anschließend in WorkAdventure geladen werden.

#### Durchgeführte Tests

- Lokaler Webserver startet erfolgreich.
- Browseransicht wird geladen.
- JSON Dateien können ausgewählt werden.
- Karte wird korrekt dargestellt.
- WorkAdventure kann die veröffentlichte Karte laden.

#### Ergebnis

Die Anwendung kann anhand der Dokumentation von einer anderen Person gestartet und getestet werden, ohne den Quellcode verändern zu müssen.

---

### US-05: Karte in WorkAdventure anzeigen

Die erzeugten Karten wurden über GitHub Pages veröffentlicht.

Beispiel einer Karten-URL:

text https://elieen-b.github.io/workadventure-map/island-map-1434381.json 

Für WorkAdventure wird die Karten-URL in einen WorkAdventure-Link eingebettet:

text https://play.workadventu.re/_/global/elieen-b.github.io/workadventure-map/island-map-1434381.json 

Dadurch kann die Karte direkt in WorkAdventure geladen werden.

Getestet mit:

- Rügen
- Bali
- Amrum
- sylt

---


### US-06: Punktförmige Orte als Object Layer speichern

Für US-06 wurde die erzeugte WorkAdventure-JSON um einen Object Layer erweitert.

Der neue Layer heißt `places` und speichert Orte als Objekte.

Beispiel:

```json

{

  "name": "Bergen",

  "type": "village",

  "x": 500,

  "y": 500,

  "point": true

}
```
---

### US-07: Punkte im Browser anzeigen

Für US-07 wurde die Browseranzeige erweitert.

Die Anwendung sucht in der geladenen JSON-Datei nach einem Layer mit dem Namen `places`. Aus diesem Layer werden die gespeicherten Orte ausgelesen und anschließend auf der Karte dargestellt.

Die Darstellung erfolgt als:

- roter Punkt für den Ort
- Ortsname als Beschriftung neben dem Punkt

Die Umsetzung erfolgt in `index.html`.

Getestet wurde mit den Beispielorten:
- Bergen
- Sassnitz

Durchgeführter Test:
1. Lokalen Webserver starten
```bash
python3 -m http.server 8080
```
---

### US-08: Straßen / Wege als Linien speichern

Für US-08 wurde die erzeugte Karten-Datei um einen weiteren Object Layer erweitert.
Der neue Layer heißt roads. In diesem Layer werden Straßen bzw. Wege als Linien gespeichert.
Eine Linie besteht aus mehreren Koordinatenpunkten. Diese Punkte werden später verbunden und ergeben dadurch einen Weg oder eine Straße.

Beispiel:
```json
{
  "id": 1,
  "name": "Beispielweg 1",
  "type": "road",
  "x": 0,
  "y": 0,
  "polyline": [
    { "x": 100, "y": 100 },
    { "x": 200, "y": 140 },
    { "x": 300, "y": 180 }
  ]
}
```

Zusätzlich wurde ein zweiter Beispielweg gespeichert:
```json
{
  "id": 2,
  "name": "Beispielweg 2",
  "type": "path",
  "x": 0,
  "y": 0,
  "polyline": [
    { "x": 400, "y": 300 },
    { "x": 500, "y": 350 },
    { "x": 600, "y": 320 }
  ]
}
```
Die Umsetzung erfolgt in wamap.py. Beim Ausführen von python3 wamap.py wird die Datei island-map-1434381.json neu erzeugt und enthält danach den Layer roads.
Durchgeführte Tests:
1. Karte neu erzeugen

python3 wamap.py

2. Prüfen, ob der Roads-Layer vorhanden ist
grep roads island-map-1434381.json

3. Prüfen, ob Linienobjekte gespeichert wurden
grep polyline island-map-1434381.json

Ergebnis:

* Der Object Layer roads wird erzeugt.
* Zwei Beispielwege werden als Polyline-Objekte gespeichert.
* Die Linieninformationen sind in der JSON-Datei vorhanden.
* Die JSON-Datei bleibt gültig.
* Die Daten können in US-09 im Browser dargestellt werden.

!!! Die Straßenkoordinaten wurden für Sprint 2 als Beispielwerte gesetzt. Eine automatische Übernahme echter Straßen aus OpenStreetMap ist noch nicht umgesetzt.

---

### US-09: Straßen im Browser anzeigen

In US-09 werden die in US-08 gespeicherten Straßen und Wege im Browser sichtbar dargestellt.
Die Straßen liegen in der JSON-Datei im Object Layer `roads`.
Jede Straße enthält eine `polyline`.  
Eine `polyline` besteht aus mehreren Punkten mit `x`- und `y`-Koordinaten.

Beispiel:

```json
{
  "name": "Beispielweg 1",
  "type": "road",
  "polyline": [
    { "x": 100, "y": 100 },
    { "x": 200, "y": 140 },
    { "x": 300, "y": 180 }
  ]
}
```
In der Browseransicht wird der Layer roads ausgelesen.
Der erste Punkt der polyline wird als Startpunkt verwendet.
Alle weiteren Punkte werden mit Linien verbunden.

Dadurch werden Straßen und Wege als schwarze Linien auf der Karte angezeigt.

für den Test

1. Lokalen Webserver starten:

python3 -m http.server 8080

2. Browser öffnen:

http://localhost:8080/index.html

3. Datei island-map-1434381.json auswählen.

Erwartetes Ergebnis

* Die Karte wird angezeigt.
* Die Orte aus dem Layer places werden angezeigt.
* Die Straßen aus dem Layer roads werden als schwarze Linien angezeigt.



## Sprint 2 – Umgesetzte Funktionen

In Sprint 2 wurde die erzeugte Inselkarte erweitert.
Neben Land, Wasser und Küste werden jetzt auch Orte, Straßen, Ortsnamen, Straßennamen und Kategorien aus OpenStreetMap verarbeitet.

```md
Getestet wurde hauptsächlich mit der Datei:
`selectedIslands/Ruegen-map.json`.
```
Die Daten stammen aus OpenStreetMap und werden beim Erzeugen der Karte automatisch in die JSON-Datei geschrieben.


## US-06: Punktförmige Orte als Object Layer speichern

Die Grundfunktion für punktförmige Orte wurde bereits in Sprint 1 umgesetzt.

In Sprint 2 wurde die Funktion erweitert. Statt Beispielwerten werden nun echte Ortsdaten aus OpenStreetMap übernommen und als Punktobjekte in der erzeugten WorkAdventure-/Tiled-JSON-Datei gespeichert.

# Layer

Der Layer heißt: `places`
```
In diesem Layer werden Orte aus OpenStreetMap als Punktobjekte gespeichert.

Beispiel aus der Datei

Datei:
```json
selectedIslands/Ruegen-map.json
```
```json
{
  "id": 1,
  "name": "Bergen auf Rügen",
  "type": "town",
  "x": 1426,
  "y": 2085,
  "width": 22,
  "height": 22,
  "size": 22,
  "color": "red",
  "point": true
}
```
Durchgeführte Tests


### Test 1: Prüfen, ob der Layer vorhanden ist

```python
python3 - <<'PY'
import json
with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)
layer = next((l for l in m["layers"] if l["name"] == "places"), None)
print("places Layer vorhanden:", layer is not None)
print("Anzahl Orte:", len(layer["objects"]))
PY
```
Ergebnis:
```python
places Layer vorhanden: True
Anzahl Orte: 497
```

Test 2: Prüfen, ob Ortsdaten gespeichert wurden
```json
python3 - <<'PY'
import json
with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)
places = next(l for l in m["layers"] if l["name"] == "places")["objects"]
print("Name:", places[0]["name"])
print("Typ:", places[0]["type"])
print("Point:", places[0]["point"])
PY
```

Ergebnis:
```json
Name: Bergen auf Rügen
Typ: town
Point: True
```

# Ergebnis

Der Layer places wurde erfolgreich erzeugt.

In der Datei Ruegen-map.json wurden insgesamt 497 Orte gespeichert.

Jeder Ort besitzt einen Namen, eine Ortskategorie sowie eine Position auf der Karte.

Die gespeicherten Ortsdaten können anschließend in US-07 grafisch dargestellt werden.

## US-07: Punkte im Browser anzeigen

Für US-07 wurde die Browseransicht in index.html erweitert.

Der Browser liest den Layer places aus der geladenen JSON-Datei aus und stellt die gespeicherten Orte auf der Karte dar.

Für die Darstellung werden folgende Informationen verwendet:

* x und y bestimmen die Position des Ortes auf der Karte.
* size bestimmt die Größe des dargestellten Punktes.
* color bestimmt die Farbe des Punktes.
* name wird als Ortsname neben dem Punkt angezeigt.

Die Ortsdaten stammen aus OpenStreetMap und werden aus dem Layer places der Datei selectedIslands/Ruegen-map.json gelesen.

Durchgeführter Test

Lokalen Webserver starten:

python3 -m http.server 8080

Browser öffnen:

http://localhost:8080/index.html

Anschließend die Datei auswählen:

selectedIslands/Ruegen-map.json

Ergebnis

Die Orte wurden erfolgreich aus dem Layer places geladen und auf der Karte dargestellt.
Die Positionen stimmen mit den gespeicherten Koordinaten überein.
Ortsnamen werden sichtbar angezeigt.

US-07 ist damit erfüllt.

# US-08: Straßen / Wege als Linien speichern

Die Grundfunktion für Straßen und Wege wurde bereits in Sprint 1 vorbereitet.

In Sprint 2 wurde die Funktion erweitert. Statt manuell eingetragener Beispielwege werden nun echte Straßen und Wege aus OpenStreetMap übernommen und in der erzeugten WorkAdventure-/Tiled-JSON-Datei gespeichert.

Für diese User Story wurde die Karten-Datei um einen zusätzlichen Object Layer erweitert.

Der Layer heißt:

```text
roads
```

In diesem Layer werden Straßen und Wege als Linienobjekte gespeichert.

Jede Straße besteht aus mehreren Punkten, die gemeinsam eine sogenannte Polyline bilden. Beim späteren Darstellen im Browser werden diese Punkte miteinander verbunden und ergeben den Verlauf der Straße.

Die Straßeninformationen stammen direkt aus OpenStreetMap.

Jede Straße enthält unter anderem:

* Straßenname
* Straßenkategorie
* Linienfarbe
* Linienbreite
* Verlauf der Straße als Polyline

Beispiel aus der Datei:

```text
selectedIslands/Ruegen-map.json
```

```json
{
  "id": 1,
  "name": "OSM road",
  "type": "secondary",
  "x": 0,
  "y": 0,
  "lineWidth": 4,
  "color": "#7570b3",
  "polyline": [
    { "x": 71, "y": 743 },
    { "x": 72, "y": 742 },
    { "x": 73, "y": 740 }
  ]
}
```

## Bedeutung der Attribute

* name enthält den Straßennamen aus OpenStreetMap.
* type enthält die Straßenkategorie.
* lineWidth bestimmt die Breite der Linie.
* color bestimmt die Farbe der Linie.
* polyline enthält die Punkte des Straßenverlaufs.

## Verwendete Straßenkategorien

* primary
* secondary
* tertiary
* road

Für die verschiedenen Kategorien werden unterschiedliche Farben und Linienbreiten gespeichert.

Beispiele:

* primary → lineWidth 6
* secondary → lineWidth 4
* tertiary → lineWidth 4

## Durchgeführte Tests

Prüfen, ob der Layer roads vorhanden ist:

```bash
python3 - <<'PY'
import json

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

layer = next((l for l in m["layers"] if l["name"] == "roads"), None)

print("roads Layer existiert:", layer is not None)
PY
```

Ergebnis:

```text
roads Layer existiert: True
```

Prüfen, wie viele Straßen gespeichert wurden:

```bash
python3 - <<'PY'
import json

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

roads = next(l for l in m["layers"] if l["name"] == "roads")

print("Anzahl Straßen:", len(roads["objects"]))
PY
```

Ergebnis:

```text
Anzahl Straßen: 1692
```

Prüfen, ob eine Polyline vorhanden ist:

```bash
python3 - <<'PY'
import json

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

roads = next(l for l in m["layers"] if l["name"] == "roads")

road = roads["objects"][0]

print("Polyline vorhanden:", "polyline" in road)
print("Punkte:", len(road["polyline"]))
PY
```

Ergebnis:

```text
Polyline vorhanden: True
Punkte: 13
```

Prüfen, ob Straßenname und Kategorie gespeichert wurden:

```bash
python3 - <<'PY'
import json

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

roads = next(l for l in m["layers"] if l["name"] == "roads")

road = roads["objects"][0]

print("Name:", road.get("name"))
print("Type:", road.get("type"))
PY
```

Ergebnis:

```text
Name: OSM road
Type: secondary
```

## Ergebnis

Der Layer `roads` wurde erfolgreich erzeugt.

In der Datei `Ruegen-map.json` wurden insgesamt 1692 Straßen und Wege gespeichert.

Jede Straße besitzt eine Kategorie, einen Verlauf als Polyline sowie Darstellungsinformationen wie Farbe und Linienbreite.

Die gespeicherten Straßendaten können anschließend in US-09 grafisch im Browser dargestellt werden.

# US-09: Straßen im Browser anzeigen

Für diese User Story wurde die Browseransicht erweitert.

Die Anwendung liest den Layer `roads` aus der geladenen JSON-Datei aus und stellt die gespeicherten Straßen auf der Karte dar.

Jede Straße enthält eine Polyline mit mehreren Punkten. Diese Punkte werden im Browser miteinander verbunden und ergeben den Verlauf der Straße.

Zusätzlich werden die in der JSON-Datei gespeicherten Darstellungsinformationen verwendet:

* Straßenkategorie
* Linienfarbe
* Linienbreite

Zur besseren Sichtbarkeit werden die Straßen mit einem dunklen Rand und einer helleren Innenlinie dargestellt.

Dadurch sind Straßen und Wege auf der Karte deutlich besser erkennbar.

## Durchgeführter Test

Lokalen Webserver starten:

```bash
python3 -m http.server 8080
```

Browser öffnen:

```text
http://localhost:8080/index.html
```

Anschließend die Datei auswählen:

```text
selectedIslands/Ruegen-map.json
```

## Ergebnis

* Die Inselkarte wird erfolgreich geladen.
* Die Orte aus dem Layer `places` werden angezeigt.
* Die Straßen aus dem Layer `roads` werden dargestellt.
* Die Polylines werden korrekt als Linien gezeichnet.
* Die Straßen sind auf der Karte deutlich sichtbar.

Die Darstellung der Straßen funktioniert damit erfolgreich.

US-09 ist damit erfüllt.


# US-10: Ortsnamen als Textlabel speichern

Für diese User Story wurde die erzeugte Karten-Datei um einen zusätzlichen Object Layer erweitert.

Der Layer heißt:

```text
placeLabels
```

In diesem Layer werden die Namen der Orte als Textobjekte gespeichert.

Für jeden Ort aus dem Layer `places` wird automatisch ein passendes Textlabel erzeugt.

Jedes Textlabel enthält unter anderem:

* Namen des Labels
* angezeigten Text
* Position auf der Karte

Beispiel aus der Datei:

```text
selectedIslands/Ruegen-map.json
```

```json
{
  "id": 1,
  "name": "Bergen auf Rügen Label",
  "type": "text",
  "x": 1434,
  "y": 2077,
  "text": "Bergen auf Rügen"
}
```

## Bedeutung der Attribute

* name enthält den Namen des Label-Objekts.
* type kennzeichnet das Objekt als Textobjekt.
* x und y speichern die Position des Labels auf der Karte.
* text enthält den anzuzeigenden Ortsnamen.

## Durchgeführte Tests

Prüfen, ob ein Ortslabel erzeugt wurde:

```text
Name: Bergen auf Rügen Label
Text: Bergen auf Rügen
X: 1434
Y: 2077
```

Prüfen, wie viele Ortslabels gespeichert wurden:

```text
Anzahl Labels: 497
```

## Ergebnis

Der Layer `placeLabels` wurde erfolgreich erzeugt.

Für jeden gespeicherten Ort wurde automatisch ein Textlabel angelegt.

In der Datei `Ruegen-map.json` wurden insgesamt 497 Ortslabels gespeichert.

Die gespeicherten Ortsnamen können anschließend in US-12 im Browser dargestellt werden.

US-10 ist damit erfüllt.

# US-11: Straßennamen als Textlabel speichern

Für diese User Story wurde die erzeugte Karten-Datei um einen zusätzlichen Object Layer erweitert.

Der Layer heißt:

```text
roadLabels
```

In diesem Layer werden Straßennamen als Textobjekte gespeichert.

Dabei werden nur Straßen berücksichtigt, für die in OpenStreetMap ein Name vorhanden ist.

Jedes Textlabel enthält unter anderem:

* Namen des Label-Objekts
* anzuzeigenden Text
* Position auf der Karte

Beispiel aus der Datei:

```text
selectedIslands/Ruegen-map.json
```

```json
{
  "id": 1,
  "name": "Circus Label",
  "type": "text",
  "x": 458,
  "y": 673,
  "text": "Circus"
}
```

## Bedeutung der Attribute

* name enthält den Namen des Label-Objekts.
* type kennzeichnet das Objekt als Textobjekt.
* x und y speichern die Position des Labels.
* text enthält den anzuzeigenden Straßennamen.

## Durchgeführte Tests

Prüfen, ob der Layer vorhanden ist:

```text
roadLabels Layer existiert: True
```

Prüfen, wie viele Straßennamen gespeichert wurden:

```text
Anzahl roadLabels: 702
```

Prüfen eines einzelnen Labels:

```text
Name: Circus Label
Type: text
Text: Circus
X: 458
Y: 673
```

Prüfen mehrerer verschiedener Straßennamen:

```text
Circus
Alleestraße
Bahnhofstraße
Dorfstraße
Bergerlandstraße
Putbuser Chaussee
Lauterbacher Straße
Putbuser Straße
Bergener Straße
```

## Ergebnis

Der Layer `roadLabels` wurde erfolgreich erzeugt.

In der Datei `Ruegen-map.json` wurden insgesamt 702 Straßennamen gespeichert.

Für alle Straßen mit vorhandenem Namen wurde automatisch ein Textlabel angelegt.

Die gespeicherten Straßennamen können anschließend in US-12 im Browser dargestellt werden.

US-11 ist damit erfüllt.

# US-12: Namen im Viewer anzeigen

Für diese User Story wurde die Browseransicht erweitert.

Der Viewer liest nun zusätzlich die Textobjekte aus den Layern

```text
placeLabels
roadLabels
```

aus und stellt diese auf der Karte dar.

Dadurch werden sowohl Ortsnamen als auch Straßennamen direkt im Browser angezeigt.

Um die Lesbarkeit der Karte zu verbessern, werden sehr lange Namen sowie übermäßig viele Straßennamen gefiltert. Dadurch bleibt die Darstellung auch bei größeren Karten übersichtlich.

Zusätzlich wird geprüft, ob ein Textobjekt tatsächlich einen Inhalt besitzt. Leere Texte werden übersprungen und verursachen keine Fehler.

## Durchgeführter Test

Lokalen Webserver starten:

```bash
python3 -m http.server 8080
```

Browser öffnen:

```text
http://localhost:8080/index.html
```

Anschließend die Datei auswählen:

```text
selectedIslands/Ruegen-map.json
```

## Geprüfte Funktionen

* Ortsnamen werden angezeigt.
* Straßennamen werden angezeigt.
* Leere Textobjekte verursachen keine Fehler.
* Die Karte bleibt trotz vieler Namen lesbar.

## Ergebnis

Die Textobjekte aus den Layern `placeLabels` und `roadLabels` werden erfolgreich geladen und dargestellt.

Ortsnamen und Straßennamen sind direkt auf der Karte sichtbar.

Die Filterung sorgt dafür, dass die Karte trotz vieler Beschriftungen übersichtlich bleibt.

US-12 ist damit erfüllt.

## US-13: Ortsgrößen unterschiedlich darstellen

Für US-13 werden Orte je nach OpenStreetMap-Kategorie unterschiedlich dargestellt.

Die Kategorie eines Ortes steht im JSON im Feld `type`.

Beispiele für Ortskategorien sind:

- `town`
- `village`
- `hamlet`
- `locality`

Für die Darstellung wurde eine einfache Regel festgelegt:

| Kategorie | Größe | Farbe |
|----------|-------|-------|
| town | 22 | red |
| village | 16 | orange |
| hamlet | 10 | yellow |
| andere / unbekannt | 14 | orange |

Diese Werte werden direkt im JSON-Objekt gespeichert.

Beispiel aus `selectedIslands/Ruegen-map.json`:

```json
{
  "id": 1,
  "name": "Bergen auf R\u00fcgen",
  "type": "town",
  "x": 1426,
  "y": 2085,
  "width": 22,
  "height": 22,
  "size": 22,
  "color": "red",
  "point": true
}
```

## Durchgeführte Tests

### Test 1: Prüfen, welche Ortskategorien gespeichert wurden

```bash

python3 - <<'PY'
import json
from collections import Counter

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

places = next(l for l in m["layers"] if l["name"] == "places")["objects"]

types = Counter(p.get("type", "KEIN_TYPE") for p in places)

print("Ortskategorien:")
for t, c in types.most_common():
    print(t, c)
PY

```

Ergebnis:

```text

Ortskategorien:
hamlet 308
locality 60
village 56
isolated_dwelling 39
neighbourhood 25
town 4
suburb 4
region 1

```
Damit wurde geprüft, welche Ortskategorien in den OpenStreetMap-Daten von Rügen vorhanden sind.

### Test 2: Prüfen, ob die Ortsgrößen und Farben je nach Kategorie richtig gespeichert werden

Folgender Test wurde ausgeführt:

```bash

python3 - <<'PY'

import json
with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)
places = next(l for l in m["layers"] if l["name"] == "places")["objects"]
wanted = ["village", "town", "city", "hamlet"]
for w in wanted:
    print("\nKategorie:", w)
    count = 0
    for p in places:
        if p.get("type") == w:
            print(p.get("name"), "size=", p.get("size"), "color=", p.get("color"))
            count += 1
            if count == 5:
                break

PY

```

Ergebnis:

```text

Kategorie: village
Samtens size=16 color=orange
Kasnevitz size=16 color=orange
Dreschvitz size=16 color=orange
Putgarten size=16 color=orange
Lancken size=16 color=orange

Kategorie: town
Bergen auf Rügen size=22 color=red
Putbus size=22 color=red
Garz/Rügen size=22 color=red
Sassnitz size=22 color=red

Kategorie: city

Kategorie: hamlet
Neukamp size=10 color=yellow
Ketelshagen size=10 color=yellow
Dumsevitz size=10 color=yellow
Posewald size=10 color=yellow
Wreechen size=10 color=yellow

```

Dabei wurde geprüft,

- ob verschiedene Ortskategorien vorhanden sind,
- ob für jede Kategorie die richtige Größe gespeichert wurde,
- ob für jede Kategorie die richtige Farbe gespeichert wurde.

Auf Rügen wurde keine Ortskategorie **city** gefunden. Die Regel für diese Kategorie ist trotzdem im Code vorhanden und kann bei anderen Karten verwendet werden.

## Ergebnis

Die Orte werden abhängig von ihrer OpenStreetMap-Kategorie unterschiedlich dargestellt.
Größere Orte erhalten größere Symbole und kleinere Orte kleinere Symbole. Zusätzlich wird für jede Kategorie eine passende Farbe gespeichert.
Dadurch können wichtige Orte auf der Karte schneller erkannt werden.

US-13 ist damit erfüllt.

## US-14: Straßenkategorien unterschiedlich darstellen

Für US-14 werden Straßen je nach OpenStreetMap-Kategorie unterschiedlich dargestellt.

Die Straßenkategorie steht im JSON im Feld `type`.

Beispiele für Straßenkategorien sind:

- `primary`
- `secondary`
- `tertiary`
- `trunk`

Für die Darstellung werden zusätzlich folgende Informationen gespeichert:

- `lineWidth`
- `color`

Für die verschiedenen Straßenkategorien wurde folgende Regel festgelegt:

| Kategorie | Linienbreite | Farbe |
|----------|-------------|---------|
| primary / trunk | 6 | #d95f02 |
| secondary / tertiary | 4 | #7570b3 |
| andere / unbekannt | 2 | #666666 |

Diese Werte werden direkt im JSON-Objekt gespeichert.

Beispiel aus `selectedIslands/Ruegen-map.json`:

```json
{
  "id": 1,
  "name": "OSM road",
  "type": "secondary",
  "x": 0,
  "y": 0,
  "lineWidth": 4,
  "color": "#7570b3",
  "polyline": [
    { "x": 71, "y": 743 },
    { "x": 72, "y": 742 },
    { "x": 73, "y": 740 }
  ]
}
```

## Durchgeführte Tests

### Test 1: Prüfen, welche Straßenkategorien gespeichert wurden

```bash
python3 - <<'PY'
import json
from collections import Counter

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

roads = next(l for l in m["layers"] if l["name"] == "roads")["objects"]

types = Counter(r.get("type", "KEIN_TYPE") for r in roads)

print("Straßenkategorien:")
for t, c in types.most_common():
    print(t, c)
PY
```

Ergebnis:

```text
Straßenkategorien:
secondary 867
tertiary 358
primary 298
trunk 98
trunk_link 60
secondary_link 8
tertiary_link 3
```

Damit wurde geprüft, welche Straßenkategorien in den OpenStreetMap-Daten von Rügen vorhanden sind.

### Test 2: Prüfen, ob für verschiedene Straßenkategorien die richtige Linienbreite und Farbe gespeichert wurden

```bash
python3 - <<'PY'
import json

with open("selectedIslands/Ruegen-map.json") as f:
    m = json.load(f)

roads = next(l for l in m["layers"] if l["name"] == "roads")["objects"]

wanted = ["primary", "secondary", "tertiary"]

for w in wanted:
    print("\nKategorie:", w)
    count = 0
    for r in roads:
        if r.get("type") == w:
            print(r.get("name"), "lineWidth=", r.get("lineWidth"), "color=", r.get("color"))
            count += 1
            if count == 5:
                break
PY
```

Ergebnis:

```text
Kategorie: primary
OSM road lineWidth=6 color=#d95f02
Göhrener Chaussee lineWidth=6 color=#d95f02
OSM road lineWidth=6 color=#d95f02
OSM road lineWidth=6 color=#d95f02
Nordstraße lineWidth=6 color=#d95f02

Kategorie: secondary
OSM road lineWidth=4 color=#7570b3
Circus lineWidth=4 color=#7570b3
OSM road lineWidth=4 color=#7570b3
Alleestraße lineWidth=4 color=#7570b3
Bahnhofstraße lineWidth=4 color=#7570b3

Kategorie: tertiary
Lauterbacher Straße lineWidth=4 color=#7570b3
OSM road lineWidth=4 color=#7570b3
Boddenstraße lineWidth=4 color=#7570b3
OSM road lineWidth=4 color=#7570b3
Tilzower Weg lineWidth=4 color=#7570b3
```

Dabei wurde geprüft:

- ob verschiedene Straßenkategorien vorhanden sind,
- ob für jede Kategorie die richtige Linienbreite gespeichert wurde,
- ob für jede Kategorie die richtige Farbe gespeichert wurde.

Alle Straßen besitzen eine Straßenkategorie. Die Standardregel für unbekannte Kategorien ist trotzdem im Code vorhanden und kann bei anderen Karten verwendet werden.

## Ergebnis

Die Straßen werden abhängig von ihrer OpenStreetMap-Kategorie unterschiedlich dargestellt.

Hauptstraßen erhalten eine größere Linienbreite als kleinere Straßen. Zusätzlich wird für jede Straßenkategorie eine passende Farbe gespeichert.

Dadurch können verschiedene Straßentypen auf der Karte leichter unterschieden werden.

US-14 ist damit erfüllt.