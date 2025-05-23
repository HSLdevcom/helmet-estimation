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

demand_start = """

### DEPARTURE TIME PARAMETERS ###

# Demand shares for different time periods
from typing import Any, Dict
"""

demand_share: Dict[str,Dict[str,Any]] = {
    "hw": {
        "car": {
            "aht": (0.288820549293814, 0.00164983305999384),
            "pt": (0.0191570544576966, 0.0187771980766991),
            "iht": (0.00837994382924266, 0.200731740107779),
        },
        "transit": {
            "aht": (0.262479154675437, 0.00454557641637759),
            "pt": (0.0225536757473919, 0.0128179742542008),
            "iht": (0.00652782252709554, 0.195785332057699),
        },
        "bike": {
            "aht": (0.333051067436711, 0.00608107081976724),
            "pt": (0.0243488683605967, 0.0108569277701356),
            "iht": (0.00253869404962361, 0.305891580275386),
        },
        "walk": {
            "aht": (0.273980325226173, 0),
            "pt": (0.0435560236876547, 0.0189789041646973),
            "iht": (0.0103649240096114, 0.216436049124337),
        },
        "park_and_ride": { #TODO: count the real ones
            "aht": (0.288820549293814, 0.00164983305999384),
            "pt": (0.0191570544576966, 0.0187771980766991),
            "iht": (0.00837994382924266, 0.200731740107779),
        },
    },
    "hc": {
        "car": {
            "aht": (0.490351584394913, 0),
            "pt": (0.0254451935768562, 0.0703760687389817),
            "iht": (0, 0.0921431200622989),
        },
        "transit": {
            "aht": (0.540424167743717, 0),
            "pt": (0.0217636820804232, 0.091223241969132),
            "iht": (0, 0.15431375989959),
        },
        "bike": {
            "aht": (0.573544771072346, 0),
            "pt": (0.0341593458419707, 0.109149614323394),
            "iht": (0.00581859500994643, 0.106528611377131),
        },
        "walk": {
            "aht": (0.634870345538194, 0),
            "pt": (0.0306004089091672, 0.101786210936117),
            "iht": (0.00129395017965348, 0.0873941474226051),
        },
    },
    "hu": {
        "car": {
            "aht": (0.382660524070486, 0.0127971082664054),
            "pt": (0.0401662768013263, 0.0419553527613303),
            "iht": (0.0634572553797318, 0.174561156092557),
        },
        "transit": {
            "aht": (0.284476235025134, 0.00561152590349421),
            "pt": (0.0601280307807604, 0.0510887696999263),
            "iht": (0.0446532572748154, 0.126845096164362),
        },
        "bike": {
            "aht": (0.229360821622338, 0),
            "pt": (0.0853918424071615, 0.0977621699203758),
            "iht": (0, 0.139908006489409),
        },
        "walk": {
            "aht": (0.231109452978529, 0.0309167551561489),
            "pt": (0.070746711397507, 0.0467990916911236),
            "iht": (0.0684187871098807, 0.149939088659526),
        },
    },
    "hs": {
        "car": {
            "aht": (0.0405885794319654, 0.017477652057659),
            "pt": (0.0603970615836207, 0.0516421108026735),
            "iht": (0.0467016998318382, 0.0638692528598624),
        },
        "transit": {
            "aht": (0.0765341541405897, 0.00474012379675776),
            "pt": (0.0836406354990259, 0.0689212206158884),
            "iht": (0.0502459240576862, 0.0745312871363393),
        },
        "bike": {
            "aht": (0.0543007460241876, 0.00810299970756844),
            "pt": (0.0692597647600368, 0.0653942703626311),
            "iht": (0.103151738228992, 0.0943488182960698),
        },
        "walk": {
            "aht": (0.0541193511885965, 0.0352911509085712),
            "pt": (0.0722356526856759, 0.0662356604096378),
            "iht": (0.0779480165375336, 0.097691106660283),
        },
    },
    "ho": {
        "car": {
            "aht": (0.0383781860538185, 0.00726442614171374),
            "pt": (0.0360424142229208, 0.0275607040867388),
            "iht": (0.0806312062597426, 0.0540736359601802),
        },
        "transit": {
            "aht": (0.0269642764493981, 0.0119453710428538),
            "pt": (0.0503769382556892, 0.0333208756748491),
            "iht": (0.0561622637903115, 0.052159156048967),
        },
        "bike": {
            "aht": (0.0493482076538219, 0.00527814017610801),
            "pt": (0.0380796623932762, 0.0237108591394003),
            "iht": (0.103754797149548, 0.0365662237825043),
        },
        "walk": {
            "aht": (0.0503132293052518, 0.0126997362017003),
            "pt": (0.0423249887393872, 0.0148612529729895),
            "iht": (0.0743905515132885, 0.0235606061219946),
        },
    },
    "hoo": {
        "car": {
            "aht": (
                (0.0113538534294527, 0.0483356330299955),
                (0.000783876140666748, 0.0782437896466509),
            ),
            "pt": (
                (0.0415688948149155, 0.0275008865700513),
                (0.0249338403352452, 0.0218610155562793),
            ),
            "iht": (
                (0.126631086164843, 0.0254942149131846),
                (0.103874241247952, 0.0253360698120264),
            ),
        },
        "transit": {
            "aht": (
                (0.007848433131924, 0.0318369625680414),
                (0.00148575955291745, 0.0800841531842564),
            ),
            "pt": (
                (0.0392336062771297, 0.0251341675086098),
                (0.0191847672424449, 0.0215475457292278),
            ),
            "iht": (
                (0.191259463404029, 0.0367695909665859),
                (0.0872373132287834, 0.0165925719765324),
            ),
        },
        "bike": {
            "aht": (
                (0, 0.10752104373009),
                (0.00325263861271775, 0.0927918963956284),
            ),
            "pt": (
                (0.0409730943539997, 0.017507905833713),
                (0.0223568984557525, 0.0207634708992704),
            ),
            "iht": (
                (0.207855295206265, 0.0225336043406983),
                (0.145116003557633, 0.0142643853021503),
            ),
        },
        "walk": {
            "aht": (
                (0.00528306888246316, 0.0242399831328879),
                (0.00245894352109173, 0.0537383727550346),
            ),
            "pt": (
                (0.0563252625358924, 0.0206655527844586),
                (0.0292490758079734, 0.0210437085372139),
            ),
            "iht": (
                (0.0814142081203715, 0.0271941913428873),
                (0.172295888708894, 0.0396594463206377),
            ),
        },
    },
    "wo": {
        "car": {
            "aht": (0.0276329210085113, 0.0160545369209701),
            "pt": (0.117661361659664, 0.112453940581752),
            "iht": (0.0444924430264217, 0.0342827141128922),
        },
        "transit": {
            "aht": (0.0612632351804617, 0.262154110522183),
            "pt": (0.0433316351591352, 0.0504505017148806),
            "iht": (0.106235593058989, 0.0737024653715484),
        },
        "bike": {
            "aht": (0.086082711150622, 0),
            "pt": (0.123481019815671, 0.108973372738578),
            "iht": (0.0389737064352321, 0),
        },
        "walk": {
            "aht": (0.011792243269137, 0.00568311888204953),
            "pt": (0.142991903140661, 0.136629905882937),
            "iht": (0.0353877586419574, 0.00914593563528563),
        },
    },
    "oo": {
        "car": {
            "aht": (0.0196842157479813, 0.0479857415578179),
            "pt": (0.0586827967478624, 0.0422759234382751),
            "iht": (0.0681586448888759, 0.0736313747819507),
        },
        "transit": {
            "aht": (0.168710422485735, 0.0387468664988151),
            "pt": (0.0716348116654068, 0.0679842570835241),
            "iht": (0.0437554897467228, 0.108924099422715),
        },
        "bike": {
            "aht": (0.0259945209673068, 0.0164613914375604),
            "pt": (0.0692448058659033, 0.0449421010361262),
            "iht": (0.0131611231013582, 0.0411710936086695),
        },
        "walk": {
            "aht": (0.0453535537909917, 0.00282685203656034),
            "pt": (0.0873311164803913, 0.0374143719459607),
            "iht": (0.0547447028678427, 0.0134107502846961),
        },
    },
    "hwp": {
        "car": {
            "aht": (0.284828673072634, 0.00755712929837991),
            "pt": (0.023112752669798, 0.0328984808575901),
            "iht": (0.00803413387844214, 0.332443891285462),
        },
        "transit": {
            "aht": (0.149234181643916, 0),
            "pt": (0.0163476939401269, 0.0355138136169777),
            "iht": (0, 0.412582980634712),
        },
    },
    "hop": {
        "car": {
            "aht": (0.0910767007840877, 0.0133245756008547),
            "pt": (0.0733228496135912, 0.0632392268306549),
            "iht": (0.0725521634967265, 0.0897368257624752),
        },
        "transit": {
            "aht": (0.330576470748095, 0),
            "pt": (0.0391056752731289, 0.0919882820859918),
            "iht": (0.0311972821960398, 0.0991336256168802),
        },
    },
    "oop": {
        "car": {
            "aht": (0.0585795789311712, 0.041118431421166),
            "pt": (0.114889840412835, 0.116203520254407),
            "iht": (0.0397633661562958, 0.0277396603049591),
        },
        "transit": {
            "aht": (0.376361385885435, 0),
            "pt": (0.0869523179383367, 0.0347224022302181),
            "iht": (0.0112765910942976, 0.0136093560308682),
        },
    },
    "freight": {
        "trailer_truck": {
            "aht": (0.066, 0),
            "pt": (0.07, 0),
            "iht": (0.066, 0),
        },
        "truck": {
            "aht": (0.066, 0),
            "pt": (0.07, 0),
            "iht": (0.066, 0),
        },
        "van": {
            # As shares of car traffic
            # On top of this, the trucks sum is added
            "aht": (0.054, 0),
            "pt": (0.07, 0),
            "iht": (0.044, 0),
        },
    },
    "external": {
        # External matrices are untransposed (ext->int),
        # and describe trips, not tours
        "car": {
            "aht": (
                [
                    [0.042], [0.042], [0.049], [0.042], [0.055], [0.042],
                    [0.042], [0.058], [0.042], [0.042], [0.042], [0.042],
                    [0.042], [0.061], [0.030], [0.042], [0.042], [0.041],
                    [0.038], [0.040], [0.000], [0.000], [0.000], [0.043],
                    [0.000], [0.000], [0.000], [0.250],
                ], 
                [
                    0.028, 0.028, 0.024, 0.028, 0.018, 0.028,
                    0.028, 0.045, 0.028, 0.028, 0.028, 0.028,
                    0.028, 0.031, 0.039, 0.028, 0.028, 0.034,
                    0.028, 0.046, 0.000, 0.000, 0.000, 0.042,
                    0.000, 0.000, 0.083, 0.000,
                ],
            ),
            "pt": (0.05, 0.05),
            "iht": (
                [
                    [0.045], [0.045], [0.044], [0.045], [0.048], [0.045],
                    [0.045], [0.056], [0.045], [0.045], [0.045], [0.045],
                    [0.045], [0.051], [0.070], [0.045], [0.045], [0.039],
                    [0.056], [0.069], [0.000], [0.000], [0.000], [0.071],
                    [0.000], [0.000], [0.125], [0.000],
                ],
                [
                    0.055, 0.055, 0.069, 0.055, 0.066, 0.055,
                    0.055, 0.052, 0.055, 0.055, 0.055, 0.055,
                    0.055, 0.065, 0.049, 0.055, 0.055, 0.064,
                    0.076, 0.057, 0.000, 0.000, 0.000, 0.066,
                    0.188, 0.273, 0.083, 0.250,
                ],
            ),
        },
        "transit": {
            "aht": (0.101, 0.034),
            "pt": (0.05, 0.05),
            "iht": (0.064, 0.119),
        },
        "trailer_truck": {
            "aht": (0.033, 0.033),
            "pt": (0.035, 0.035),
            "iht": (0.033, 0.033),
        },
        "truck": {
            "aht": (0.033, 0.033),
            "pt": (0.035, 0.035),
            "iht": (0.033, 0.033),
        },
    },
}


