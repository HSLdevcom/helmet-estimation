import pandas as pd
import numpy as np

def get_cycle(func, zones_number, modes, mode):
    e = modes[mode]
    start_num = zones_number*e +1
    end_num = zones_number*(e+1)
    j_var = "I" if mode == "W" else "I - %s*%s" % (e, zones_number)
    cycle_text = """
DO I = %s,%s
    J = %s
    %s
END
    """ % (start_num, end_num, j_var, func)

    return cycle_text


def model2alogit(alo_file, title="", subtitle="", alo_print="", estimate="", algor="", is_simple_logit=0, zones_number=2098, keep_vars=[], coeffs=[],lsm="", files_and_vars={}, extras={}, util={}, size=[]):
    modes_tot = {"W":0,"B":1,"T":2,"C":3, "L":4}
    if is_simple_logit==0 or is_simple_logit == 34: #nested logit
        modes = modes_tot if is_simple_logit==0 else {m:modes_tot[m] for m in modes_tot if m in ["C","T"]}
        nest_str = "$nest root () " + " ".join(modes)+"\n"

        for mode in modes:
            e = modes[mode]
            if mode == "": continue
            nest_str += "$nest %s (Dcoeff)" % mode
            mode_start = zones_number*e+1
            mode_end = zones_number*(e+1)+1
            nest_str += "\n+ "+"\n+ ".join([" ".join([str(i+y*10+mode_start) for i in range(0,10) if i+y*10+mode_start < mode_end]) for y in range(0,int((mode_end-mode_start)/10)+1)])+"\n"
    else:
        modes = {k:modes_tot[k] for k in modes_tot if modes_tot[k] == is_simple_logit-1}
        nest_str = "$nest root ()\n"

        e=list(modes.values())[0] #vain viimeinen luokka käytössä
        mode_start = zones_number*e+1
        mode_end = zones_number*(e+1)+1
        nest_str += "\n+ "+"\n+ ".join([" ".join([str(i+y*10+mode_start) for i in range(0,10) if i+y*10+mode_start < mode_end]) for y in range(0,int((mode_end-mode_start)/10)+1)])+"\n"

    keep_str = "\n$keep IZ = "+str(zones_number)
    keep_str += "\n$ARRAY "+",\n+ ".join([f"{var}(IZ)" for var in keep_vars])

    if len(coeffs)>0:
        coeff_str = "\n$coeff "+coeffs[0]
        if len(coeffs)>1:
            for c in coeffs[1:]:
                coeff_str += "\n+ "+c
    else: 
        coeff_str = ""

    if lsm != "":
        lsm_str = "\n$L_S_M "+lsm+"\n"
    else:
        lsm_str = ""
    
    files_str = ""
    for fv in files_and_vars:
        if "key" not in files_and_vars[fv]: 
            key = ""
        else:
            key = ",key="+files_and_vars[fv]["key"]

        if "output" in files_and_vars[fv]:
            output = " ,output "
        else:
            output = ""
        files_str += "\nFILE (name= "+fv+output+key+")\n"
        var_counter = 1
        used_vars = []
        for var in files_and_vars[fv]["vars"]:
            if var in used_vars: continue
            else: used_vars.append(var)
            
            files_str += var
            if var_counter % 10 == 0:
                files_str += "\n"
            else:
                files_str += " "
            var_counter += 1

    extras_str = "\n\n"

    #Ndest
    extras_str += f"Ndest={zones_number}\n"

    #Choice
    if is_simple_logit in [1,2,3,4] and "ORIG" not in alo_file: #sec_dest model
        extras_str += f"choice= kzone+((ifeq(mode,1,2,3,4)+ifeq(mode,5)*4)-1)*Ndest\n"
    elif "L" in modes_tot:
        extras_str += f"choice= jzone+((ifeq(mode,1,2,3,4)+ifeq(mode,5)*4+ifeq(mode,6)*5)-1)*Ndest\n"
    else:
        extras_str += f"choice= jzone+((ifeq(mode,1,2,3,4)+ifeq(mode,5)*4)-1)*Ndest\n"
    

    #Weight
    extras_str += f"WEIGHT=xfactor/closed*1379/159761.06\n"

    #Stats
    stat_vars = ["choice", "WEIGHT","xfactor","ttype","mode","jzone"]
    extras_str += "$GEN.STATS\n"+"\n".join(stat_vars)+"\n\n"

    if is_simple_logit==0 and "_SEC_" not in alo_file:
        #Filters
        extras_str += get_cycle("Avail(I) =  ifle(walkDist(J) ,15) and ifle(J,%s)" % zones_number, zones_number, modes, "W")
        extras_str += get_cycle("Avail(I) =  ifle(bikeDist(J) ,60) and ifle(J,%s)" % zones_number, zones_number, modes, "B")
    
    for calc in extras["calcs"]:
        extras_str += "\n"+calc+"\n"

    excludes_str = ""


    for i,excl in enumerate(extras["excludes"]):
        excludes_str += f"\nexclude({i+1}) = {excl}\n"

    utils_str = ""
    for mode in modes:
        print(util[mode])
        mode_id = modes[mode]
        for zone in range(zones_number):
            zn = mode_id*zones_number+zone+1
            pid = zone % zones_number+1
            utils_str += f"\nPid={pid}\nUtil({zn})="
            utils_str += "\n+ ".join(util[mode])+"\n"

    sizes_str = ""
    for mode in modes:
        mode_id = modes[mode]
        for zone in range(zones_number):
            zn = mode_id*zones_number+zone+1
            pid = zone % zones_number+1
            sizes_str += f"\nPid={pid}\nSize({zn})="
            sizes_str += "\n+ ".join(size)+"\n"

    with open(alo_file, "w") as f:
        f.write("$TITLE "+title+"\n")
        f.write("$subtitle "+subtitle+"\n")
        f.write("$print "+alo_print+"\n")
        f.write("$estimate "+estimate+"\n")
        f.write("$algor "+algor+"\n")
        f.write(nest_str)
        f.write(keep_str)
        f.write(coeff_str)
        f.write(lsm_str)
        f.write(files_str)
        f.write(extras_str)
        f.write(excludes_str)
        f.write(utils_str)
        f.write(sizes_str)


