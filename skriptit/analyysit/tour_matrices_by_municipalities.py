import openmatrix as omx
import pandas as pd
from collections import defaultdict as dd
from datetime import datetime, time

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
    # "Raasepori": (17000, 17499),
    # "Hanko": (17500, 17999),
    # "Inkoo": (18000, 18499),
    # "Karkkila": (18500, 18999),
    # "Lohja": (19000, 19999),
    # "Porvoo": (20000, 20999),
    # "Pukkila": (21000, 21499),
    # "Askola": (21500, 21999),
    # "Myrskyla": (22000, 22499),
    # "Lapinjarvi": (22500, 22999),
    # "Loviisa": (23000, 23999),
    # "Salo": (24000, 24499),
    # "Somero": (24500, 24999),
    # "Hameenlinna": (25000, 25999),
    # "Janakkala": (26000, 26499),
    # "Hattula": (26500, 26999),
    # "Loppi": (27000, 27499),
    # "Tammela": (27500, 27999),
    # "Riihimaki": (28000, 28999),
    # "Hausjarvi": (29000, 29499),
    # "Karkola": (29500, 29999),
    # "Orimattila": (30000, 30499),
    # "Hollola": (30500, 30999),
    # "Lahti": (31000, 31999),
}

heha = pd.read_csv("C:\\Users\\HajduPe\\helmet-data-preprocessing\\tours\\tours-heha23.csv",sep=";",decimal=",")
heha["xfactor"] = heha["xfactor"].apply(lambda x: float(x))
heha["zone_origin"] = heha["zone_origin"].apply(lambda x: int(x))
heha["zone_destination"] = heha["zone_destination"].apply(lambda x: int(x))
print(heha.head())
modes = {"car":4,"transit":3,"bike":2,"walk":1,"other":6} #NOTE: HEHA numbers
modes_autokul = {"car":" | mode==5","transit":"","bike":"","walk":"","other":""}



for chosen in ["walk","bike","car","transit"]:
    volumes = dd(lambda: 0)
    heha_suodattu = heha.query(f"mode=={modes[chosen]}{modes_autokul[chosen]}")
    print(chosen, heha_suodattu.query("zone_origin < 2000 & zone_destination < 2000")["xfactor"].sum())
    for tt in ["hc","ho","hs","hu","hw","oo","wo"]:    
        with omx.open_file(f"T:/Petr Hajduk/Helmet 5/estimation/demand_{tt}.omx") as myfile:
            zone_mapping = myfile.mapping("zone_number")
            muns = {mun: [zone_mapping[x] for x in zone_mapping if x >= municipalities[mun][0] and x < municipalities[mun][1]] for mun in municipalities}
            print(myfile.list_matrices())
            for m1 in muns:
                for m2 in muns:
                    #volumes[(m1,m2)] += sum([myfile[tg][muns[m1][0]:muns[m1][-1],muns[m2][0]:muns[m2][-1]].sum()*volume_factors[tg][tp] for tg in [f"{chosen}_work",f"{chosen}_leisure"]])
                    volumes[(m1,m2)] += sum([myfile[tg][muns[m1][0]:muns[m1][-1],muns[m2][0]:muns[m2][-1]].sum() for tg in [f"{chosen}"]])
                    #print(tp,m1,m2,volumes[(m1,m2)])
        
    with open(f"analyysit/demand_flows_{chosen}.txt","w") as file:
        file.writelines(["from,to,helmet_volume,heha_volume\n"])
        for m1 in muns: # type: ignore
            for m2 in muns: # type: ignore
                volume = volumes[(m1,m2)]
                heha_volume = heha_suodattu.query(f'(zone_origin > {municipalities[m1][0]})&(zone_origin < {municipalities[m1][1]})&(zone_destination > {municipalities[m2][0]})&(zone_destination < {municipalities[m2][1]})')["xfactor"].sum()
                print(m1,m2)
                print(volume)
                print(heha_volume)
                file.writelines([f"{m1},{m2},{volume},{heha_volume}\n"])