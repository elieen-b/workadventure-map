from PIL import Image, ImageDraw


def create_road_tileset(
    roads_data,
    map_width,
    map_height,
    tile_size=32,
    source_coordinate_size=8,
    output_file="roads-tileset.png"
):
    """
    Erzeugt ein transparentes Tileset mit den Straßen.

    Die Straßenkoordinaten wurden bisher für eine 8-Pixel-Darstellung
    berechnet. Für WorkAdventure werden sie auf 32 Pixel hochskaliert.
    """

    image_width = map_width * tile_size
    image_height = map_height * tile_size

    image = Image.new(
        "RGBA",
        (image_width, image_height),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(image)

    scale = tile_size / source_coordinate_size

    for road in roads_data:
        polyline = road.get("polyline", [])

        if len(polyline) < 2:
            continue

        points = [
            (
                int(point["x"] * scale),
                int(point["y"] * scale)
            )
            for point in polyline
        ]

        road_type = road.get("type", "road")

        outer_width = 12
        inner_width = 7
        inner_color = "#f7f3e8"

        if road_type in ("motorway", "trunk"):
            outer_width = 18
            inner_width = 12
            inner_color = "#f6b26b"

        elif road_type == "primary":
            outer_width = 16
            inner_width = 10
            inner_color = "#ffd966"

        elif road_type == "secondary":
            outer_width = 14
            inner_width = 8
            inner_color = "#fff2cc"

        elif road_type == "tertiary":
            outer_width = 12
            inner_width = 7
            inner_color = "#f7f3e8"

        # Dunkler Straßenrand
        draw.line(
            points,
            fill="#6b6255",
            width=outer_width,
            joint="curve"
        )

        # Helle Straßenfläche
        draw.line(
            points,
            fill=inner_color,
            width=inner_width,
            joint="curve"
        )

    image.save(output_file)

    first_gid = 63

    tile_data = [
        first_gid + index
        for index in range(map_width * map_height)
    ]

    tileset = {
        "columns": map_width,
        "firstgid": first_gid,
        "image": output_file,
        "imageheight": image_height,
        "imagewidth": image_width,
        "margin": 0,
        "name": "Roads",
        "spacing": 0,
        "tilecount": map_width * map_height,
        "tileheight": tile_size,
        "tilewidth": tile_size
    }

    return tileset, tile_data