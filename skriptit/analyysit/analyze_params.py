import sys

# adding Folder_2 to the system path
sys.path.insert(0, 'C:\\Users\\HajduPe\\helmet-model-system-olusanya\\Scripts')

from parameters.departure_time import demand_share
from parameters.assignment import volume_factors,assignment_classes

trips_num = 1
periods = ["aht","pt","iht"]
for tclass in ["hw","hc","hu","hs","ho"]:
    #tclass = "ho"
    mode = "transit"
    vtype = "transit_"+assignment_classes[tclass]
    trips = [trips_num * demand_share[tclass]["transit"][period] for period in periods]
    # print(tclass)
    # print(trips)
    # print([volume_factors[vtype][period] for period in periods])
    # print([tp[0]*volume_factors[vtype][period] for tp,period in zip(trips,periods)])
    # print([tp[1]*volume_factors[vtype][period] for tp,period in zip(trips,periods)])
    trips_vrk_s1 = sum([tp[0]*volume_factors[vtype][period] for tp,period in zip(trips,periods)])
    trips_vrk_s2 = sum([tp[1]*volume_factors[vtype][period] for tp,period in zip(trips,periods)])

    print(tclass,trips_vrk_s1,trips_vrk_s2)



