import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

heha = pd.read_excel("C:\\Users\\HajduPe\\helmet-data-preprocessing\\input\\HEHA-aineistot\\HEHA23_MATKAT_KERTOIMET_sij23.xlsx")
print(heha.query(f"LENKKI == 1 & aloitus_sij23 == 133")["kerroin_arki"].sum())
heha["username"] = heha["username"].apply(lambda x: str(x))

taustat = pd.read_excel("C:\\Users\\HajduPe\\helmet-data-preprocessing\\input\\HEHA-aineistot\\HEHA23_TAUSTAT_KERTOIMET_sij23.xlsx")
taustat["username"] = taustat["username"].apply(lambda x: str(x))

heha = heha.merge(taustat, on = "username")

municipalities = {
    "s2": (130, 131),
    "s3": (131, 132),
    "special": (132, 133),
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

# zone_data = pd.read_csv("C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/Aineisto/uudet2023/validation_zones.csv",sep=";",encoding="ANSI")
# zone_data = zone_data[["zone","pop"]]

# zone_data["hh_trips"] = zone_data["zone"].apply(lambda alue: heha.query(f"LENKKI == 1 & aloitus_sij23 == {alue}")["kerroin_arki_x"].sum())
# zone_data["hh_per_capita"] = zone_data["hh_trips"] / zone_data["pop"]
# zone_data = zone_data[zone_data["zone"]<15500]

#zone_data.plot.scatter("pop","hh_trips")

# for mun in municipalities:
#     m_count = zone_data.query(f"zone>{municipalities[mun][0]} & zone<={municipalities[mun][1]}")["hh_trips"].sum()
#     p_count = zone_data.query(f"zone>{municipalities[mun][0]} & zone<={municipalities[mun][1]}")["pop"].sum()
#     print(mun,m_count/p_count)
# print("all", zone_data["hh_trips"].sum()/zone_data["pop"].sum())

modes = {"car":1,"transit":2,"bike":3,"walk":4,"other":5}
modes_autokul = {"car":" & autokul==1","transit":"","bike":"","walk":"","other":""}
tot_sum = heha.query(f"LENKKI == 1")["kerroin_arki_x"].sum()
print("All hh trips", tot_sum)
expsum = 0
# for chosen in ["walk","bike","transit","car"]:
#     heha_suodattu = heha.query(f"kerroin_arki_x>0 & pktapa2_luok=={modes[chosen]}{modes_autokul[chosen]} & LENKKI==1")
#     i_count = heha_suodattu["kerroin_arki_x"].sum()
#     print(chosen,i_count,i_count/tot_sum, np.log(i_count/tot_sum))
#     expsum += np.exp(np.log(i_count/tot_sum))
# print(expsum)

# Age groups in zone data
age_groups = [ #changed to list for type checker
        (7, 17),
        (18, 29),
        (30, 49),
        (50, 64),
        (65, 99),
]

tot_sum = heha["kerroin_arki_x"].sum()
i_series = [0 for _ in range(len(age_groups))]
t_series = [0 for _ in range(len(age_groups))]
chosen = "bike"
for e,(ab,af) in enumerate(age_groups):
    i_count = heha.query(f"ika>{ab} & ika<={af} & LENKKI == 1 & pktapa2_luok=={modes[chosen]}")["kerroin_vkl_x"].sum()
    t_count = taustat.query(f"ika>{ab} & ika<={af}")["kerroin_arki"].sum()
    print(ab,af, i_count/t_count)
    i_series[e] = i_count
    t_series[e] = t_count
plt.plot([(ag[0]+ag[1])/2 for ag in age_groups],[i/t for i,t in zip(i_series,t_series)])

plt.show()