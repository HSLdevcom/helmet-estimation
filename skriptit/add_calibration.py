
import pandas as pd
import numpy as np
import sys
import json
from functools import reduce
import operator
from typing import Any, Dict, Optional
import numpy # type: ignore

def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value  # type: ignore

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

def parse_dict(rows):
    rdict = "".join(rows)
    mcdict = eval(rdict.split(" = ")[1]) #Never use this with public input, potential problem
    return mcdict

def adjust_dict(mcdict, data):
    for model in mcdict:
        if model in ["hoo","hwp","hop","sop","wh","oop"]: continue
        modeldict = mcdict[model]
        for mode in modeldict:
            print(model,mode)
            modedict = modeldict[mode]
            calibration_row = data.query(f"model_mode=='{model}_{mode}'")
            #dcoeff = modedict["log"]["logsum"]
            #print(calibration_row["surround"].shape)
            if calibration_row.empty: continue
            cbd,other,evk,surround = [calibration_row[source].item() for source in ["helsinki_cbd","helsinki_other","espoo_vant_kau","surround"]]
            print("cbd",cbd,"other",other,"evk",evk,"surround",surround)
            print(modedict["generation"].keys())
            modedict["constant"] = (modedict["constant"][0],surround + modedict["constant"][1])
            if "cbd" in modedict["generation"]:
                modedict["generation"]["cbd"] += cbd
            else:
                modedict["generation"]["cbd"] = cbd
            if "helsinki_other" in modedict["generation"]:
                modedict["generation"]["helsinki_other"] += other
            else:
                modedict["generation"]["helsinki_other"] = other
            if "espoo_vant_kau" in modedict["generation"]:
                modedict["generation"]["espoo_vant_kau"] += evk
            else:
                modedict["generation"]["espoo_vant_kau"] = evk
    return mcdict

df = pd.read_excel("C:/Users/HajduPe/OneDrive - Helsingin Seudun liikenne - Kuntayhtymä/Estimointi/Calibration/Calibration-vertailu.xlsx",
                        sheet_name="ModeSourceExport",
                        engine='openpyxl'
                        )
print(df.query("model_mode=='hc_bike'")["helsinki_cbd"])
with open('generated/modes_dict.py', 'r') as f:
               # Create a new Python script to recreate the dictionary
    with open('generated/modes_dict_calibrated.py', 'w') as fc:
        ftext = []
        mdict = []
        mode_choice_detected = False
        for row in f.readlines():

            if "mode_choice" in row:
                mode_choice_detected = True
            if mode_choice_detected:
                mdict.append(row)
            else:
                ftext.append(row)
        ftext.append(adjust_dict(parse_dict(mdict),df))
        for text in ftext:

            if type(text) == dict:
                fc.write(print_dict(text, "mode_choice"))
            else:
                fc.write(text)
