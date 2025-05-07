import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

gdf = gpd.read_file("C:/Users/HajduPe/OneDrive - Helsingin Seudun liikenne - Kuntayhtymä/Aluejako/sij2023/sijoittelualueet2023_raasepori_korjattu.shp")
gdf["geometry"] = gdf["geometry"].centroid
gdf["helmet_id"] = gdf["SIJ2023"].rank().sub(1).astype(int)
gdf["izone"] = gdf["helmet_id"]+1
gdf["jzone"] = gdf["helmet_id"]+1
print(gdf.sort_values("helmet_id"))
df = pd.read_csv("C:/Users/HajduPe/OneDrive - Helsingin Seudun liikenne - Kuntayhtymä/Estimointi/HBO_pitkat_jkl_matkat.txt", sep=" ", names=["izone","jzone","cost"])
df = pd.merge(df,gdf, how="left", left_on=['izone'], right_on=['izone'])
df = pd.merge(df,gdf, how="left", left_on=['jzone_x'], right_on=['jzone'])
#df = df.join(gdf,"izone","left",lsuffix="",rsuffix="iz")
#df = df.join(gdf,"jzone","right",lsuffix="",rsuffix="jz")
df["geom"] = df.apply(lambda row: LineString([row['geometry_x'], row['geometry_y']]), axis=1) #Create a linestring column
df = df[["izone_x","SIJ2023_x","jzone_x","SIJ2023_y","cost","geom"]]
df.to_csv("weird_points_HBO.csv")