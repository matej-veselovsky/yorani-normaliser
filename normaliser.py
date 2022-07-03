import sys
import csv


def replaceDelimiters(csv_file):
    data = ""

    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        data = file.read().replace("\\,", ",").replace("\\", ",").replace("/", ",")

    with open(csv_file, mode="w") as file:
        file.truncate()
        file.write(data)


def dropDescription(csv_file):
    data = ""

    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            for element in row: #iterates through all elements of each row
                
                if element != "Difficult":  # Once we get to "Difficult" there are no more translations in that row, and we can discard the rest
                    data += element + ","
                else: 
                    data = data.rstrip(",") # Deletes the trailing comma
                    break # continue in next row
            data += "\n"
    
    with open(csv_file, mode="w") as file:
        file.truncate()
        file.write(data)


def createFeminine(csv_file):
    data = ""

    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            addition = ""

            for element in row:
                if element == row[1] and element[0] == "-":
                    stem = ""
                    masculineForm = row[0].strip()
                    feminineForm = ""
                    suffix = row[1][1:].strip()
                    match = suffix[0]

                    if masculineForm[0] == "-" or masculineForm[0] == "—":
                        continue
                    
                    if suffix == "cekaa":
                        screener = len(masculineForm) - len("sikayi") - 1
                    elif suffix == "wiā":
                        screener = len(masculineForm) - len("veyi") - 1
                    elif suffix == "liā":
                        screener = len(masculineForm) - len("neyi") - 1
                    elif suffix == "huā":
                        screener = len(masculineForm) - len("gayi") - 1
                    elif suffix == "tuneā":
                        screener = len(masculineForm) - len("neyi") - 1
                    else:
                        screener = len(masculineForm) - 1
                        while (masculineForm[screener] != match):
                            screener -= 1
                    
                    stem = masculineForm[0:screener]
                    feminineForm = stem + suffix
                    addition += "0" + feminineForm + ","
                else:
                    addition += element + ","
            data += addition.rstrip(",") + "\n"

    with open(csv_file, mode="w", encoding="utf-8-sig") as file:
        file.truncate()
        file.write(data)


def main(file):
    replaceDelimiters(file)
    dropDescription(file)
    createFeminine(file)


if (__name__ == "__main__"):
    file = str(sys.argv[1])
    main(file)