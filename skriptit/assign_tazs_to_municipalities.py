import openmatrix as omx
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from collections import defaultdict as dd

municipalities = {
    "Helsinki": (0, 1999),
    "Espoo": (2000, 3499),
    "Kauniainen": (3500, 3999),
    "Vantaa": (4000, 5999),
    "Kirkkonummi": (6000, 6999),
    "Vihti": (7000, 7999),
    "Nurmijarvi": (8000, 8999),
    "Tuusula": (9000, 9999),
    "Kerava": (10000, 10999),
    "Jarvenpaa": (11000, 11999),
    "Sipoo": (12000, 12999),
    "Mantsala": (13000, 13999),
    "Hyvinkaa": (14000, 14999),
    "Pornainen": (15000, 15499),
    "Siuntio": (15500, 15999),
    "Raasepori": (17000, 17499),
    "Hanko": (17500, 17999),
    "Inkoo": (18000, 18499),
    "Karkkila": (18500, 18999),
    "Lohja": (19000, 19999),
    "Porvoo": (20000, 20999),
    "Pukkila": (21000, 21499),
    "Askola": (21500, 21999),
    "Myrskyla": (22000, 22499),
    "Lapinjarvi": (22500, 22999),
    "Loviisa": (23000, 23999),
    "Salo": (24000, 24499),
    "Somero": (24500, 24999),
    "Hameenlinna": (25000, 25999),
    "Janakkala": (26000, 26499),
    "Hattula": (26500, 26999),
    "Loppi": (27000, 27499),
    "Tammela": (27500, 27999),
    "Riihimaki": (28000, 28999),
    "Hausjarvi": (29000, 29499),
    "Karkola": (29500, 29999),
    "Orimattila": (30000, 30499),
    "Hollola": (30500, 30999),
    "Lahti": (31000, 31999),
}

def get_municipality_number(sij2023_id: int):
    for e,mun in enumerate(municipalities):
        if sij2023_id>=municipalities[mun][0] and sij2023_id<=municipalities[mun][1]:
            return e+1
    print(f"Municipality not found for id {sij2023_id}")
    return 999

#print(get_municipality_number(102),get_municipality_number(31001))        
gdf = gpd.read_file("C:/Users/HajduPe/OneDrive - Helsingin Seudun liikenne - Kuntayhtymä/Aluejako/sij2023/sijoittelualueet2023_raasepori_korjattu.shp")
gdf["helmet_id"] = gdf["SIJ2023"].rank().sub(1).astype(int)
gdf["izone"] = gdf["helmet_id"]+1
gdf["kunta"] = gdf["SIJ2023"].astype(int).apply(get_municipality_number)
gdf.sort_values(by=['SIJ2023'],ascending=True, inplace=True)
with open("../Aineisto/uudet2023/flatfiles/zones_municipality.csv","w") as jfile:
    for e,r in gdf.iterrows():
        jfile.write(str(r["kunta"])+" ")

with open("../Aineisto/uudet2023/zonedata_municipality.csv","w") as ifile:
    for e,r in gdf.iterrows():
        ifile.write(str(r["izone"])+" "+str(r["kunta"])+"\n")
