def lonlat_to_pixel(lon, lat, bounds, width, height, tile_size):
    min_lon, min_lat, max_lon, max_lat = bounds

    x = int(
        (lon - min_lon)
        / (max_lon - min_lon)
        * width
        * tile_size
    )

    y = int(
        (max_lat - lat)
        / (max_lat - min_lat)
        * height
        * tile_size
    )

    return x, y