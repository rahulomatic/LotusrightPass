def project_to_meters(gdf):
    """
    Converts WGS84 → Web Mercator (meters)
    Required for accurate distance calculations
    """
    return gdf.to_crs(epsg=3857)