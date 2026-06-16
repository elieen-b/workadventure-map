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


## US-06: Punktförmige Orte als Object Layer speichern

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

## US-07: Punkte im Browser anzeigen

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

## US-08: Straßen / Wege als Linien speichern

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
