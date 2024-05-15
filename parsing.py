import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # Assuming a column named 'No' to
            # be the primary key
            key1 = rows["STATE"]
            key2 = rows["ENERGY SOURCE"]
            if key1 not in data:
                data[key1] = {}
            if (
                rows["TYPE OF PRODUCER"] == "Total Electric Power Industry"
                and rows["YEAR"] == "2021"
            ):
                data[key1][key2] = int(rows["GENERATION (Megawatthours)"])
            # if key2 not in data[key1]:
            #     data[key1][key2] = []
            # data[key1][key2] = rows
    # Open a json writer, and use the json.dumps()
    # function to dump data
    for state in data.keys():
        total = 0
        for type in data[state].keys():
            if type != "Total":
                if data[state][type] < 0:
                    data[state][type] = 0
                else:
                    total += data[state][type]
        data[state]["Total"] = total

    with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Driver Code

# Decide the two file paths according to your
# computer system
csvFilePath = r"data.csv"
jsonFilePath = r"data.json"

# Call the make_json function
make_json(csvFilePath, jsonFilePath)