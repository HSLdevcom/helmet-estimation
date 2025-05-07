import pandas as pd
import sys

if len(sys.argv) > 1:
        
    model_name = sys.argv[1] # = 'HS15_logsum_for_orig'
    print("Model name: ", model_name)
    alogit_run_petr_path = "C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/ohjaus/"    
    text_file_path = f"{alogit_run_petr_path}{model_name}.F12"

    # Read and process the text file to create a DataFrame
    with open(text_file_path, 'r') as file:
        lines = file.readlines()

    data_lines = lines[3:]
    end_index = next(i for i, line in enumerate(data_lines) if line.strip().startswith('-1'))
    relevant_lines = data_lines[:end_index]
    data = [line.split() for line in relevant_lines]
    df = pd.DataFrame(data)

    # Extract the second and fourth columns
    second_column_values = df.iloc[:, 1].values
    fourth_column_values = df.iloc[:, 3].values

    # Create a dictionary for quick lookup
    value_dict = dict(zip(second_column_values, fourth_column_values))

    res_file = f"{alogit_run_petr_path}{model_name[:-9]}_tulokset.alo"

    with open(res_file, 'w') as filew:
        for k in value_dict:
            key = k+"_p" if k=="CT_cost" and model_name[:3] == "YMP" else k #special quirk for peripheral CT_cost
            if key!="Dcoeff":
                filew.write(key+" = "+str(value_dict[k])+"\n")
            else:
                pass