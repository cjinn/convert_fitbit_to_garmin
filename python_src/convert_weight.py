import os
import csv
import json

def convert_fitbit_weight_json_to_garmin_csv(
        input_filepath,
        output_filepath):
    """ Convert Fitbit JSON into csv file for garmin

    Only support weights at this time

    input_filepath - 
    output_filepath - 
    """
    ### Check parameters


    ## Constants
    FITIBIT_DATE_STR = "date"
    FITIBT_WEIGHT_STR = "weight"
    FITBIT_BMI_STR = "bmi"
    FITBIT_FAT_STR = "fat"

    with open(output_filepath, mode ='w') as out_file:
        output_csvFile = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_NONE)

        # Necessaary lines
        output_csvFile.writerow([
            "Body",
        ])
        output_csvFile.writerow([
            "Date",
            "Weight",
            "BMI",
            "Fat"
        ])

        with open(input_filepath, mode ='r') as input_file:
            input_jsonfile = json.load(input_file)

            for dict_entry in input_jsonfile:
                garmin_date_str = ""
                garmin_weight_float = 0.0
                garmin_bmi_float = 0.0
                garmin_fat_float = 0.0

                if FITIBIT_DATE_STR not in dict_entry or \
                    FITIBT_WEIGHT_STR not in dict_entry:
                    continue
                
                ### Format date
                # Fitbit convention is mm/dd/yy
                # Garmin convention will be yyyy-mm-dd
                fitbit_date_list = dict_entry[FITIBIT_DATE_STR].split('/')

                if len(fitbit_date_list) != 3:
                    continue
                else:
                    garmin_date_str = "20{}-{}-{}".format(
                        fitbit_date_list[2].strip(),
                        fitbit_date_list[0].strip(),
                        fitbit_date_list[1].strip()
                    )

                ### Import weight
                # Note that both conventions is in pounds
                garmin_weight_float = dict_entry[FITIBT_WEIGHT_STR]

                ### If present, import bmi
                if FITBIT_BMI_STR in dict_entry:
                    garmin_bmi_float = dict_entry[FITBIT_BMI_STR]

                ### If present, import fat
                if FITBIT_FAT_STR in dict_entry:
                    garmin_fat_float = dict_entry[FITBIT_FAT_STR]

                garmin_csv_row = [
                    "{}".format(garmin_date_str),
                    "{}".format(garmin_weight_float),
                    "{}".format(garmin_bmi_float),
                    "{}".format(garmin_fat_float),
                ]

                ### Log entry
                output_csvFile.writerow(garmin_csv_row)

                # TODO: Remove new line creation after writerow()

def convert_fitbit_weight_json_to_garmin_csv_directory(
        input_directory,
        output_directory):
    """
    """
    assert(os.path.exists(input_directory) and os.path.isdir(input_directory))
    assert(os.path.exists(output_directory) and os.path.isdir(output_directory))

    for input_filename in os.listdir(input_directory):
        # TODO: Implement Recursively apply to subdirectory well
        if (os.path.isdir(input_filename)):
            convert_fitbit_weight_json_to_garmin_csv_directory(
                input_directory=input_filename,
                output_directory=output_directory)
            continue
        
        input_basename, input_file_extension  = input_filename.split('.')

        if input_file_extension.lower() != "json":
            continue
        output_basename = "{}.csv".format(input_basename)

        input_filepath = os.path.join(input_directory, input_filename)
        output_filepath = os.path.join(output_directory, output_basename)

        convert_fitbit_weight_json_to_garmin_csv(
            input_filepath=input_filepath,
            output_filepath=output_filepath,
        )

if __name__ == "__main__":
    INPUT_DIRECTORY = "examples/weight"
    OUTPUT_DIRECTORY = "_output/weight"

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    convert_fitbit_weight_json_to_garmin_csv_directory(
        input_directory=INPUT_DIRECTORY,
        output_directory=OUTPUT_DIRECTORY,
    )