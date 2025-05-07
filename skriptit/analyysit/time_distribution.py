from datetime import datetime, time
import pandas as pd
import matplotlib.pyplot as plt

# heha = pd.read_excel("C:\\Users\\HajduPe\\helmet-data-preprocessing\\input\\HEHA-aineistot\\HEHA23_MATKAT_KERTOIMET_sij23.xlsx")
# heha["itime"] = heha["aika"].apply(lambda x: datetime.fromisoformat(x.split(",")[0]).time().hour+datetime.fromisoformat(x.split(",")[0]).time().minute/60)
# heha["jtime"] = heha["aika"].apply(lambda x: datetime.fromisoformat(x.split(",")[1]).time().hour+datetime.fromisoformat(x.split(",")[1]).time().minute/60)
# heha.to_pickle("./heha.pkl")  

mode = 3
heha = pd.read_pickle("./heha.pkl") #Remember to remove
heha = heha.query(f"kerroin_arki>0 & pktapa2_luok=={mode}")
heha["kuuma"] = heha["maaranpaa_sij23"].apply(lambda x: x>6000)

print(heha["itime"].head())
scaler = 2
bins = list(range(30*scaler))

heha_all = heha
data_all = heha_all.groupby(pd.cut(heha_all.itime*scaler, bins), observed=False).apply(lambda x: (x['kerroin_arki']).sum())

heha_kuuma = heha.query(f"kuuma==True")
data_kuuma = heha_kuuma.groupby(pd.cut(heha_kuuma.itime*scaler, bins), observed=False).apply(lambda x: (x['kerroin_arki']).sum())

heha_pks = heha.query(f"kuuma==False")
data_pks = heha_pks.groupby(pd.cut(heha_pks.itime*scaler, bins), observed=False).apply(lambda x: (x['kerroin_arki']).sum())

# heha_kuuma_sis = heha.query(f"kerroin_arki>0 & pktapa2_luok==2 & aloitus_sij23>6000 & maaranpaa_sij23>6000")
# data_kuuma_sis = heha_kuuma_sis.groupby(pd.cut(heha_kuuma_sis.itime*scaler, bins), observed=False).apply(lambda x: (x['kerroin_arki']).sum())

heha_hel_sis = heha.query(f"kerroin_arki>0 & pktapa2_luok=={mode} & aloitus_sij23<2000 & maaranpaa_sij23<2000")
data_hel_sis = heha_hel_sis.groupby(pd.cut(heha_hel_sis.itime*scaler, bins), observed=False).apply(lambda x: (x['kerroin_arki']).sum())

#data = groups.size().unstack()
# print(type(groups))
# data = groups
# print(data)
#plt.plot(bins[:-1],[d/sum(data_kuuma.T) for d in data_kuuma.T],label="Kuuma")
plt.plot(bins[:-1],[d/sum(data_hel_sis.T) for d in data_hel_sis.T],label="Helsinki sisäinen")
plt.plot(bins[:-1],[d/sum(data_all.T) for d in data_all.T],label="All")
plt.legend()
plt.show()