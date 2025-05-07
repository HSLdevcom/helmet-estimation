import pandas as pd

print("Reading input file")

# zones_num = 1977
# split_ch=" "
# header = """d1 d2 d3 d4 d5 d6 d7
# d8 d9 d10 d11 d12 d13 d14
# d15 d16 d17 d18 d19 d20 d21
# d22 d23 d24 d25 d26 d27 d28 d29
# d30 d31 d32
# downtownD homeMunD sameZoneD areaIfSame jobDens popDens 
# singleHP carDens pop jobs service shops high universit 
# primary CparkWork CparkOther BsepLen BadjLen BmixLen
# BwTime TwTime TcostWork TcostOther CTime Ccost walkDist 
# WTime"""

# input_file = "../Aineisto/kulkutapa_ja_suuntautumismallien_estimointidatat/WSS.txt"

# zones_num = 2098
# split_ch=","
# header = """pid survey xfactor ttype otherDest closed carsOwned licence car_user employed
# children rzoneCapR rzoneSurrM rzonePerM ind_female age_7_17 age_18_29 age_30_49 age_50_64 age_65
# ageMissing izone izone_cbd mode jzone zone pop age7to17 age18to29 age30to49
# age50to64 age64to99 age7to99 age18to99 female male popDens workplaces service shops logistics
# industry parkCostW parkCostE schoolL1 schoolL2 schoolL3 area detachS detachSqrt helsinki
# cbd lauttaS helsOther espooVantK surround shopsCbd shopsElse carDens carsPer1K """

# input_file = "../Aineisto/uudet2023/flatfiles/output_school_trips_test.csv"

zones_num = 2098
split_ch=" "
header = """izone zone pop age7to17 age18to29 age30to49 age50to64 age64to99 age7to99 age18to99
female male popDens workplaces service shops logistics industry parkCostW parkCostE schoolL1
schoolL2 schoolL3 area detachS detachSqrt helsinki cbd lauttaS helsOther espooVantK
surround shopsCbd shopsElse carDens carsPer1K """

input_file = "../Aineisto/uudet2023/zonedata_base_folded.csv"
header_list = header.replace('\n',' ').split(" ")
header_list = [h for h in header_list if h!=""]
print(header_list)
header_full = []
for hl in header_list:
    if True: #(hl[0] == "d" or hl=="jzone") and hl[-1] != "D":
        header_full.append(hl)
    else:
        for i in range(zones_num):
            header_full.append(hl+str(i+1))
#print(header_full)

item_id =0
data = {hf:[] for hf in header_full}
with open(input_file, "r") as f:
    for line in f.readlines():
        items = line.replace('\n','').split(split_ch)
        for item in items:
            if item == "": continue
            data[header_full[item_id % len(header_full)]].append(item)
            #print(item_id % len(header_full),item)
            item_id += 1

print(len(header_full), item_id)
print("Turning into pandas structure")
print({d:len(data[d]) for d in data})
df = pd.DataFrame(data)
print("Writing to csv")
df.to_csv("../Aineisto/uudet2023/validation_zones.csv", sep=";")

print(df.head())
print(len(df))

