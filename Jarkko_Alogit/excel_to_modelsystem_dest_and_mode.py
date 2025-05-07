import pandas as pd
import numpy as np
from copy import deepcopy
import sys
import json
from functools import reduce
import operator
from typing import Any, Dict, Optional
import numpy # type: ignore

def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value 

# Convert the dataframe to a dictionary


def print_dict(key_value_dict, dict_name):
    def serialize_dict(d, indent=4, level=1):
        """
        Serializes a dictionary to a string that represents Python code.
        Handles tuples as keys.
        """
        def serialize_item(key, value, level):
            key_str = repr(key)
            value_str = serialize_value(value, indent, level + 1)
            return f"{key_str}: {value_str}"

        def serialize_value(value, indent, level):
            if isinstance(value, dict):
                return serialize_dict(value, indent, level)
            elif isinstance(value, list):
                indented_items = [serialize_value(v, indent, level + 1) for v in value]
                indented_list = "[\n" + ",\n".join(" " * (level * indent) + item for item in indented_items) + "\n" + " " * ((level - 1) * indent) + "]"
                return indented_list
            else:
                if type(value) == np.float64:
                    value = float(value)
                rval = repr(value)
                return rval

        items = [serialize_item(k, v, level) for k, v in d.items()]
        indented_dict = "{\n" + ",\n".join(" " * (level * indent) + item for item in items) + "\n" + " " * ((level - 1) * indent) + "}"
        return indented_dict
    


    # Serialize the dictionary
    serialized_dict = f"{dict_name} = " + serialize_dict(key_value_dict)
    serialized_dict = serialized_dict.replace("'\"", "")
    serialized_dict = serialized_dict.replace("\"'", "")
    serialized_dict = serialized_dict.replace("'", "\"")
    serialized_dict = serialized_dict.replace("\"(", "(")
    serialized_dict = serialized_dict.replace(")\"", ")")

    return serialized_dict

