import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

# Get project root safely
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

RAW_DIR = os.path.join(BASE_DIR, "backend", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "backend", "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

# -------- Population --------
pop_df = pd.read_csv(os.path.join(RAW_DIR, "population.csv"))

pop_gdf = gpd.GeoDataFrame(
    pop_df,
    geometry=gpd.points_from_xy(
        pop_df.longitude,
        pop_df.latitude
    ),
    crs="EPSG:4326"
)

pop_gdf.to_file(
    os.path.join(PROCESSED_DIR, "population.geojson"),
    driver="GeoJSON"
)

# -------- Hospitals --------
hosp_df = pd.read_csv(os.path.join(RAW_DIR, "hospitals.csv"))

hosp_gdf = gpd.GeoDataFrame(
    hosp_df,
    geometry=gpd.points_from_xy(
        hosp_df.longitude,
        hosp_df.latitude
    ),
    crs="EPSG:4326"
)

hosp_gdf.to_file(
    os.path.join(PROCESSED_DIR, "hospitals.geojson"),
    driver="GeoJSON"
)

print("✅ Milestone 1 preprocessing completed")