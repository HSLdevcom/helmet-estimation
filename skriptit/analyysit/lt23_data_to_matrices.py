import openmatrix as omx
import pandas as pd
from collections import defaultdict as dd
from datetime import datetime, time
import numpy as np

# with omx.open_file(f"T:/Petr Hajduk/Helmet5/Matrices_LT23/demand_iht.omx","r") as newfile:
#     print(np.sum(newfile["trailer_truck"]))
# exit()
# data = {'A': ['origin1', 'origin2', 'origin1', 'origin3','origin3','origin4'],
#         'B': ['destination1', 'destination2', 'destination2', 'destination1', 'destination1','destination4'],
#         'C': [10, 20, 30, 40, 40,17]}
# df = pd.DataFrame(data)
# grouped_df = df.groupby(['A', 'B']).sum().reset_index()
# pivot_table = grouped_df.pivot_table(index='A', columns='B', values='C', fill_value=0)
# origins = ['origin1', 'origin2', 'origin3', 'origin4']  # Add all possible origins
# destinations = ['destination1', 'destination2', 'destination3', 'destination4']  # Add all possible destinations
# predefined_matrix = pd.DataFrame(0, index=origins, columns=destinations)
# for _, row in grouped_df.iterrows():
#     predefined_matrix.loc[row['A'], row['B']] = row['C']
# numpy_matrix = predefined_matrix.to_numpy()
# print(numpy_matrix)

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


heha = pd.read_excel("C:\\Users\\HajduPe\\helmet-data-preprocessing\\input\\HEHA-aineistot\\HEHA23_MATKAT_KERTOIMET_sij23.xlsx")
print(heha["pktapa2_luok"].head())
modes = {"car":1,"transit":2,"bike":3,"walk":4,"other":5}
modes_autokul = {"car":" & autokul==1","transit":"","bike":"","walk":"","other":""}
# chosen = "transit"
# chosen = "car"
# chosen = "bike"
heha["ajanjakso"] = heha["aika"].apply(lambda x: gettimeperiod(x.split(",")[0]))
#heha_suodattu = heha.query(f"kerroin_arki>0 & pktapa2_luok=={modes[chosen]}{modes_autokul[chosen]}")
heha_suodattu = heha.query(f"kerroin_arki>0")
print(heha_suodattu["ajanjakso"].head())
suodatukset = {f"{chsn}_work": f"pktapa2_luok=={modes[chsn]}{modes_autokul[chsn]}" for chsn in modes}
suodatukset.update({f"{chsn}_leisure": f"pktapa2_luok==7" for chsn in modes}) #returns nothing on purpose

volumes = dd(lambda: 0)
for tp in ["aht","pt","iht"]:
    with omx.open_file(f"T:/Petr Hajduk/Helmet5/Matrices/demand_{tp}.omx") as myfile:
        with omx.open_file(f"T:/Petr Hajduk/Helmet5/Matrices_LT23/demand_{tp}.omx","w") as newfile:
            zone_mapping = myfile.mapping("zone_number")
            newfile.create_mapping('zone_number', list(zone_mapping.keys()))
            # print(myfile.mapping("zone_number"))
            # print(newfile.mapping("zone_number"))
            # exit()
            for tg in myfile.list_matrices():
                newfile[tg] = myfile[tg]
                print(tg, myfile[tg][:1771,:1771].sum())
                if tg not in suodatukset: continue #trucks etc.
                #print(f"ajanjakso=={tp} & {suodatukset[tg]} & aloitus_sij23<15500 & maaranpaa_sij23<15500")
                heha_data = heha_suodattu.query(f"ajanjakso=='{tp}' & {suodatukset[tg]} & aloitus_sij23<15500 & maaranpaa_sij23<15500")

                df = heha_data[['aloitus_sij23', 'maaranpaa_sij23', 'kerroin_arki']]
                grouped_df = df.groupby(['aloitus_sij23', 'maaranpaa_sij23']).sum().reset_index()
                origins = [o for o in zone_mapping if o<16000]  # Add all possible origins
                print(len(origins),origins[-1])
                destinations = [o for o in zone_mapping if o<16000]  # Add all possible destinations
                predefined_matrix = pd.DataFrame(0.0, index=origins, columns=destinations)
                for _, row in grouped_df.iterrows():
                    predefined_matrix.loc[row['aloitus_sij23'], row['maaranpaa_sij23']] = float(row['kerroin_arki'])
                numpy_matrix = predefined_matrix.to_numpy()
                print(numpy_matrix[:10,:10])
                print(numpy_matrix.shape)
                
                newfile[tg][:1771,:1771] = numpy_matrix

            print(zone_mapping[101])
            