destination_beginning = """
from typing import Any, Dict
import numpy as np # type: ignore


### DESTINATION CHOICE PARAMETERS ###

# Destination choice (generated 2.9.2024)
"""
destination_choice: Dict[str, Dict[str, Dict[str, Any]]] = {
    "hw": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.343374988523,
            },
            "impedance": {
                "time": (-0.0132535252, -0.0180517183),
                "cost": (-0.1004054942, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518),
                        numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487),
                                   numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.491418509053, 0.491418509053),
            },
            "impedance": {
                "time": -0.0101838292646,
                "cost": (-0.100405494227, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518), numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487), numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.11623384398, -1.3592708114),
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518), numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487), numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.15046600566, -2.08475720417),
            },
            "impedance": {},
            "log": {
                "dist": -2.66277304293,
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "cbd": (numpy.exp(4.6880073518), numpy.exp(5.43822704609)),
                "workplaces_own": (numpy.exp(0.314367891487), numpy.exp(0.906947845409)),
                "workplaces_other": 1,
            },
        },
    },
    "hc": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": -0.418311339830e-1,
            },
            "log": {
                "transform": -2.31917697254,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
            "transform": {
                "attraction":{
                    "parking_cost_errand": 1,
                },
                "impedance": {
                    "cost": 1,
                },
            }
        },
        "transit": {
            "attraction": {
                "own_zone_area_sqrt": -1.40415965463,
                "cbd": (0.704345842211, 0.704345842211),
                "helsinki_other": (0.50, 0.20),
            },
            "impedance": {
                "time": -0.245629127645e-1,
            },
            "log": {
                "transform": -2.31917697254,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
            "transform": {
                "attraction": {},
                "impedance": {
                    "cost": (1.0, 1.0),
                },
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": -2.04456095712,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-3.87680793384 + 0.10,
                                       -3.87680793384 - 2.00),
            },
            "impedance": {},
            "log": {
                "dist": -4.89065780132,
                "size": 1.00000000000,
            },
            "size": {
                "comprehensive_schools": 1,
            },
        },
    },
    "hu": {
        "car": {
            "attraction": {
                "parking_cost_work": (-0.357366885936,
                                      -0.357366885936),
            },
            "impedance": {
                "time": -0.0297120650,
                "cost": -0.225091401758,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.145828916891, 0.145828916891),
            },
            "impedance": {
                "time": (-0.0135191971654, -0.0135191971654),
                "cost": (-0.225091401758, -0.225091401758),
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {
            },
            "log": {
                "dist": (-1.70901466021, -1.70901466021),
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": -2.28428769533,
            },
            "impedance": {},
            "log": {
                "dist": -3.32824531424 + 0.00,
                "size": 1.00000000000,
            },
            "size": {
                "secondary_schools": numpy.exp(-1.22536093464),
                "tertiary_education": 1,
            },
        },
    },
    "hs": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.198005522852,
            },
            "impedance": {
                "time": -0.0427449023,
                "cost": -0.477596673469,
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (0.194157681759 + 0.00, 4.25838834127 + 0.00),
                "helsinki_other": (0.00, 0.00),
            },
            "impedance": {
                "time": -0.0268255591268,
                "cost": -0.477596673469,
            },
            "log": {
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.95518149948, -1.67112409733),
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-3.46874228834 - 0.70, 
                                       -4.72081529262 - 1.20),
                "population_density": 0.0000215025563001,
            },
            "impedance": {},
            "log": {
                "dist": -4.00475528272,
                "size": 1.00000000000,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.54407400279),
                "shops_other": numpy.exp(6.34839288971),
                "shops_own": (numpy.exp(5.90300326341), 
                              numpy.exp(6.98452705435)),
                "service_other": numpy.exp(3.80218657061),
                "service_own": (numpy.exp(4.399261887),
                                numpy.exp(5.06426205412)),
                "cbd": (numpy.exp(8.92119753904),
                        numpy.exp(7.17315876803)),
            },
        },
    },
    "ho": {
        "car": {
            "attraction": {
                "own_zone": 0.642829705544,
                "parking_cost_errand": -.271848312580,
            },
            "impedance": {
                "time": -0.0195496488,
                "cost": -.218431829623,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
        "transit": {
            "attraction": {
                "own_zone": -1.99877035216,
                "cbd": 0.637633920546,
            },
            "impedance": {
                "time": -0.0163548606161,
                "cost": -0.218431829623,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.83301197674, -1.64746747645),
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.13782241032 + 0.00,
                                       -1.00451024484 + 0.00),
                "population_density": -0.423271371798E-04,
            },
            "impedance": {},
            "log": {
                "dist": -3.69672461344,
                "size": 1,
            },
            "size": {
                "population_other": 1,
                "population_own": numpy.exp(1.36533858970),
                "service_other": numpy.exp(2.39351567744),
                "service_own": numpy.exp(3.35003762339),
                "shops": numpy.exp(3.10201560094),
                "cbd": (numpy.exp(7.82599214329),
                        numpy.exp(4.95459142492)),
            },
        },
    },
    "hoo": {
        "car": {
            "attraction": {
                "own_zone": (1.511261249, 0.496255377),
                "parking_cost_errand": -0.110043052,
            },
            "impedance": {
                "time": -0.121821884,
                "cost": -0.071273703,
            },
            "log": {
                "size": 0.635546074,
            },
            "size": {
                "population": 1,
                "service": numpy.exp(3.359535766),
                "shops": numpy.exp(5.054869817),
                "cbd": numpy.exp(5.497881457),
            },
        },
        "transit": {
            "attraction": {
                "own_zone": (1.138959644, -0.582370838),
            },
            "impedance": {
                "time": -0.054854548,
                "cost": -0.071273703,
            },
            "log": {
                "size": 0.564060942,
            },
            "size": {
                "population": 1,
                "service": numpy.exp(3.171875158),
                "shops": numpy.exp(5.513706147),
            },
        },
        "bike": {
            "attraction": {
                "own_zone": (1.254997132, 0.698948786),
            },
            "impedance": {
                "dist": -0.575044482,
            },
            "log": {
                "size": 0.698342216,
            },
            "size": {
                "population": 1,
                "service": numpy.exp(1.455295457),
                "shops": numpy.exp(3.2502116),
            },
        },
    },
    "wo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -.291338216556,
            },
            "impedance": {
                "time": -0.0371080433,
                "cost": -.281121539905,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": .350354942258,
                "own_zone": -1.87675547285,
            },
            "impedance": {
                "time": -.0190572340198,
                "cost": -.281121539905,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.05206422461, -1.82198542728),
                "size": 1,
            },
           "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.10044318679, -1.94548368752),
            },
            "impedance": {},
            "log": {
                "dist": -3.38855455974,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
    },
    "oo": {
        "car": {
            "attraction": {
                "parking_cost_errand": -.291338216556,
            },
            "impedance": {
                "time": -0.0371080433 + 0.00,
                "cost": -.281121539905 + 0.00,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "transit": {
            "attraction": {
                "cbd": .350354942258 + 0.00,
                "own_zone": -1.87675547285 + 0.00,
            },
            "impedance": {
                "time": -.0190572340198,
                "cost": -.281121539905,
            },
            "log": {
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-2.05206422461, -1.82198542728),
                "size": 1,
            },
           "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-1.10044318679, -1.94548368752),
            },
            "impedance": {},
            "log": {
                "dist": -3.38855455974,
                "size": 1,
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(.400884483384),
                "service": numpy.exp(1.58922222310),
                "shops_cbd": numpy.exp(3.58798748920),
                "shops_elsewhere": numpy.exp(3.36839356543),
                "own_zone": (numpy.exp(6.94153078815),
                             numpy.exp(6.94153078815)),
            },
        },
    },
    "wh": {
        "car": {
            "attraction": {},
            "impedance": {
                "time": (-0.0132535252, -0.0180517183),
                "cost": (-0.1004054942, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.0101838292646,
                "cost": (-0.100405494227, -0.136755441374),
            },
            "log": {
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
        "bike": {
            "attraction": {},
            "impedance": {},
            "log": {
                "dist": (-1.11623384398, -1.3592708114),
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
        "walk": {
            "attraction": {
                "own_zone_area_sqrt": (-2.15046600566, -2.08475720417),
            },
            "impedance": {},
            "log": {
                "dist": -2.66277304293,
                "size": 1.00000000000, # L_S_M
            },
            "size": {
                "population_own": numpy.exp(0.314367891487),
                "population_other": 1,
            },
        },
    },
    "hwp": {
        "car": {
            "attraction": {
                "parking_cost_work": -0.157123873740,
                "share_detached_houses": 0.580974879625,
                "own_zone_area": -0.0205161484737 - 0.020,
            },
            "impedance": {
                "time": -0.0207403513,
                "cost": -0.157123873740,
            },
            "log": {
                "size": 0.906942834933, # LN_Size
            },
            "size": {
                "workplaces": 1,
            },
        },
        "transit": {
            "attraction": {
                "cbd": 0.460082225170,
                "own_zone_area": -0.113153242090,
            },
            "impedance": {
                "time": -0.824400763002E-02,
                "cost": (-0.157123873740),
            },
            "log": {
                "size": 0.906942834933, # LN_Size
            },
            "size": {
                "workplaces": 1,
            },
        },
    },
    "hop": {
        "car": {
            "attraction": {
                "car_density": 1000 * 0.190087895761E-02,
                "own_zone_area": -0.914703619822E-02,
            },
            "impedance": {
                "time": -0.0207498305,
                "cost": -.231841682005,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.23033343181),
                "service": numpy.exp(4.63048603927),
                "shops": numpy.exp(5.40401631191),
                "comprehensive_schools": numpy.exp(2.38807154465),
                "population_own": numpy.exp(3.32704971816),
                "population_other": 1,
            },
        },
        "transit": {
            "attraction": {},
            "impedance": {
                "time": -0.503184346810E-02,
                "cost": (-0.231841682005 - 0.00),
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "workplaces": numpy.exp(1.23033343181),
                "service": numpy.exp(4.63048603927),
                "shops": numpy.exp(5.40401631191),
                "comprehensive_schools": numpy.exp(2.38807154465),
                "population_own": numpy.exp(3.32704971816),
                "population_other": 1,
            },
        },
    },
    "sop": {
        "logsum": {
            "attraction": {
                "own_zone": 0.491757816367,
            },
            "impedance": {},
            "log": {
                "logsum": 0.852698948873,
                "size": 0.824476718431,
            },
            "size": {
                "workplaces": numpy.exp(3.93387218470),
                "population_own": numpy.exp(3.04338951027),
                "population_other": 1.0,
            },
        },
    },
    "oop": {
        "car": {
            "attraction": {
                "parking_cost_errand": -0.227398812175,
            },
            "impedance": {
                "time": (-0.427365675012e-1,
                         -0.427365675012e-1 - 0.005),
                "cost": -0.227398812175,
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(1.26651176555),
                "shops_cbd": (numpy.exp(4.08944842667 - 3.0),
                              numpy.exp(4.08944842667 + 2.0)),
                "shops_elsewhere": numpy.exp(2.62226008068),
            },
        },
        "transit": {
            "attraction": {
                "cbd": (2.84600723332 - 1.0,
                        2.84600723332 + 2.0),
            },
            "impedance": {
                "time": -0.819579857062e-2,
                "cost": (-0.227398812175 - 0.2,
                         -0.227398812175 - 0.2),
            },
            "log": {
                "size": 1, # L_S_M
            },
            "size": {
                "population": 1,
                "workplaces": numpy.exp(1.26651176555),
                "shops_cbd": numpy.exp(4.08944842667),
                "shops_elsewhere": numpy.exp(2.62226008068),
            },
        },
    },
}
destination_end = """
# Maximum possible distance to destination
distance_boundary = {
    "car": 9999,
    "transit": 9999,
    "bike": 60,
    "walk": 15,
    "park_and_ride": 9999,
}
# O-D pairs with demand below threshold are neglected in sec dest calculation
secondary_destination_threshold = 0.1
"""

modes_beginning="""
### MODE CHOICE PARAMETERS ###

# Mode choice (generated 2.9.2024)
from typing import Any, Dict, Optional

"""
mode_choice: Dict[str, Optional[Dict[str, Dict[str, Any]]]] = {
    "hw": {
        "car": {
            "constant": (0.830938747727 * (0 + 0.278), 
                         0.830938747727 * (0 + 0.251)),
            "generation": {
                "car_density": (0.830938747727 * 1000 * 0.00282859274412, 0.830938747727 * 1000 * 0.00453019737785),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {
                "car_users": (0.830938747727 * 3.03999716806, 0.830938747727 * 2.95110380739),
            },
        },
        "transit": {
            "constant": (0.830938747727 * (3.35620148087 - 0.107), 
                         0.830938747727 * (3.35324641782 - 0.527)),
            "generation": {
                "cbd": 0.40,
                "helsinki_other": -0.10,
                "espoo_vant_kau": -0.30,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.830938747727 * (3.80657808148 - 0.017), 
                         0.830938747727 * (4.31992749379 + 0.033)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.830938747727 * (6.19979345573 + 0.040),
                         0.830938747727 * (6.52578316385 - 0.421)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
    },
    "hc": {
        "car": {
            "constant": (0.272803753976 * (0 + 0.684),
                         0.272803753976 * (0 - 0.697)),
            "generation": {
                "car_density": 0.272803753976 * 1000 * 0.201094997058e-01,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.272803753976 * (13.2817160786 + 0.077),
                         0.272803753976 * (13.2817160786 - 0.734)),
            "generation": {
                "cbd": 0.3,
                "helsinki_other": 0.3,
                "espoo_vant_kau": -0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.272803753976 * (11.3490028510 + 0.163),
                         0.272803753976 * (11.3490028510 + 2.018)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.272803753976 * (17.7784859496 + 0.033),
                         0.272803753976 * (17.7784859496 - 1.254)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.272803753976, # Dcoeff
            },
            "individual_dummy": {},
        },
    },
    "hu": {
        "car": {
            "constant": (0 - 0.315, 0 + 0.675),
            "generation": {
                "car_density": 1000 * 0.504851816443e-2,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (3.12509878421 + 0.053, 3.12509878421 + 0.468),
            "generation": {
                "cbd": 0.5,
                "helsinki_other": 0.1,
                "espoo_vant_kau": -0.7,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (3.24451960342 + 0.379, 3.24451960342 + 1.910),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (6.16685830247 + 0.493, 6.16685830247 + 1.253), 
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
    },
    "hs": {
        "car": {
            "constant": (0.522036062262 * (0 + 0.323), 
                         0.522036062262 * (0 + 0.189)),
            "generation": {
                "car_density": (0.522036062262 * 1000 * 0.00996637488914, 0.522036062262 * 1000 * 0.0166093327868),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262, # Dcoeff
            },
            "individual_dummy": {
                "car_users": (0.522036062262 * 4.50826448347, 0.522036062262 * 3.60490124299),
            },
        },
        "transit": {
            "constant": (0.522036062262 * (6.72180796903 + 0.158), 
                         0.522036062262 * (6.67197643351 - 0.399)),
            "generation": {
                "espoo_vant_kau": -0.3,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.522036062262 * (4.3562332376 + 0.307), 
                         0.522036062262 * (7.8358175344 + 0.210)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.522036062262 * (11.3353754845 + 0.065),
                         0.522036062262 * (13.3431291443 + 0.068)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.522036062262,
            },
            "individual_dummy": {},
        },
    },
    "ho": {
        "car": {
            "constant": (0.157371648547 * (0 - 0.280),
                         0.157371648547 * (0 - 0.130)),
            "generation": {
                "car_density": (0.157371648547 * 1000 * 0.0275157057103, 0.157371648547 * 1000 * 0.00903883238252),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {
                "car_users": (0.157371648547 * 4.43378318532, 0.157371648547 * 2.98838274317),
            },
        },
        "transit": {
            "constant": (0.157371648547 * (8.33856436370 - 0.380), 
                         0.157371648547 * (-9.21721208402 - 0.258)),
            "generation": {
                "cbd": 0.2,
                "espoo_vant_kau": -0.8,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.157371648547 * (5.65570738596 - 0.113), 
                         0.157371648547 * (-.549035575271 + 0.374)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (0.157371648547 * (20.8216972704 - 0.450), 
                         0.157371648547 * (12.5696379434 - 0.134)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.157371648547,
            },
            "individual_dummy": {},
        },
    },
    "hh": {
        "car": {
            "constant": -4.193566283037721,
            "generation": {
            },
            "individual_dummy": {
            },
            "log": {
            },

            "attraction": {
            },
            "impedance": {

            }
        },
        "transit": {
            "constant": -6.219339088071782,
            "log": {
            },
            "generation": {
            },
            "attraction": {
                #left empty on purpose
            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "bike": {
            "constant": -3.557848140624303,
            "log": {
            },
            "generation": {
            },
            "attraction": {
            },
            "impedance": {

            },
            "individual_dummy": {

            }
        },
        "walk": {
            "constant": -0.06238631413467127,
            "log": {
            },
            "generation": {

            },
            "attraction": {
            },
            "impedance": {

            },
            "individual_dummy": {

            }
        }
    },
    "hoo": None,
    "wo": {
       "car": {
            "constant": (.718153936654 * (0 + 0.520),
                         .718153936654 * (0 + 1.112)),
            "generation": {
                "car_density": (.718153936654 * 1000 * .00281255180930, .718153936654 * 1000 * .00306776772245),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (.718153936654 * (1.47963675807 - 0.168),
                         .718153936654 * (1.47963675807 - 3.635)),
            "generation": {
                "cbd": 0.9,
                "helsinki_other": -0.1,
                "espoo_vant_kau": -0.9,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (.718153936654 * (-.346070374291 + 1.601),
                         .718153936654 * (.0632569112049 - 0.280)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (.718153936654 * (5.72318117910 + 0.522),
                         .718153936654 * (5.72318117910 - 0.368)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
    },
    "oo": {
        "car": {
            "constant": (.718153936654 * (0 - 0.094),
                         .718153936654 * (0 + 0.030)),
            "generation": {
                "car_density": (.718153936654 * 1000 * .00281255180930, .718153936654 * 1000 * .00306776772245),
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (.718153936654 * (1.47963675807 + 0.894),
                         .718153936654 * (1.47963675807 + 0.242)),
            "generation": {
                "cbd": 0.2,
                "helsinki_other": -0.4,
                "espoo_vant_kau": -0.4,
            },
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (.718153936654 * (-.346070374291 - 0.323),
                         .718153936654 * (.0632569112049 + 1.241)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        }, 
        "walk": {
            "constant": (.718153936654 * (5.72318117910 + 0.464),
                         .718153936654 * (5.72318117910 + 0.867)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": .718153936654,
            },
            "individual_dummy": {},
        },
    },
    "wh": {
        "car": {
            "constant": (0.830938747727 * (0 + 0.278), 
                         0.830938747727 * (0 + 0.251)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.830938747727 * (3.35620148087 - 0.107), 
                         0.830938747727 * (3.35324641782 - 0.527)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "bike": {
            "constant": (0.830938747727 * (3.80657808148 - 0.017), 
                         0.830938747727 * (4.31992749379 + 0.033)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
        "walk": {
            "constant": (0.830938747727 * (6.19979345573 + 0.040),
                         0.830938747727 * (6.52578316385 - 0.421)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.830938747727,
            },
            "individual_dummy": {},
        },
    },
    "hwp": {
        "car": {
            "constant": (0 + 0.024),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (-1.83293849298 - 0.199), # T_const
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000, # Dcoeff
            },
            "individual_dummy": {},
        },
    },
    "hop": {
        "car": {
            "constant": (0 + 0.075),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (-1.02607987269 - 0.075),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 1.00000000000,
            },
            "individual_dummy": {},
        },
    },
    "sop": {
        "car": {
            "constant": 0.0,
            "generation": {},
            "attraction": {
                "own_zone_area": -0.01478815,
                "parking_cost_work": -0.154340268,
            },
            "impedance": {
                "time": -0.021262374,
                "cost": -0.154340268,
            },
            "log": {},
            "individual_dummy": {},
        },
        "transit": {
            "constant": -2.060141017,
            "generation": {},
            "attraction": {
                "own_zone_area": -0.115937409151,
            },
            "impedance": {
                "time": -0.007909217,
                "cost": -0.154340268 / 30.0,
            },
            "log": {},
            "individual_dummy": {},
        },
    },
    "oop": {
        "car": {
            "constant": (0.715272183645 * (0 + 0.135)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.715272183645,
            },
            "individual_dummy": {},
        },
        "transit": {
            "constant": (0.715272183645 * (-3.44371464477 + 0.243)),
            "generation": {},
            "attraction": {},
            "impedance": {},
            "log": {
                "logsum": 0.715272183645,
            },
            "individual_dummy": {},
        },
    },
}

def insert_param(tdict, param, map, model_system_ttype, universal=""):
    #insert param with tuple address into correct position in the nested dict
    #tdict is the dictionary to be filled with model_system_ttype data with map[param] mapping
    #for universal recursion is used to assign the same param to all modes
    all_modes = ["car","transit","bike","walk"]
    if any(["PR" in param for param in model_system_ttype]): #check if any param has PR in it (Park and Ride)
        all_modes.append("park_and_ride")

    if param[0] == "universal":
        for mode in all_modes:
            if len(param) == 2:
                nparam = (mode,param[1])
            if len(param) == 3:
                nparam = (mode,param[1],param[2])
            insert_param(tdict, nparam, map, model_system_ttype, universal="universal")
    elif param[0] == "ct":
        for mode in ["car","transit"]:
            if len(param) == 2:
                nparam = (mode,param[1])
            if len(param) == 3:
                nparam = (mode,param[1],param[2])
            insert_param(tdict, nparam, map, model_system_ttype, universal="ct")
    else:
        deepest_level_dict = tdict 
        for p in range(len(param)-1):
            if len(param)>p:
                if param[p] not in deepest_level_dict:
                    deepest_level_dict[param[p]]={}
                deepest_level_dict = deepest_level_dict[param[p]]
        if universal!="":
            if len(param) == 2:
                deepest_level_dict[param[-1]] = map[(universal,param[1])]
            if len(param) == 3:
                deepest_level_dict[param[-1]] = map[(universal,param[1],param[2])]
        else:
            deepest_level_dict[param[-1]] = map[param]

def get_mode_param_map(mpa):
    param_map_mode = {}
    dcoeff = mpa["Dcoeff"]
    if "C_const" in mpa: param_map_mode[("car","constant")]=(mpa["C_const"]*dcoeff,mpa["C_const"]*dcoeff)
    if "C_Ocardns" in mpa: 
        param_map_mode[("car","generation", "car_density")]=(mpa['C_Ocardns']*1000*dcoeff,mpa['C_Ocardns']*1000*dcoeff)
        if "PR_const" in mpa:
            param_map_mode[("park_and_ride","generation", "car_density")]=(mpa['C_Ocardns']*1000*dcoeff,mpa['C_Ocardns']*1000*dcoeff)
    if "C_HAP" in mpa:
        param_map_mode[("car","individual_dummy","car_users")]=(mpa['C_HAP']*dcoeff,mpa['C_HAP']*dcoeff)
        if "PR_const" in mpa:
            param_map_mode[("park_and_ride","individual_dummy","car_users")]=(mpa['C_HAP']*dcoeff,mpa['C_HAP']*dcoeff)
    if "T_const" in mpa: param_map_mode[("transit","constant")]=(mpa["T_const"]*dcoeff,mpa["T_const"]*dcoeff)
    if "B_const" in mpa: param_map_mode[("bike","constant")]=(mpa["B_const"]*dcoeff,mpa["B_const"]*dcoeff)
    if "W_const" in mpa: param_map_mode[("walk","constant")]=(mpa["W_const"]*dcoeff,mpa["W_const"]*dcoeff)
    if "PR_const" in mpa: param_map_mode[("park_and_ride","constant")]=(mpa["PR_const"]*dcoeff,mpa["PR_const"]*dcoeff)
    if "T_acc" in mpa: param_map_mode[("transit","generation","hw_t")]=(mpa["T_acc"]*dcoeff,mpa["T_acc"]*dcoeff)
    param_map_mode[("universal","log","logsum")]=dcoeff
    # #calibration
    # if "Cal_W_const_EV" in mpa: 
    #     param_map_mode[("walk","generation","espoo_vant_kau")]=(mpa["Cal_W_const_EV"]*dcoeff,mpa["Cal_W_const_EV"]*dcoeff)
    # if "Cal_W_const_kuuma" in mpa: 
    #     if ("walk","constant") in param_map_mode:
    #         param_map_mode[("walk","constant")]=(param_map_mode[("walk","constant")][0],param_map_mode[("walk","constant")][1]+mpa["Cal_W_const_kuuma"]*dcoeff)
    # if "Cal_B_const" in mpa: 
    #     if ("bike","constant") in param_map_mode:
    #         param_map_mode[("bike","constant")]=(param_map_mode[("bike","constant")][0]+mpa["Cal_B_const"]*dcoeff,
    #                                                 param_map_mode[("bike","constant")][1]+mpa["Cal_B_const"]*dcoeff)
    #     else:
    #         param_map_mode[("bike","constant")]=(mpa["Cal_B_const"]*dcoeff,
    #                                                 mpa["Cal_B_const"]*dcoeff)
    # if "Cal_B_const_kuuma" in mpa: 
    #     if ("bike","constant") in param_map_mode:
    #         param_map_mode[("bike","constant")]=(param_map_mode[("bike","constant")][0],param_map_mode[("bike","constant")][1]+mpa["Cal_B_const_kuuma"]*dcoeff)
    # if "Cal_B_const_cbd" in mpa: 
    #     param_map_mode[("bike","generation","cbd")]=(mpa["Cal_B_const_cbd"]*dcoeff,mpa["Cal_B_const_cbd"]*dcoeff)
    # if "Cal_B_const_helsinki" in mpa: 
    #     param_map_mode[("bike","generation","cbd")]=(mpa["Cal_B_const_helsinki"]*dcoeff,mpa["Cal_B_const_helsinki"]*dcoeff)
    #     param_map_mode[("bike","generation","helsinki_other")]=(mpa["Cal_B_const_helsinki"]*dcoeff,mpa["Cal_B_const_helsinki"]*dcoeff)
    # if "Cal_B_const_EV" in mpa: 
    #     param_map_mode[("bike","generation","espoo_vant_kau")]=(mpa["Cal_B_const_EV"]*dcoeff,mpa["Cal_B_const_EV"]*dcoeff)
    # if "Cal_T_const" in mpa: 
    #     if ("transit","constant") in param_map_mode:
    #         param_map_mode[("transit","constant")]=(param_map_mode[("transit","constant")][0]+mpa["Cal_T_const"]*dcoeff,
    #                                                 param_map_mode[("transit","constant")][1]+mpa["Cal_T_const"]*dcoeff)
    #     else:
    #         param_map_mode[("transit","constant")]=(mpa["Cal_T_const"]*dcoeff,mpa["Cal_T_const"]*dcoeff)
    # if "Cal_T_const_kuuma" in mpa: 
    #     if ("transit","constant") in param_map_mode:
    #         param_map_mode[("transit","constant")]=(param_map_mode[("transit","constant")][0],param_map_mode[("transit","constant")][1]+mpa["Cal_T_const_kuuma"]*dcoeff)
    # if "Cal_T_const_cbd" in mpa: 
    #     param_map_mode[("transit","generation","cbd")]=(mpa["Cal_T_const_cbd"]*dcoeff,mpa["Cal_T_const_cbd"]*dcoeff)
    # if "Cal_T_const_EV" in mpa: 
    #     param_map_mode[("transit","generation","espoo_vant_kau")]=(mpa["Cal_T_const_EV"]*dcoeff,mpa["Cal_T_const_EV"]*dcoeff)
    # if "Cal_C_const" in mpa: 
    #     if ("car","constant") in param_map_mode:
    #         param_map_mode[("car","constant")]=(param_map_mode[("car","constant")][0]+mpa["Cal_C_const"]*dcoeff,
    #                                                 param_map_mode[("car","constant")][1]+mpa["Cal_C_const"]*dcoeff)
    #     else:
    #         param_map_mode[("car","constant")]=(mpa["Cal_C_const"]*dcoeff,
    #                                                 mpa["Cal_C_const"]*dcoeff)
    # if "Cal_C_const_cbd" in mpa: 
    #     param_map_mode[("car","generation","cbd")]=(mpa["Cal_C_const_cbd"]*dcoeff,mpa["Cal_C_const_cbd"]*dcoeff)
    # if "Cal_C_const_pks" in mpa: 
    #     if ("car","constant") in param_map_mode:
    #         param_map_mode[("car","constant")]=(param_map_mode[("car","constant")][0]+mpa["Cal_C_const_pks"]*dcoeff,
    #                                                 param_map_mode[("car","constant")][1])
    #     else:
    #         param_map_mode[("car","constant")]=(mpa["Cal_C_const"]*dcoeff,
    #                                                 mpa["Cal_C_const"]*dcoeff)
    # if "Cal_C_const_kuuma" in mpa: 
    #     if ("car","constant") in param_map_mode:
    #         param_map_mode[("car","constant")]=(param_map_mode[("car","constant")][0],param_map_mode[("car","constant")][1]+mpa["Cal_C_const_kuuma"]*dcoeff)
    # if "Cal_C_const_helsinki" in mpa: 
    #     param_map_mode[("car","generation","cbd")]=(mpa["Cal_C_const_helsinki"]*dcoeff,mpa["Cal_C_const_helsinki"]*dcoeff)
    #     param_map_mode[("car","generation","helsinki_other")]=(mpa["Cal_C_const_helsinki"]*dcoeff,mpa["Cal_C_const_helsinki"]*dcoeff)
    

    return param_map_mode
    
def get_dest_param_map(mpa, c_time):
    param_map_dest = {}
      
    if "C_wpark" in mpa: param_map_dest[("car","attraction","parking_cost_work")]=(mpa["C_wpark"],mpa["C_wpark"])
    if "C_opark" in mpa: param_map_dest[("car","attraction","parking_cost_errand")]=(mpa["C_opark"],mpa["C_opark"])
    if "CT_gen" in mpa and "C_time" not in mpa:
        param_map_dest[("car","impedance","time")]=(c_time*mpa["CT_gen"],c_time*mpa["CT_gen"])
    elif "C_time" in mpa:
        param_map_dest[("car","impedance","time")]=(mpa["C_time"],mpa["C_time"])
    if "CT_gen" in mpa: param_map_dest[("ct","impedance","cost")]=(mpa["CT_gen"],mpa["CT_gen"])
    if "CT_lnCosPO" in mpa: 
        param_map_dest[("ct","log","transform")] = mpa["CT_lnCosPO"]
        param_map_dest[("car","transform")]={
                "attraction":{
                    "parking_cost_errand": 1,
                },
                "impedance": {
                    "cost": 1,
                },
            }
        param_map_dest[("transit","transform")]={
                "attraction": {},
                "impedance": {
                    "cost": (1.0, 1.0),
                },
            }
        
    #if "C_wpark" in mpa: param_map_dest[("transit","attraction")]={}
    if "T_time" in mpa: param_map_dest[("transit","impedance","time")]=mpa["T_time"]
    if "T_downtown" in mpa: param_map_dest[("transit","attraction","cbd")]=mpa["T_downtown"]
    if "T_sameOz" in mpa: param_map_dest[("transit","attraction","own_zone")]=mpa["T_sameOz"]
    #if "C_wpark" in mpa: param_map_dest[("bike","attraction")]={}
    if "B_Len" in mpa: param_map_dest[("bike","impedance","dist")]=mpa["B_Len"]
    if "B_time" in mpa: param_map_dest[("bike","impedance","time")]=mpa["B_time"]
    if "B_logtime" in mpa: param_map_dest[("bike","log","time")]=mpa["B_logtime"]
    if "B_wpark" in mpa: param_map_dest[("bike","attraction","parking_cost_work")]=(mpa["B_wpark"],mpa["B_wpark"])
    if "W_wpark" in mpa: param_map_dest[("walk","attraction","parking_cost_work")]=(mpa["W_wpark"],mpa["W_wpark"])
    if "T_wpark" in mpa: param_map_dest[("transit","attraction","parking_cost_work")]=(mpa["T_wpark"],mpa["T_wpark"])
    #if "C_wpark" in mpa: param_map_dest[("walk","attraction")]={}
    if "W_Len" in mpa: param_map_dest[("walk","impedance","dist")]=mpa["W_Len"]
    if "W_time" in mpa: param_map_dest[("walk","impedance","time")]=mpa["W_time"]
    if "W_logtime" in mpa: param_map_dest[("walk","log","time")]=mpa["W_logtime"]
    if "W_ODpopd" in mpa: param_map_dest[("walk","attraction","population_density")]=mpa["W_ODpopd"]
    if "PR_gen" in mpa: param_map_dest[("park_and_ride","impedance","utility")]=mpa["PR_gen"]
    if "PR_dwntown" in mpa: param_map_dest[("park_and_ride","attraction","cbd")]=mpa["PR_dwntown"]
    if "PR_wpark" in mpa: param_map_dest[("park_and_ride","attraction","parking_cost_work")]=(mpa["PR_wpark"],mpa["PR_wpark"])
    if "PR_gen" in mpa:
        param_map_dest[("park_and_ride","utility")]={   
                "facility": {
                    "shops": 0.00001,
                    "cost": mpa["CT_gen"],
                    "time": c_time*mpa["CT_gen"]
                },
                "car_impedance": {
                    "time": c_time*mpa["CT_gen"],
                    "cost": mpa["CT_gen"]
                },
                "transit_impedance": {
                    "time": mpa["T_time"],
                    "cost": mpa["CT_gen"]
                }
            } 
    if "L_S_M" in mpa: param_map_dest[("universal","log","size")]=mpa["L_S_M"] #TODO: does not work, but is not really used in relevant models
    else:
        param_map_dest[("universal","log","size")]=1.0
    if "S_dwntwn" in mpa: param_map_dest[("universal","size","cbd")]=mpa["S_dwntwn"]
    if "S_jobs" in mpa: param_map_dest[("universal","size","workplaces")]=mpa["S_jobs"] #manually set in Excel to zero if equals one
    if "S_primary" in mpa: param_map_dest[("universal","size","comprehensive_schools")]=mpa["S_primary"] #manually set in Excel if equals one
    if "So_primary" in mpa: param_map_dest[("universal","size","comprehensive_schools_own")]=mpa["So_primary"] #manually set in Excel if equals one
    if "Sm_primary" in mpa: param_map_dest[("universal","size","comprehensive_schools_other")]=mpa["Sm_primary"] #manually set in Excel if equals one
    if "S_High" in mpa: param_map_dest[("universal","size","secondary_schools")]=mpa["S_High"] #manually set in Excel if equals one
    if "S_uni" in mpa: param_map_dest[("universal","size","tertiary_education")]=mpa["S_uni"] 
    if "S_pop" in mpa: param_map_dest[("universal","size","population")]=mpa["S_pop"] #manually set in Excel if equals one
    if "S_service" in mpa: param_map_dest[("universal","size","service")]=mpa["S_service"] 
    if "So_service" in mpa: param_map_dest[("universal","size","service_own")]=mpa["So_service"] 
    if "Sm_service" in mpa: param_map_dest[("universal","size","service_other")]=mpa["Sm_service"] 
    if "S_shops" in mpa: param_map_dest[("universal","size","shops")]=mpa["S_shops"] 
    if "S_area" in mpa: param_map_dest[("universal","size","zone_area")]=mpa["S_area"] 
    #secondary destionation model variables
    if "Cd_Time" in mpa: param_map_dest[("car","impedance","time")]=mpa["Cd_Time"]
    if "Cd_park" in mpa: param_map_dest[("car","attraction","parking_cost_errand")]=mpa["Cd_park"]
    if "Td_time" in mpa: param_map_dest[("transit","impedance","time")]=mpa["Td_time"]
    if "Bd_Len" in mpa: param_map_dest[("bike","impedance","dist")]=mpa["Bd_Len"]
    if "Wd_Len" in mpa: param_map_dest[("walk","impedance","dist")]=mpa["Wd_Len"] #not in use

    # #calibration
    # if "Cal_B_dwntwn" in mpa: #expects no prior definition
    #     param_map_dest[("bike","attraction","cbd")]=mpa["Cal_B_dwntwn"]
    # if "Cal_C_CT_gen" in mpa: #expects no prior definition
    #     param_map_dest[("car","impedance","time")]=(c_time*(mpa["Cal_C_CT_gen"]+mpa["CT_gen"]),c_time*(mpa["Cal_C_CT_gen"]+mpa["CT_gen"]))
    #     param_map_dest[("car","impedance","cost")]=(mpa["Cal_C_CT_gen"]+mpa["CT_gen"],mpa["Cal_C_CT_gen"]+mpa["CT_gen"])

    for k in param_map_dest:
        if k[1]=="size":
            param_map_dest[k] = np.exp(param_map_dest[k])

    return param_map_dest

#manually copied from alo files in ohjaus
c_time_work = 0.132
c_time_other = 0.0895
c_time_map = {
    "hw": c_time_work,
    "hc": c_time_work, #actually has its own
    "hu": c_time_work,
    "hs": c_time_other,
    "ho": c_time_other,
    "oo": c_time_other,
    "wo": c_time_other,
    "hoo": c_time_other,
}

if __name__ == "__main__":

    #sheet_name = sys.argv[1] # = 'mode_choice'

    # File paths
    model_system_petr_path = "C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/ohjaus/"
    excel_file_path_petr = "C:/Users/HajduPe/OneDrive - Helsingin Seudun liikenne - Kuntayhtymä/Estimointi/EstimointikoneHelmet5.xlsx"
    excel_file_path = excel_file_path_petr #'EstimointikoneHelmet5_esimerkki.xlsx'

    model_map = {
        "HS15 Koti-työ": "hw",
        "HS15 Koti-koulu": "hc",
        "HS15 Koti-opiskelu": "hu",
        "HS15 Koti-ostosAsiointi": "hs",
        "HS15 Koti-muu": "ho",
        "HS15 EKP": "oo",
        "HS15 EKP2": "wo",
        "HS15 2ST": "hoo",
        #"HS15 2SW": "hoo", #not in use
        "HS15 2SB": "hoo",
        "HS15 2SC": "hoo",
    }

    model_params_alogit = {}
    for sheet_name in model_map:
        if sheet_name == "HS15 EKP2": continue
        # Load the Excel file
        df = pd.read_excel(excel_file_path,
                        sheet_name=sheet_name,
                        engine='openpyxl'
                        )
        #df.reset_index()
        
            # Create dictionary object from dataframe
        key_value_dict = {}
        
        for i1, row in df.iterrows():
            coeff = str(row["Coeff"]).split("#")[0].split("=")[0]
            val = row["Start value"] #Fix this later?
            if coeff != "nan" and str(val) != "nan":
                key_value_dict[coeff] = val


        model_params_alogit[sheet_name] = key_value_dict

    model_params_alogit["HS15 EKP2"]=deepcopy(model_params_alogit["HS15 EKP"])
    print(model_params_alogit)
        
    
    #TODO: translate maps into attrs in dictionary

    for mpx in model_params_alogit:
        mx = model_map[mpx]
        dcx = destination_choice[mx]
        mcx = mode_choice[mx]
        model_system_ttype = model_params_alogit[mpx]
        if mx!="hoo": #not secondary destination model
            dcx.clear()
            mcx.clear()
        if mpx=="HS15 2ST": #first secondary destination only
            dcx.clear()

        
        param_map_dest = get_dest_param_map(model_system_ttype, c_time_map[mx])
        print("Model: ",mpx)
        if mx!="hoo":
            param_map_mode = get_mode_param_map(model_system_ttype)
            print("model: ",mx, len(model_system_ttype),"=",len(param_map_mode),"(mode) + ",len(param_map_dest), "(dest)")
            #insert mode params
            
            for pmm in param_map_mode:
                print("--->",pmm)
                insert_param(mcx, pmm, param_map_mode, model_system_ttype)
        #insert destination params
        for pmd in param_map_dest:
            print("-->",pmd)
            insert_param(dcx,pmd, param_map_dest, model_system_ttype)
            
        #mode_choice[mx] = {}
        
    

    for model in destination_choice:
        for mode in destination_choice[model]:
            if "attraction" not in destination_choice[model][mode]:
                destination_choice[model][mode]["attraction"] = {}

    for model in mode_choice:
        if mode_choice[model] == None: continue
        for mode in mode_choice[model]:
            if "constant" not in mode_choice[model][mode]:
                mode_choice[model][mode]["constant"] = (0.,0.)
            if "generation" not in mode_choice[model][mode]:
                mode_choice[model][mode]["generation"] = {}
            if "attraction" not in mode_choice[model][mode]:
                mode_choice[model][mode]["attraction"] = {}
            if "impedance" not in mode_choice[model][mode]:
                mode_choice[model][mode]["impedance"] = {}
            if "individual_dummy" not in mode_choice[model][mode]:
                mode_choice[model][mode]["individual_dummy"] = {}
    try:
        destination_choice["hoo"].pop("walk") #walk model is not used 
    except:
        pass
    destinations_file = [destination_beginning,
                         destination_choice,
                         destination_end]
    
    modes_file = [modes_beginning,
                  mode_choice,
                  ]

    # Create a new Python script to recreate the dictionary
    with open('C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/skriptit/generated/destinations_dict.py', 'w') as f:
        for text in destinations_file:
            if type(text) == dict:
                f.write(print_dict(destination_choice, "destination_choice"))
            else:
                f.write(text)

       # Create a new Python script to recreate the dictionary
    with open('C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/skriptit/generated/modes_dict.py', 'w') as f:
        for text in modes_file:
            if type(text) == dict:
                f.write(print_dict(mode_choice, "mode_choice"))
            else:
                f.write(text)
            