demand_end = """
backup_demand_share = {
    "aht": (0.042, 0.028),
    "pt": (0.05, 0.05),
    "iht": (0.045, 0.055),
}

### DEMAND TRANSFORMATION REFERENCES ###

divided_classes = (
    "car",
    "transit",
    "bike",
)
"""

df = pd.read_csv("C:/Users/HajduPe/helmet-data-preprocessing/shares/shares.csv", sep=";",decimal=",")

print(df.head())
models = {"hw":"hw","hc":"hc","hu":"hu","hs":"hs","ho":"ho","wo":"wo","oo":"oo","hoo_leg2":"hoo"}

print(demand_share["hw"]["car"]["aht"])
for model,h5model in models.items():
    for h5mode,mode in zip(["car","transit","bike","walk","park_and_ride"],["car","transit","bike","walk","pnr"]):
        if "park_and_ride" not in demand_share[h5model] and mode=="pnr": continue
        for period in ["aht","pt","iht"]:
            if h5model=="hoo":
                forward1 = df.query(f"model_type=='hoo_leg2' & mode_name=='{mode}' & scenario=='{period}'")["share_forward"].item()
                backward1 = df.query(f"model_type=='hoo_leg2' & mode_name=='{mode}' & scenario=='{period}'")["share_backward"].item()
                forward2 = df.query(f"model_type=='hoo_leg3' & mode_name=='{mode}' & scenario=='{period}'")["share_forward"].item()
                backward2 = df.query(f"model_type=='hoo_leg3' & mode_name=='{mode}' & scenario=='{period}'")["share_backward"].item()
                demand_share[h5model][h5mode][period] = ((float(forward1),float(backward1)),
                                                     (float(forward2),float(backward2)))
            else:
                
                forward = df.query(f"model_type=='{model}' & mode_name=='{mode}' & scenario=='{period}'")["share_forward"].item()
                backward = df.query(f"model_type=='{model}' & mode_name=='{mode}' & scenario=='{period}'")["share_backward"].item()
                demand_share[h5model][h5mode][period] = (float(forward),float(backward))

demand_file = [demand_start,
                demand_share,
                demand_end]


# Create a new Python script to recreate the dictionary
with open('C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/skriptit/generated/demand_dict.py', 'w') as f:
    for text in demand_file:
        if type(text) == dict:
            f.write(print_dict(demand_share, "demand_share"))
        else:
            f.write(text)