if __name__=="__main__":
      
    excel_path = "C:\\Users\\HajduPe\\OneDrive - Helsingin Seudun liikenne - Kuntayhtymä\\Estimointi\\EstimointikoneHelmet5.xlsx"
    files = pd.read_excel(excel_path, "Vastaavuudet", engine='openpyxl')
    for label,file in files.iterrows():
        if pd.isnull(file["Välilehti"]): continue
        if file["Välilehti"] != "HS15 Koti-työ":continue #for testing a single model
        print("Model: ", file["Välilehti"])
        sheet = pd.read_excel(excel_path, file["Välilehti"], engine='openpyxl')
        size = sheet["Size"].dropna().astype("string").to_list()
        utils = {alo_mode:sheet["Util_"+mode].dropna().astype("string").to_list() for alo_mode,mode in zip(["W","B","T","C","L"],["W","B","PT","Car","PR"])} #TODO: change this later?
        coeffs = sheet["Coeff"].dropna().to_list()
        arrays = sheet.loc[sheet["Source"].isin(["Jzonet","vastukset","SEC_vastukset","laskettuArr"]),"Property"].dropna().to_list()
        if "pid" in arrays: arrays.remove("pid")
        all_vars = sheet["Property"].dropna().to_list()
        sources_wanted = sheet["Source"].dropna().to_list()
        all_vars_except_array = [var for var in all_vars if var not in arrays]
        var_list = pd.read_excel(excel_path, "Muuttujalista", engine='openpyxl')
        sources = {(sfile,var_list[sfile][0]): var_list[sfile][1:].dropna().to_list() for sfile in var_list}
        
        alo_sources = {}
        vastukset_type = file["Vastukset"]
        for s in sources:
            #print(str(file["Vastukset"]), s)
            if s[1].startswith("vastukset") and str(file["Vastukset"])!="nan":
                if ("bike" in s[0] or "walk" in s[0]) and file["Välilehti"].startswith("YMP"): continue
                alo_sources[s[0].replace("_X_","_"+vastukset_type+"_")] = {"key":"izone","vars":sources[s]}
            elif s[1].startswith("Jzonet"):
                alo_sources[s[0]] = {"vars":sources[s]}
            elif s[1] == "laskettuArr":
                pass
            else:
                if s[1] not in sources_wanted: continue
                if len(s[1]) == 3: #!!! Vain 3 kirjainta per havaintolähde
                    alo_sources[s[0]] = {"vars": sources[s]}
                elif s[1] == "SEC_vastukset":
                    alo_sources[s[0]] = {"key": "pid",
                                        "vars": sources[s]}
                else:
                    alo_sources[s[0]] = {"key": "izone",
                                        "vars": sources[s]}
        alo_sources[file["Output"]] = {"output": True, "vars": all_vars_except_array}

        if type(file["LSM"]) == float or str(file["LSM"])=="":
            lsm = ""
        else:
            lsm = file["LSM"]

        if "Exclude" in sheet:
            excludes = sheet["Exclude"].dropna().to_list()
        else:
            excludes = []

        if "Calc" in sheet:
            calcs = sheet["Calc"].dropna().to_list()
        else:
            calcs = []

        extras = {"calcs":calcs,
                  "excludes": excludes}
        #print(extras)
        model2alogit(file["Tiedosto"],
                    file["Title"],
                    str(file["Subtitle"]),
                    file["Print"],
                    file["Estimate"],
                    file["Algorithm"],
                    file["Simple_logit"],
                    int(file["Zones_num"]),
                    arrays,
                    coeffs,
                    lsm,
                    alo_sources,
                    extras,
                    utils,
                    size

                    )
        
        #break