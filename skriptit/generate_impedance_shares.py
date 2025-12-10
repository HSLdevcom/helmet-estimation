import pandas as pd
import numpy as np
import sys
import json
from functools import reduce
import operator
from typing import Any, Dict, Optional
import numpy # type: ignore

# adding Folder_2 to the system path
sys.path.insert(0, 'C:\\Users\\HajduPe\\helmet-model-system\\Scripts')

from parameters.departure_time import demand_share
from parameters.assignment import volume_factors,assignment_classes
from parameters.tour_generation import tour_generation

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

exp_start = """### IMPEDANCE TRANSFORMATION PARAMETERS ###

from typing import Dict, Tuple, Union


transit_trips_per_month: Dict[str,Dict[str,Union[Tuple[float],Tuple[float,float]]]] = {
    "metropolitan": {
        "work": (60.0, 44.0),
        "leisure": (30.0, 30.0),
    },
    "peripheral": {
        "work": (44.0,),
        "leisure": (30.0,),
    },
    "all": {
        "work": (60.0, 44.0),
        "leisure": (30.0, 30.0),
    },
}
"""

exp_end = """
### IMPEDANCE TRANSFORMATION REFERENCES ###

divided_classes = (
    "car",
    "transit",
)
"""

impedance_share = {
    "hw": {
        "car": {
            "aht": (0.746026, 0.015065),
            "pt":  (0.234217, 0.329877),
            "iht": (0.019757, 0.655057),
        },
        "transit": {
            "aht": (0.746026, 0.015065),
            "pt":  (0.234217, 0.329877),
            "iht": (0.019757, 0.655057),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hc": {
        "car": {
            "aht": (0.811476, 0.000687),
            "pt":  (0.178970, 0.719189),
            "iht": (0.009555, 0.280124),
        },
        "transit": {
            "aht": (0.811476, 0.000687),
            "pt":  (0.178970, 0.719189),
            "iht": (0.009555, 0.280124),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hu": {
        "car": {
            "aht": (0.485475, 0.010482),
            "pt":  (0.430205, 0.609424),
            "iht": (0.084320, 0.380094),
        },
        "transit": {
            "aht": (0.485475, 0.010482),
            "pt":  (0.430205, 0.609424),
            "iht": (0.084320, 0.380094),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hs": {
        "car": {
            "aht": (0.096467, 0.042198),
            "pt":  (0.642764, 0.712821),
            "iht": (0.260769, 0.244981),
        },
        "transit": {
            "aht": (0.096467, 0.042198),
            "pt":  (0.642764, 0.712821),
            "iht": (0.260769, 0.244981),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "ho": {
        "car": {
            "aht": (0.129790, 0.034834),
            "pt":  (0.573629, 0.778648),
            "iht": (0.296581, 0.186519),
        },
        "transit": {
            "aht": (0.129790, 0.034834),
            "pt":  (0.573629, 0.778648),
            "iht": (0.296581, 0.186519),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hoo": {
        # Only un-transposed afternoon matrices are used.
        # However, the secondary destination choice is done "backwards",
        # from destination 1 to origin.
        "car": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (1, 0),
        },
        "transit": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (1, 0),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (0, 0),
            "iht": (1, 0),
        },
    },
    "wo": {
        "car": {
            "aht": (0.060857, 0.131316),
            "pt":  (0.781535, 0.785023),
            "iht": (0.157608, 0.083661),
        },
        "transit": {
            "aht": (0.060857, 0.131316),
            "pt":  (0.781535, 0.785023),
            "iht": (0.157608, 0.083661),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "oo": {
        "car": {
            "aht": (0.129495, 0.055808),
            "pt":  (0.668475, 0.666841),
            "iht": (0.202030, 0.277352),
        },
        "transit": {
            "aht": (0.129495, 0.055808),
            "pt":  (0.668475, 0.666841),
            "iht": (0.202030, 0.277352),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "wh": {
        "car": {
            "aht": (0.015065, 0.746026),
            "pt":  (0.329877, 0.234217),
            "iht": (0.655057, 0.019757),
        },
        "transit": {
            "aht": (0.015065, 0.746026),
            "pt":  (0.329877, 0.234217),
            "iht": (0.655057, 0.019757),
        },
        "bike": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
        "walk": {
            "aht": (0, 0),
            "pt":  (1, 1),
            "iht": (0, 0),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.679006, 0.031175),
            "pt":  (0.296493, 0.356524),
            "iht": (0.024502, 0.612301),
        },
        "transit": {
            "aht": (0.679006, 0.031175),
            "pt":  (0.296493, 0.356524),
            "iht": (0.024502, 0.612301),
        },
    },
    "hop": {
        "car": {
            "aht": (0.223073, 0.032569),
            "pt":  (0.532323, 0.708387),
            "iht": (0.244604, 0.259044),
        },
        "transit": {
            "aht": (0.223073, 0.032569),
            "pt":  (0.532323, 0.708387),
            "iht": (0.244604, 0.259044),
        },
    },
    "sop": {
        "car": {
            "aht": (0.538281, 0.031605),
            "pt":  (0.369282, 0.465128),
            "iht": (0.092437, 0.503267),
        },
        "transit": {
            "aht": (0.538281, 0.031605),
            "pt":  (0.369282, 0.465128),
            "iht": (0.092437, 0.503267),
        },
    },
    "oop": {
        "car": {
            "aht": (0.183770, 0.071658),
            "pt":  (0.714281, 0.754509),
            "iht": (0.101948, 0.173833),
        },
        "transit": {
            "aht": (0.183770, 0.071658),
            "pt":  (0.714281, 0.754509),
            "iht": (0.101948, 0.173833),
        },
    },
}

path = "C:\\Users\\HajduPe\\helmet-data-preprocessing\\shares\\impedance_shares.csv"
df = pd.read_csv(path, sep=";",decimal=",")
print(df)

for model in impedance_share:
    if model in ["hoo","sop"]: continue
    for mode in impedance_share[model]:
        if mode in ["bike","walk"]: continue
        for tp in ["aht","pt","iht"]:
            if model == "wh":
                d1 = float(df.query("model_type == 'hw' & time_period == @tp & forward == False")["share"].iloc[0])
                d2 = float(df.query("model_type == 'hw' & time_period == @tp & forward")["share"].iloc[0])
            else:
                if len(df.query("model_type == @model & time_period == @tp & forward")) > 0:
                    d1 = float(df.query("model_type == @model & time_period == @tp & forward")["share"].iloc[0])
                else: 
                    d1 = 0
                if len(df.query("model_type == @model & time_period == @tp & forward == False")) > 0:
                    d2 = float(df.query("model_type == @model & time_period == @tp & forward == False")["share"].iloc[0])
                else:
                    d2 = 0

                # d1 = demand_share[model][mode][tp][0]*volume_factors[f"{mode}_{assignment_classes[model]}"][tp]
                # d2 = demand_share[model][mode][tp][1]*volume_factors[f"{mode}_{assignment_classes[model]}"][tp]
            impedance_share[model][mode][tp] = (d1,d2)

# for mode in volume_factors:
#     print(mode)
#     if mode in ["trailer_truck","truck","van","bus"]:continue
#     for period in ["aht","pt","iht"]:
#         #"transport_class";"scenario";"share"
#         if "work" in mode or "leisure" in mode:
#             print(df_tr_class.query(f"transport_class=='{mode}' & scenario=='{period}'"))
#             share = df_tr_class.query(f"transport_class=='{mode}' & scenario=='{period}'")["share"].item()
#             volume_factors[mode][period] = share
#         else:
#             print(df_mode.query(f"mode_name=='{mode}' & scenario=='{period}'"))
#             share = df_mode.query(f"mode_name=='{mode}' & scenario=='{period}'")["share"].item()
#             volume_factors[mode][period] = 1 / share

assignment_file = [exp_start,
                impedance_share,
                exp_end]


# Create a new Python script to recreate the dictionary
with open('C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/skriptit/generated/impedance_dict.py', 'w') as f:
    for text in assignment_file:
        if type(text) == dict:
            f.write(print_dict(impedance_share, "volume_factors"))
        else:
            f.write(text)