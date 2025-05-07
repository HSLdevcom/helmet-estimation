import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("Impedance analysis")

malli = "ho"
havainnot = "OTH"
ttype = 5
# malli = "hw"
# havainnot = "WSS"
# ttype = 1
# malli = "hc"
# havainnot = "WSS"
# ttype = 2
# malli = "hu"
# havainnot = "WSS"
# ttype = 3
columns = ["pid","survey","xfactor","ttype","other_destinations","closed","cars_owned","licence","car_user","employed","children","rzone_capital_region",
           "rzone_surrounding_municipality","rzone_peripheral_municipality","female","age_7_17","age_18_29","age_30_49","age_50_64","age_65","age_missing",
           "izone","izone_cbd","mode","jzone"]
oth_data_source = pd.read_csv("C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/Aineisto/uudet2023/havainnot23/"+havainnot+".txt",sep=" ",names=columns)
for i in range(1):
    oth_data = oth_data_source.copy()
    oth_data = oth_data[oth_data["izone"] < 1772]
    oth_data = oth_data[oth_data["ttype"] == ttype]
    #oth_data = oth_data[oth_data["pid"] % 10 == i]
    header = """izone zone pop age7to17 age18to29 age30to49 age50to64 age64to99 age7to99 age18to99 female male popDens workplaces service shops logistics
    industry parkCostW parkCostE schoolL1 schoolL2 schoolL3 area detachS detachSqrt helsinki
    cbd lauttaS helsOther espooVantK surround shopsCbd shopsElse carDens carsPer1K"""


    col_headers = " ".join(header.split("\n")).split(" ")
    zone_data = pd.read_csv("C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/Aineisto/uudet2023/validation_zones.csv",sep=";",encoding="ANSI")
    #print(zone_data)
    oth_data = oth_data.merge(zone_data, on='izone', how='right')
    oth_data = oth_data[oth_data["mode"].isin([1,2,3,4,5])]
    vastukset_dir = "C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/Aineisto/uudet2023/vastukset/"
    
    t_cost = pd.read_csv(vastukset_dir + malli + "_transit_cost.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])
    t_time = pd.read_csv(vastukset_dir + malli + "_transit_time.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])
    t_dist = pd.read_csv(vastukset_dir + malli + "_transit_dist.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])
    c_cost = pd.read_csv(vastukset_dir + malli + "_car_cost.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])
    c_time = pd.read_csv(vastukset_dir + malli + "_car_time.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])
    c_dist = pd.read_csv(vastukset_dir + malli + "_car_dist.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])

    # print(t_cost)
    # print(t_cost.size)
    # print("Lookup")
    # print(t_cost.iat[1768,1])
    # print(t_cost["izone"])
    oth_data["t_cost"] = oth_data.apply(lambda x: t_cost.iat[int(x.izone-1), int(x.jzone)], axis=1)
    oth_data["c_cost"] = oth_data.apply(lambda x: c_cost.iat[int(x.izone-1), int(x.jzone)], axis=1)
    oth_data["c_time"] = oth_data.apply(lambda x: c_time.iat[int(x.izone-1), int(x.jzone)], axis=1)
    oth_data["c_dist"] = oth_data.apply(lambda x: c_dist.iat[int(x.izone-1), int(x.jzone)], axis=1)
    oth_data["t_time"] = oth_data.apply(lambda x: t_time.iat[int(x.izone-1), int(x.jzone)], axis=1)
    oth_data["t_dist"] = oth_data.apply(lambda x: t_dist.iat[int(x.izone-1), int(x.jzone)], axis=1)
    print(oth_data)
    c_kerroin = 0.0895
    mode2color = {1: "green",2:"orange",3:"blue",4:"red",5:"red"}
    oth_data["modes_color"] = oth_data["mode"].apply(lambda x: mode2color[x])


    oth_data["vast_pop"] = (oth_data["c_cost"]+c_kerroin*oth_data["c_time"])*oth_data["pop"]
    plt.title("Model: "+malli)
    #print(oth_data["vast_pop"])
    #plt.hist(oth_data["c_dist"], [i for i in range(150)])
    #plt.hist(oth_data["c_cost"]+c_kerroin*oth_data["c_time"],[i*1 for i in range(100)],label=str(i), histtype='step')
    #plt.scatter(oth_data["t_cost"],oth_data["t_time"],c=oth_data["modes_color"], label="scatter")
    plt.scatter(np.power(oth_data["t_cost"],1),oth_data["t_dist"],c=oth_data["modes_color"], label="blue=pt, red=car")
    # for x,y,i,j in zip(np.power(oth_data["t_cost"],1),oth_data["t_dist"]/oth_data["t_time"],oth_data["izone"],oth_data["jzone"]):
    #     plt.annotate(str(i)+"->"+str(int(j)), (x,y))
    #plt.scatter(oth_data["c_dist"],oth_data["c_cost"]+c_kerroin*oth_data["c_time"],label=str(i))

    # for e,r in oth_data.iterrows():
    #     if r["t_cost"]>15 and r["mode"]==3:
    #         print(r["izone"],int(r["jzone"]),r["t_cost"])
plt.legend()
plt.show()

