import pandas as pd
import numpy as np
import sys
import json
from functools import reduce
import operator

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
                return repr(value)

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

tour_combinations = {
# utility function 1
    0: {
        () : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_50-64": -0.305509545 ,
                "age_65-99":  0.597976527
            },
            "zone": {},
        },
# utility function 2
    },
    1: {
        ("hw",) : {
            "constant":   0.000000000 + 0.0210,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.1065,
                "age_30-49":  2.977241136 - 0.3498,
                "age_50-64":  2.018825449 - 0.1177,
                "age_65-99": -1.185980639 - 0.0771
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 3
        ("hc",) : {
            "constant":   3.308625072 + 0.0150,
            "individual_dummy": {
                "age_7-17":  0.000000000 - 0.0641
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 4
        ("hu",) : {
            "constant":   0.000000000 + 0.3000,
            "individual_dummy": {
                "age_18-29":  0.000000000 + 0.0653,
                "age_30-49": -1.586979829 - 0.0192,
                "age_50-64": -3.739206239 - 1.3644,
                "age_65-99": -3.636471246 - 0.5649
            },
            "zone": {
                "share_detached_houses": -0.5910000 ,
                "hu_t":  0.148402259
            },
        },
# utility function 5
        ("hs",) : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0600,
                "age_18-29":  0.632156675 + 0.2843,
                "age_30-49":  1.106558979 - 0.6505,
                "age_50-64":  0.636516485 - 0.0855,
                "age_65-99":  1.250192981 - 0.0811
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 6
        ("ho",) : {
            "constant":   0.811674639,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1096,
                "age_18-29":  0.000000000 + 0.0679,
                "age_30-49":  0.000000000 - 0.2390,
                "age_50-64":  0.000000000 - 0.1643,
                "age_65-99":  0.394182783 - 0.1262
            },
            "zone": {
                "share_detached_houses": -0.5910000
            },
        },
# utility function 7
    },
    2: {
        ("hw", "hw") : {
            "constant":  -6.702389265,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 1.0022,
                "age_30-49":  2.977241136 + 0.3275,
                "age_50-64":  2.018825449 - 0.1879,
                "age_65-99": -1.185980639 ,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 8
        ("hw", "hu") : {
            "constant":  -8.418852173 + 0.2000,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 0.4439,
                "age_30-49": -1.586979829 +  2.977241136 + 0.4961,
                "age_50-64": -3.739206239 +  2.018825449 + 1.6450,
                "age_65-99": -3.636471246  -1.185980639 ,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 9
        ("hw", "hs") : {
            "constant":  -5.468303413,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 - 0.1900,
                "age_30-49":  1.106558979 +  2.977241136 + 0.0878,
                "age_50-64":  0.636516485 +  2.018825449 - 0.1499,
                "age_65-99":  1.250192981  -1.185980639 - 0.6537,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 10
        ("hw", "ho") : {
            "constant":  -3.969665707,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.0229,
                "age_30-49":  2.977241136 + 0.0059,
                "age_50-64":  2.018825449 - 0.0759,
                "age_65-99":  0.394182783  -1.185980639 - 0.1253,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 11
        ("hc", "hc") : {
            "constant":  -2.189925729,
            "individual_dummy": {},
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 12
        ("hc", "hs") : {
            "constant":  -0.932031836,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0317,
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 13
        ("hc", "ho") : {
            "constant":   1.040646615,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.0322,
                "age_65-99":  0.394182783
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 14
        ("hu", "hs") : {
            "constant":  -5.264912587 + 0.0736,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.0197,
                "age_30-49":  1.106558979  -1.586979829 - 0.6757,
                "age_50-64":  0.636516485  -3.739206239 + 0.7197,
                "age_65-99":  1.250192981  -3.636471246 + 0.9990,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 15
        ("hu", "ho") : {
            "constant":  -4.133565561 + 0.0834,
            "individual_dummy": {
                "age_18-29":  0.000000000 + 0.2038,
                "age_30-49": -1.586979829 - 0.8545,
                "age_50-64": -3.739206239 + 0.2616,
                "age_65-99":  0.394182783  -3.636471246 - 0.3497,
                "car_users":  0.647176487
            },
            "zone": {
                "hu_t":  0.176002681 ,
                "ho_w":  0.249875934
            },
        },
# utility function 16
        ("hs", "hs") : {
            "constant":  -4.347727916,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.2125,
                "age_30-49":  1.106558979 + 0.3402,
                "age_50-64":  0.636516485 - 0.1912,
                "age_65-99":  1.250192981 - 0.0980,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 17
        ("hs", "ho") : {
            "constant":  -3.615413138,
            "individual_dummy": {
                "age_7-17":   0.000000000 + 0.1376,
                "age_18-29":  0.632156675 + 0.0695,
                "age_30-49":  1.106558979 - 0.2025,
                "age_50-64":  0.636516485 + 0.0648,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0123,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 18
        ("ho", "ho") : {
            "constant":  -2.954069138,
            "individual_dummy": {
                "age_7-17":   0.000000000 + 0.5035,
                "age_18-29":  0.000000000 - 0.1393,
                "age_30-49":  0.000000000 + 0.1371,
                "age_50-64":  0.000000000 - 0.2130,
                "age_65-99":  0.394182783 + 0.0096,
                "car_users":  0.647176487
            },
            "zone": {
                "ho_w":  0.249875934
            },
        },
# utility function 19
    },
    3: {
        ("hw", "hw", "ho") : {
            "constant":  -7.640316015,
            "individual_dummy": {
                "age_18-29":  2.306249018 ,
                "age_30-49":  2.977241136 - 0.4304,
                "age_50-64":  2.018825449 + 0.6609,
                "age_65-99":  0.394182783  -1.185980639 + 2.8800,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 20
        ("hw", "hs", "hs") : {
            "constant":  -6.996908123,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 - 0.7910,
                "age_30-49":  1.106558979 +  2.977241136 + 0.4528,
                "age_50-64":  0.636516485 +  2.018825449 - 0.2617,
                "age_65-99":  1.250192981  -1.185980639  - 0.2451,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 21
        ("hw", "hs", "ho") : {
            "constant":  -6.280857590,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 + 0.2580,
                "age_30-49":  1.106558979 +  2.977241136 + 0.1582,
                "age_50-64":  0.636516485 +  2.018825449 + 0.1107,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 + 0.4486,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 22
        ("hw", "ho", "ho") : {
            "constant":  -5.143814369,
            "individual_dummy": {
                "age_18-29":  2.306249018 - 0.2782,
                "age_30-49":  2.977241136 + 0.3222,
                "age_50-64":  2.018825449 + 0.0418,
                "age_65-99":  0.394182783  -1.185980639 + 0.7158,
                "car_users":  1.492056593
            },
            "zone": {},
        },
# utility function 23
        ("hc", "hs", "ho") : {
            "constant":  -1.110080901,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1097,
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 24
        ("hc", "ho", "ho") : {
            "constant":   0.000000000,
            "individual_dummy": {
                "age_7-17":   0.000000000 - 0.1805,
                "age_65-99":  0.394182783
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 25
        ("hu", "hs", "ho") : {
            "constant": -11.751808160,
            "individual_dummy": {
                "age_18-29":  0.632156675 + 0.1437,
                "age_30-49":  1.106558979  -1.586979829 + 0.8652,
                "age_50-64":  0.636516485  -3.739206239 + 0.9321,
                "age_65-99":  1.250192981 +  0.394182783  -3.636471246 - 1.8292,
                "car_users":  1.492056593
            },
            "zone": {
                "hu_t":  0.829445548 ,
                "ho_w":  0.025800000
            },
        },
# utility function 26
        ("hu", "ho", "ho") : {
            "constant": -11.342729830,
            "individual_dummy": {
                "age_18-29": -0.000000000 + 0.1541,
                "age_30-49": -1.586979829 + 0.5275,
                "age_50-64": -3.739206239 - 0.7142,
                "age_65-99":  0.394182783  -3.636471246 ,
                "car_users":  1.492056593
            },
            "zone": {
                "hu_t":  0.829445548 ,
                "ho_w":  0.025800000
            },
        },
# utility function 27
        ("hs", "hs", "hs") : {
            "constant":  -5.575050535,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 2.3203,
                "age_30-49":  1.106558979 + 0.9194,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 - 0.2474,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 28
        ("hs", "hs", "ho") : {
            "constant":  -4.709369964,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.7508,
                "age_30-49":  1.106558979 + 0.5842,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783 + 0.1375,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 29
        ("hs", "ho", "ho") : {
            "constant":  -4.115616267,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.1442,
                "age_30-49":  1.106558979 ,
                "age_50-64":  0.636516485 + 0.3212,
                "age_65-99":  1.250192981 +  0.394182783 + 0.1907,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 30
        ("ho", "ho", "ho") : {
            "constant":  -4.110394781,
            "individual_dummy": {
                "age_30-49":  0.000000000 - 0.1750,
                "age_50-64":  0.000000000 + 0.1126,
                "age_65-99":  0.394182783 + 0.3557,
                "car_users":  1.492056593
            },
            "zone": {
                "ho_w":  0.025800000
            },
        },
# utility function 31
    },
    4: {
        ("hw", "hs", "hs", "ho") : {
            "constant":  -8.782904966,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 ,
                "age_30-49":  1.106558979 +  2.977241136 + 0.2190,
                "age_50-64":  0.636516485 +  2.018825449 + 0.7268,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 32
        ("hw", "hs", "ho", "ho") : {
            "constant":  -7.819600775,
            "individual_dummy": {
                "age_18-29":  0.632156675 +  2.306249018 + 0.5615,
                "age_30-49":  1.106558979 +  2.977241136 + 0.2939,
                "age_50-64":  0.636516485 +  2.018825449 + 0.1404,
                "age_65-99":  1.250192981 +  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 33
        ("hw", "ho", "ho", "ho") : {
            "constant":  -6.323991971,
            "individual_dummy": {
                "age_18-29":  2.306249018 + 0.3338,
                "age_30-49":  2.977241136 ,
                "age_50-64":  2.018825449 + 0.4624,
                "age_65-99":  0.394182783  -1.185980639 ,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 34
        ("hs", "hs", "hs", "hs") : {
            "constant":  -6.563838110,
            "individual_dummy": {
                "age_18-29":  0.632156675 ,
                "age_30-49":  1.106558979 + 1.11106,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 - 0.6711,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 35
        ("hs", "hs", "hs", "ho") : {
            "constant":  -6.280534875,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 1.3263,
                "age_30-49":  1.106558979 + 0.9876,
                "age_50-64":  0.636516485 ,
                "age_65-99":  1.250192981 +  0.394182783 - 0.3030,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 36
        ("hs", "hs", "ho", "ho") : {
            "constant":  -5.728407971,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.8239,
                "age_30-49":  1.106558979 + 0.4522,
                "age_50-64":  0.636516485 + 0.3281,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0183,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 37
        ("hs", "ho", "ho", "ho") : {
            "constant":  -5.167664200,
            "individual_dummy": {
                "age_18-29":  0.632156675 - 0.8511,
                "age_30-49":  1.106558979 + 0.7283,
                "age_50-64":  0.636516485 - 0.0824,
                "age_65-99":  1.250192981 +  0.394182783 - 0.0263,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
# utility function 38
        ("ho", "ho", "ho", "ho") : {
            "constant":  -4.892323651,
            "individual_dummy": {
                "age_18-29":  0.000000000 - 2.0113,
                "age_30-49":  0.000000000 + 0.2214,
                "age_50-64":  0.000000000 + 0.6946,
                "age_65-99":  0.394182783 - 0.0943,
                "car_users":  1.544612164
            },
            "zone": {
                "share_detached_houses": -0.8050000
            },
        },
    },
}
#list for variables, comments, gaps and dictionaries
tour_generation_file = ["""
### TOUR GENERATION PARAMETERS ####

# Scale parameter used in upper level of tour pattern model
tour_number_scale = 0.777654288490
# Calibration of tour numbers
tour_number_increase = {
    1: 0.943572,
    2: 1.086695,
    3: 0.937479,
    4: 1.024874,
}
# Tour combinations (calibrated)
""",
tour_combinations,
"""

tour_conditions = {
    ("hw",): (False, "age_7-17"),
    ("hc",): (True, "age_7-17"),
    ("hu",): (False, "age_7-17"),
    ("hw", "hw"): (False, "age_7-17"),
    ("hw", "hu"): (False, "age_7-17"),
    ("hw", "hs"): (False, "age_7-17"),
    ("hw", "ho"): (False, "age_7-17"),
    ("hc", "hc"): (True, "age_7-17"),
    ("hc", "hs"): (True, "age_7-17"),
    ("hc", "ho"): (True, "age_7-17"),
    ("hu", "hs"): (False, "age_7-17"),
    ("hu", "ho"): (False, "age_7-17"),
    ("hw", "hw", "ho"): (False, "age_7-17"),
    ("hw", "hs", "hs"): (False, "age_7-17"),
    ("hw", "hs", "ho"): (False, "age_7-17"),
    ("hw", "ho", "ho"): (False, "age_7-17"),
    ("hc", "hs", "ho"): (True, "age_7-17"),
    ("hc", "ho", "ho"): (True, "age_7-17"),
    ("hu", "hs", "ho"): (False, "age_7-17"),
    ("hu", "ho", "ho"): (False, "age_7-17"),
    ("hs", "hs", "hs"): (False, "age_7-17"),
    ("hs", "hs", "ho"): (False, "age_7-17"),
    ("hs", "ho", "ho"): (False, "age_7-17"),
    ("ho", "ho", "ho"): (False, "age_7-17"),
    ("hw", "hs", "hs", "ho"): (False, "age_7-17"),
    ("hw", "hs", "ho", "ho"): (False, "age_7-17"),
    ("hw", "ho", "ho", "ho"): (False, "age_7-17"),
    ("hs", "hs", "hs", "hs"): (False, "age_7-17"),
    ("hs", "hs", "hs", "ho"): (False, "age_7-17"),
    ("hs", "hs", "ho", "ho"): (False, "age_7-17"),
    ("hs", "ho", "ho", "ho"): (False, "age_7-17"),
    ("ho", "ho", "ho", "ho"): (False, "age_7-17"),
}
tour_generation = {
    "hw": {
        "population": 0.35564338,
    },
    "hc": {
        "population": 0.118853947,
    },
    "hu": {
        "population": 0.041594415,
    },
    "hs": {
        "population": 0.317210941,
    },
    "ho": {
        "population": 0.328234885,
    },
    "hoo": {
        "hw": {
            "car": 0.0656438658729866 / 0.35564338,
            "transit": 0.0526697439438969 / 0.35564338,
            "bike": 0.0115521977118796 / 0.35564338,
            "walk": 0.00649134752100624 / 0.35564338,
        },
        "hc": {
            "car": 0.00533194612539515 / 0.118853947,
            "transit": 0.00692385509143714 / 0.118853947,
            "bike": 0.00449463368636237 / 0.118853947,
            "walk": 0.00647482196705093 / 0.118853947,
        },
        "hu": {
            "car": 0.00270883182968936 / 0.041594415,
            "transit": 0.00989642413691942 / 0.041594415,
            "bike": 0.00202155468017382 / 0.041594415,
            "walk": 0.00213086543691209 / 0.041594415,
        },
        "hs": {
            "car": 0.035780598420169 / 0.317210941,
            "transit": 0.0132837264091338 / 0.317210941,
            "bike": 0.00490255394763913 / 0.317210941,
            "walk": 0.000885938755424613 / 0.317210941,
        },
        "ho": {
            "car": 0.0374586942790187 / 0.328234885,
            "transit": 0.017288313211596 / 0.328234885,
            "bike": 0.0049275398204637 / 0.328234885,
            "walk": 0.01321142864041 / 0.328234885,
        },
        "wo": {
            "car": 0.00232680277389218 / 0.036554019,
            "transit": 0.000848912513125093 / 0.036554019,
            "bike": 0 / 0.036554019, #missing from csv table?
            "walk": 0.00181085280674819 / 0.036554019,
        },
        "oo": {
            "car": 0.00216183177608496 / 0.04712731,
            "transit": 0.00148946565602993 / 0.04712731,
            "bike": 0 / 0.04712731, #missing from csv table?
            "walk": 0.00310305761313127 / 0.04712731,
        },
    },
    "wo": {
        "hw": 0.036554019 / 0.35564338, 
    },
    "oo": {
        "hc": 0.0066076386 / 0.118853947, 
        "hu": 0.0043557323 / 0.041594415, 
        "hs": 0.0002489022 / 0.317210941, 
        "ho": 0.0359150371 / 0.328234885, 
    },
    "wh": {
        "workplaces": 1,
    },
    "hwp": {
        "population": (1-0.0619) * 0.229078193053959,
    },
    "hop": {
        "population": (1-0.0619) * 0.524683573054545,
    },
    "sop": {
        "population": (1-0.0619) * 0.0503171031715505,
    },
    "oop": {
        # Every sop trip continues with oop trip
        "sop": 1,
    },
    "truck": {
        "population": 0.01,
        "workplaces": 0.025,
        "logistics": 0.35,
        "industry": 0.035,
        "shops": 0.05,
    },
    "trailer_truck": {
        "population": None,
        "workplaces": 0.005,
        "logistics": 0.38,
        "industry": 0.038,
        "shops": 0.005,
    }
}
garbage_generation = {
    "population": 0.000125,
    "workplaces": 0.000025,
}
vector_calibration_threshold = 5
"""
]

if __name__ == "__main__":

    sheet_name = "H146_manual"

    # File paths
    model_system_petr_path = "C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/ohjaus/"
    param_file_path = f"{model_system_petr_path}{sheet_name}.py"
    excel_file_path_petr = "C:/Users/HajduPe/OneDrive - Helsingin Seudun liikenne - Kuntayhtymä/Estimointi/EstimointikoneHelmet5.xlsx"
    excel_file_path = excel_file_path_petr #'EstimointikoneHelmet5_esimerkki.xlsx'

    # Load the Excel file
    df = pd.read_excel(excel_file_path,
                       sheet_name=sheet_name,
                       header=None
                       )
    df.reset_index()
    
        # Create dictionary object from dataframe
    key_value_dict = {}
    
    for i1, row in df.iterrows():
        this_row = row.to_list()
        this_row = [x for x in this_row if str(x) != 'nan']

        i = 0
        dict_depth = key_value_dict
        while this_row[i] in dict_depth:
            dict_depth = dict_depth[this_row[i]]
            i += 1
        i += 1
        print(this_row)
        while True:
            try:
                setInDict(key_value_dict, this_row[:-1], this_row[-1])
            except KeyError:
                setInDict(key_value_dict, this_row[:i], {})
                i += 1
                continue
            break

    tour_params_alogit = key_value_dict
    tour_combinations = tour_generation_file[1] #Change this later?
    tour_combinations[0][()]["individual_dummy"]["age_50-64"] = tour_params_alogit["I01_5064"]
    tour_combinations[0][()]["individual_dummy"]["age_65-99"] = tour_params_alogit["I01_65"]

    translate_tour = {"hw":"T","hc":"K","hu":"O","hs":"A","ho":"M"}
    comb_order = 2
    for num_tours in tour_combinations:
        if num_tours == 0: continue
        for tour_list in tour_combinations[num_tours]:
            #consts
            purposes = [translate_tour[x] for x in tour_list]
            const_code = "C" + str(comb_order) + "".join(purposes) + "".join(["X" for _ in range(4-num_tours)])
            tc = tour_combinations[num_tours][tour_list]
            tc["constant"] = 0
            if const_code in tour_params_alogit:
                tc["constant"] = tour_params_alogit[const_code]
                print(const_code)
            #individual dummies
            for age_cat in [(7,17),(18,29),(30,49),(50,64),(65,99)]:
                dummy_age = f"age_{age_cat[0]}-{age_cat[1]}"
                if dummy_age in tc["individual_dummy"]:
                    tc["individual_dummy"][dummy_age] = 0
                for purpose in set(purposes):
                    if age_cat[1] == 99:
                        param_age = f"{purpose}_{age_cat[0]}v" #mistä tuo tour koodi tulee?
                    else:
                        param_age = f"{purpose}_{age_cat[0]}_{age_cat[1]}"
                    if dummy_age in tc["individual_dummy"] and \
                        param_age in tour_params_alogit:
                        if(type(tour_params_alogit[param_age]) == str): print("WARN: Check that your numbers are not string inside Excel")
                        tc["individual_dummy"][dummy_age] += tour_params_alogit[param_age]
                        print(param_age, tour_params_alogit[param_age])
            if "car_users" in tc["individual_dummy"]:
                cars_param = f"H{num_tours}HAP"
                tc["individual_dummy"]["car_users"] = tour_params_alogit[cars_param]
                print(cars_param)
            #zones
            if "share_detached_houses" in tc["zone"]:
                zone_param = f"H{num_tours}erpi"
                tc["zone"]["share_detached_houses"] = tour_params_alogit[zone_param]
                print(zone_param)
            if "hu_t" in tc["zone"]:
                acc_study_param = f"O{num_tours}hu_t"
                tc["zone"]["hu_t"] = tour_params_alogit[acc_study_param]
                print(acc_study_param)
            if "ho_w" in tc["zone"]:
                acc_other_param = f"M{num_tours}ho_w"
                tc["zone"]["ho_w"] = tour_params_alogit[acc_other_param]
                print(acc_other_param)


            comb_order += 1

    # #tour_combinations[0][("hw",)]["constant"] = tour_params_alogit["C2TXXX"]
    # tour_combinations[1][("hw",)]["individual_dummy"]["age_18-29"] = tour_params_alogit["T_18_29"]
    # tour_combinations[1][("hw",)]["individual_dummy"]["age_30-49"] = tour_params_alogit["T_30_49"]
    # tour_combinations[1][("hw",)]["individual_dummy"]["age_50-64"] = tour_params_alogit["T_50_64"]
    # tour_combinations[1][("hw",)]["individual_dummy"]["age_65-99"] = tour_params_alogit["T_65v"]
    # tour_combinations[1][("hw",)]["zone"]["share_detached_houses"] = tour_params_alogit["H1erpi"]
    # tour_combinations[1][("hc",)]["constant"] = tour_params_alogit["C3KXXX"]
    # #tour_combinations[1][("hc",)]["individual_dummy"]["age_7-17"] = tour_params_alogit["K_7_17"]
    # tour_combinations[1][("hc",)]["zone"]["share_detached_houses"] = tour_params_alogit["H1erpi"]


    # Create a new Python script to recreate the dictionary
    with open('C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/skriptit/generated/tour_combinations_dict.py', 'w') as f:
        for text in tour_generation_file:
            if type(text) == dict:
                f.write(print_dict(tour_combinations, "tour_combinations"))
            else:
                f.write(text)
            
