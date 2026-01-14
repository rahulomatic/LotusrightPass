import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def load_population(csv_path):
    df = pd.read_csv(csv_path)
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )
    return gdf

def load_hospitals(csv_path):
    df = pd.read_csv(csv_path)
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )
    return gdf