import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:\\Users\\HajduPe\\helmet-model-system\\Scripts')

from parameters.departure_time import demand_share
from parameters.impedance_transformation import impedance_share
from parameters.assignment import volume_factors,assignment_classes
from parameters.tour_generation import tour_generation
from parameters.mode_choice import mode_choice
from parameters.destination_choice import destination_choice


trips_num = 1
periods = ["aht","pt","iht"]
mode = "walk"

# mode_kertoimet = {"car": 1, "transit": 1, "bike": 1,  "walk": 1}
# for tclass in ["hw","hc","hu","hs","ho","wo","oo"]:
#     #tclass = "ho"
#     vtype = mode+"_"+assignment_classes[tclass]
#     trips = [(trips_num * demand_share[tclass][mode][period][0],
#               trips_num * demand_share[tclass][mode][period][1]) for period in periods]
#     #print(trips)
#     sec_dest_generation = [((trips_num * mode_kertoimet[mode] * tour_generation["hoo"][tclass][mode] * demand_share["hoo"][mode][period][0][0],
#                             trips_num * mode_kertoimet[mode]* tour_generation["hoo"][tclass][mode] * demand_share["hoo"][mode][period][0][1]),
#                             (trips_num * mode_kertoimet[mode]* tour_generation["hoo"][tclass][mode] * demand_share["hoo"][mode][period][1][0],
#                             trips_num * mode_kertoimet[mode]* tour_generation["hoo"][tclass][mode] * demand_share["hoo"][mode][period][1][1]))  for period in periods]
#     print(tclass)
#     print(tour_generation["hoo"][tclass][mode])
#     print(sec_dest_generation)
#     print(trips)
#     print([volume_factors[vtype][period] for period in periods])
#     print([tp[0]*volume_factors[vtype][period] for tp,period in zip(trips,periods)])
#     print([tp[1]*volume_factors[vtype][period] for tp,period in zip(trips,periods)])

#     trips_vrk_s1 = sum([(tp[0]+d2trips[1][1])*volume_factors[vtype][period] for tp,d2trips,period in zip(trips,sec_dest_generation,periods)])
#     trips_vrk_s2 = sum([(tp[1]+d2trips[0][0])*volume_factors[vtype][period] for tp,d2trips,period in zip(trips,sec_dest_generation,periods)])
#     trips_vrk_sec1 = sum([(d2trips[1][1])*volume_factors[vtype][period] for tp,d2trips,period in zip(trips,sec_dest_generation,periods)])
#     trips_vrk_sec2 = sum([(d2trips[0][0])*volume_factors[vtype][period] for tp,d2trips,period in zip(trips,sec_dest_generation,periods)])

#     # print(tclass,assignment_classes[tclass], f"{trips_vrk_s1:.2f}",f"{trips_vrk_s2:.2f}","---",f"{trips_vrk_sec1:.2f}",f"{trips_vrk_sec2:.2f}")

# #Impendance shares (ei käytössä, laskettu suoraan R datasta)
# with open("analyysit/analyze_test.csv","w+") as f:
#     for tclass in ["hw","hc","hu","hs","ho","wo","oo","hwp","hop","oop","hoo0","hoo1"]:
#         rclass = tclass[:3]
#         for mode in ["car","transit","bike","walk","park_and_ride"]:
#             if mode not in demand_share[rclass]: continue
#             for tp in ["aht","pt","iht"]:
#                 if tclass[:3] == "hoo":
#                     if tclass == "hoo0":
#                         f.write(f'{tclass}\t{mode}\t{tp}\t{demand_share[rclass][mode][tp][0][0]:.6f}\t{demand_share[rclass][mode][tp][0][1]:.6f}\n')
#                     else:
#                         f.write(f'{tclass}\t{mode}\t{tp}\t{demand_share[rclass][mode][tp][1][0]:.6f}\t{demand_share[rclass][mode][tp][1][1]:.6f}\n')
#                 else:
#                     f.write(f'{tclass}\t{mode}\t{tp}\t{demand_share[tclass][mode][tp][0]:.6f}\t{demand_share[tclass][mode][tp][1]:.6f}\n')

# with open("analyysit/analyze_sec_dest.csv","w+") as f:
#     for tclass in ["hw","hc","hu","hs","ho","wo","oo"]:
#         row = []
#         for mode in ["car","transit","bike","walk"]:
#             row.append(f'{tour_generation["hoo"][tclass][mode]:.6f}')
#         print(row)
#         row_joined = "\t".join(row)
#         print(row_joined)
#         f.write(f'{row_joined}\n')

# print(volume_factors.keys())
# with open("analyysit/analyze_expansion.csv","w+") as f:
#     for mode in ["car","transit","bike",'trailer_truck', 'truck', 'van', 'bus', 'aux_transit']:
#         for tp in ["aht","pt","iht"]:
#             row = [f'{mode}_{tp}']

#             for tclass in ["","_work","_leisure"]:
#                 try:
#                     print(f"{mode}{tclass}")
#                     row.append(f'{volume_factors[f"{mode}{tclass}"][tp]:.6f}')
#                 except:
#                     pass
#             print(row)
#             row_joined = "\t".join(row)
#             print(row_joined)
#             f.write(f'{row_joined}\n')

# print(volume_factors.keys())
# with open("analyysit/analyze_impedance_shares.csv","w+") as f:
#     for tclass in ["hw","hc","hu","hs","ho","wo","oo","hwp","hop","oop","hoo"]:
#         rclass = tclass[:3]
#         for mode in ["car","transit","bike","walk","park_and_ride"]:
#             if mode not in impedance_share[rclass]: continue
#             for tp in ["aht","pt","iht"]:
#                 f.write(f'{tclass}\t{mode}\t{tp}\t{impedance_share[tclass][mode][tp][0]:.6f}\t{impedance_share[tclass][mode][tp][1]:.6f}\n')
    
print("Kalibrointikertoimet")
#print(mode_choice)
with open("analyysit/analyze_calibration.csv","w+") as f:
    for tclass in ["hw","hc","hu","hs","ho","wo","oo"]:
        
        for mode in ["car","transit","bike","walk","park_and_ride"]:
            if mode not in mode_choice[tclass]: continue
            row = [tclass,mode]
            # row = []
            for s1,s2 in [("generation","cbd"),("generation","helsinki_other"),("generation","espoo_vant_kau"),("constant",1)]:
                val = mode_choice[tclass][mode][s1][s2]
                if s1 == "constant": #handle kehyskunnat
                    val -= mode_choice[tclass][mode][s1][0] #reduce by base constant
                row.append(f'{val:.6f}')

            row_joined = "\t".join(row)
            print(row_joined)
            f.write(f'{row_joined}\n')