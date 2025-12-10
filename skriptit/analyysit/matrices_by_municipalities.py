import openmatrix as omx
import pandas as pd
from collections import defaultdict as dd
from datetime import datetime, time

def gettimeperiod(ttime):
    tps = {"aht": (time(7,30), time(8,30)),
           "pt": (time(12,0),time(13,0)),
           "iht": (time(15,30),time(16,30))}
    # Define the datetime to check
    dt_to_check = datetime.fromisoformat(ttime)

    for tp in tps:
        start_time = tps[tp][0]
        end_time = tps[tp][1]
        if start_time <= dt_to_check.time() < end_time:
            return tp
    
    return "other"

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

volume_factors = {
    "car": {
        "aht": 2.0622815050146266,
        "pt": 10.87756099936012,
        "iht": 2.636256734240595
    },
    "car_work": {
        "aht": 2.1511371941701443,
        "pt": 9.595261522147535,
        "iht": 2.6876828857537505
    },
    "car_leisure": {
        "aht": 1.822633510494245,
        "pt": 12.416216799069286,
        "iht": 2.567335795915922
    },
    "transit": {
        "aht": 1.718651340007729,
        "pt": 9.215218973897288,
        "iht": 2.466313449878458
    },
    "transit_work": {
        "aht": 1.7648082264481162,
        "pt": 9.458785710446705,
        "iht": 2.358668559084971
    },
    "transit_leisure": {
        "aht": 1.6101278413419995,
        "pt": 8.855898570776446,
        "iht": 2.7822971006521318
    },
    "bike": {
        "aht": 1.592424507799951,
        "pt": 9.778768584286764,
        "iht": 2.430075096866623
    },
    "bike_work": {
        "aht": 1.7792746478588168,
        "pt": 9.577998573953217,
        "iht": 2.0977940770728236
    },
    "bike_leisure": {
        "aht": 1.4153296994517823,
        "pt": 9.921895075001368,
        "iht": 3.003522618985676
    },
    "trailer_truck": {
        "aht": 3.3333333333333335,
        "pt": 10.0,
        "iht": 3.3333333333333335
    },
    "truck": {
        "aht": 3.3333333333333335,
        "pt": 10.0,
        "iht": 3.3333333333333335
    },
    "van": {
        "aht": 3.3333333333333335,
        "pt": 10.0,
        "iht": 3.3333333333333335
    },
    "bus": {
        "aht": 2.0120724346076457,
        "pt": 11.11111111111111,
        "iht": 2.0120724346076457
    }
}

heha = pd.read_excel("C:\\Users\\HajduPe\\helmet-data-preprocessing\\input\\HEHA-aineistot\\HEHA23_MATKAT_KERTOIMET_sij23.xlsx")
heha["period"] = heha["aika"].apply(lambda x: gettimeperiod(x.split(",")[0]))
print("Excel loaded")
modes = {"car":1,"transit":2,"bike":3,"walk":4,"other":5}
modes_autokul = {"car":" & autokul==1","transit":"","bike":"","walk":"","other":""}
# chosen = "transit"
# chosen = "car"
# chosen = "bike"
for period in ["aht","pt","iht","vrk"]:
    for chosen in ["bike","car","transit"]:
        if period == "vrk":
            heha_suodattu = heha.query(f"kerroin_arki>0 & pktapa2_luok=={modes[chosen]}{modes_autokul[chosen]} & LENKKI==2")
        else:
            heha_suodattu = heha.query(f"kerroin_arki>0 & pktapa2_luok=={modes[chosen]}{modes_autokul[chosen]} & period=='{period}' & LENKKI==2")

        volumes = dd(lambda: 0)
        if period == "vrk":
            periods = ["aht","pt","iht"]
        else:
            periods = [period]
        for tp in periods:

            with omx.open_file(f"T:/Petr Hajduk/Helmet 5/Matrices/demand_{tp}.omx") as myfile:

                zone_mapping = myfile.mapping("zone_number")
                muns = {mun: [zone_mapping[x] for x in zone_mapping if x >= municipalities[mun][0] and x < municipalities[mun][1]] for mun in municipalities}

                for m1 in muns:
                    for m2 in muns:
                        if period == "vrk":
                            volumes[(m1,m2)] += sum([myfile[tg][muns[m1][0]:muns[m1][-1],muns[m2][0]:muns[m2][-1]].sum()*volume_factors[tg][tp] for tg in [f"{chosen}_work",f"{chosen}_leisure"]])
                        else:
                            volumes[(m1,m2)] += sum([myfile[tg][muns[m1][0]:muns[m1][-1],muns[m2][0]:muns[m2][-1]].sum() for tg in [f"{chosen}_work",f"{chosen}_leisure"]])
                        #print(tp,m1,m2,volumes[(m1,m2)])

        with open(f"analyysit/od_flows_{chosen}_{period}.txt","w") as file:
            file.writelines(["from,to,helmet_volume,heha_volume\n"])
            for m1 in muns: # type: ignore
                for m2 in muns: # type: ignore
                    volume = volumes[(m1,m2)]
                    heha_volume = heha_suodattu.query(f'(aloitus_sij23 > {municipalities[m1][0]})&(aloitus_sij23 < {municipalities[m1][1]})&(maaranpaa_sij23 > {municipalities[m2][0]})&(maaranpaa_sij23 < {municipalities[m2][1]})')["kerroin_arki"].sum()
                    file.writelines([f"{m1},{m2},{volume},{heha_volume}\n"])

            # helsinki = [zone_mapping[x] for x in zone_mapping if x >= municipalities["Helsinki"][0] and x < municipalities["Helsinki"][1]]
            # espoo = [zone_mapping[x] for x in zone_mapping if x >= municipalities["Espoo"][0] and x < municipalities["Espoo"][1]]
            # print(myfile["transit_work"][espoo[0]:espoo[-1],helsinki[0]:helsinki[-1]].sum())
