import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("Impedance analysis")

# malli = "ho"
# havainnot = "OTH"
# ttype = 5
# malli = "hw"
# havainnot = "WSS"
# ttype = 1
# malli = "hc"
# havainnot = "WSS"
# ttype = 2
malli = "hu"
havainnot = "WSS"
ttype = 3
# malli = "hs"
# havainnot = "SPB"
# ttype = 4
columns = ["pid","survey","xfactor","ttype","other_destinations","closed","cars_owned","licence","car_user","employed","children","rzone_capital_region",
           "rzone_surrounding_municipality","rzone_peripheral_municipality","female","age_7_17","age_18_29","age_30_49","age_50_64","age_65","age_missing",
           "izone","izone_cbd","mode","jzone"]

mode_split_modes = {"bike":[2],"car":[4,5],"transit":[3],"walk":[1]}
length_split_bins = {"0-1":(0,1),"1-3":(1,3),"3-5":(3,5),"5-10":(5,10),"10-20":(10,20),"20-30":(20,30),"30-40":(30,40),"40-inf":(40,1000)}
trip_dist_data = {}
for malli,havainnot,ttype in zip(["hw","hc","hu","hs","ho"],["WSS","WSS","WSS","SPB","OTH"],[1,2,3,4,5]):
    print("malli: "+malli)
    oth_data = pd.read_csv("C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/Aineisto/uudet2023/havainnot23/"+havainnot+".txt",sep=" ",names=columns)
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
    w_dist = pd.read_csv(vastukset_dir + malli + "_walk_dist.csv",sep=" ",names=["izone"]+[str(i) for i in range(1,2099)])

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
    oth_data["w_dist"] = oth_data.apply(lambda x: w_dist.iat[int(x.izone-1), int(x.jzone)], axis=1)

    tot_sum = oth_data["xfactor"].sum()
    dist_by_modes = {malli+"_"+lm:[] for lm in ["c","t","b","w"]}
    for m in mode_split_modes:
        mode_filtered = oth_data[oth_data["mode"].isin(mode_split_modes[m])]
        n_obs= mode_filtered["xfactor"].sum()
        print(f"Mode: {m}, Count: {n_obs:.0f}, Share: {n_obs/tot_sum:.2f}")
        if m == "car":
            n_obs= mode_filtered[mode_filtered["jzone"]==mode_filtered["izone"]]["xfactor"].sum()
            #print(f"Mode: {m}, Length: 0.0, Count: {n_obs:.0f}")
            for l in length_split_bins:
                bin = length_split_bins[l]
                n_obs= mode_filtered[(mode_filtered["c_dist"]>=bin[0])&(mode_filtered["c_dist"]<bin[1])]["xfactor"].sum()
                #print(f"Mode: {m}, Length: {l}, Count: {n_obs:.0f}")
                dist_by_modes[malli+"_"+m[:1]].append(int(n_obs))
        if m == "transit":
            n_obs= mode_filtered[mode_filtered["jzone"]==mode_filtered["izone"]]["xfactor"].sum()
            #print(f"Mode: {m}, Length: 0.0, Count: {n_obs:.0f}")
            for l in length_split_bins:
                bin = length_split_bins[l]
                n_obs= mode_filtered[(mode_filtered["t_dist"]>=bin[0])&(mode_filtered["t_dist"]<bin[1])]["xfactor"].sum()
                #print(f"Mode: {m}, Length: {l}, Count: {n_obs:.0f}")
                dist_by_modes[malli+"_"+m[:1]].append(int(n_obs))
        if m == "bike":
            n_obs= mode_filtered[mode_filtered["jzone"]==mode_filtered["izone"]]["xfactor"].sum()
            #print(f"Mode: {m}, Length: 0.0, Count: {n_obs:.0f}")
            for l in length_split_bins:
                bin = length_split_bins[l]
                n_obs= mode_filtered[(mode_filtered["w_dist"]>=bin[0])&(mode_filtered["w_dist"]<bin[1])]["xfactor"].sum()
                dist_by_modes[malli+"_"+m[:1]].append(int(n_obs))
        if m == "walk":
            n_obs= mode_filtered[mode_filtered["jzone"]==mode_filtered["izone"]]["xfactor"].sum()
            #print(f"Mode: {m}, Length: 0.0, Count: {n_obs:.0f}")
            for l in length_split_bins:
                bin = length_split_bins[l]
                n_obs= mode_filtered[(mode_filtered["w_dist"]>=bin[0])&(mode_filtered["w_dist"]<bin[1])]["xfactor"].sum()
                #print(f"Mode: {m}, Length: {l}, Count: {n_obs:.0f}")
                dist_by_modes[malli+"_"+m[:1]].append(int(n_obs))
    trip_dist_data.update(dist_by_modes)
pd.DataFrame(trip_dist_data,index=list(length_split_bins.keys())).to_csv("analyysit/trips_by_dist.csv")