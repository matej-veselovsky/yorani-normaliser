import sys
import csv
import sqlite3


def replaceDelimiters(csvFile):
    data = ""

    with open(csvFile, mode="r", encoding="utf-8-sig") as file:
        data = file.read().replace("\\,", ",").replace("\\", ",").replace("/", ",")

    with open(csvFile, mode="w") as file:
        file.truncate()
        file.write(data)

    print("Delimiters replaced.")


def dropDescription(csvFile):
    data = ""

    with open(csvFile, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            for element in row: #iterates through all elements of each row
                
                if element != "Difficult":  # Once we get to "Difficult" there are no more translations in that row, and we can discard the rest
                    data += element + ","
                else: 
                    data = data.rstrip(",") # Deletes the trailing comma
                    break # continue in next row
            data += "\n"
    
    with open(csvFile, mode="w") as file:
        file.truncate()
        file.write(data)

    print("Description dropped.")


def createFeminine(csvFile):
    data = ""

    with open(csvFile, mode="r", encoding="utf-8-sig") as file:
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
                    addition += "0" + feminineForm + "," # 0 is a marker needed for the next step
                else:
                    addition += element + ","
            data += addition.rstrip(",") + "\n"

    with open(csvFile, mode="w", encoding="utf-8-sig") as file:
        file.truncate()
        file.write(data)

    print("Feminines created.")


def separateGenders(csvFile):
    data = ""

    with open(csvFile, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[1][0] != "0":
                for element in row:
                    data += element + ","
                data = data.rstrip(",") + "\n"
            else:
                firstRealPosition = 2
                masculineRow = ""
                feminineRow = ""
                
                while row[firstRealPosition][0] == "-":
                    firstRealPosition += 1
                
                softMarker = row[firstRealPosition][-1]
                masculineRow += row[0] + ","
                feminineRow += row[1][1:] + ","     #get rid of 0 
                
                if softMarker == "í":
                    for i in range(firstRealPosition, len(row)):
                        masculineRow += row[i] + ","
                        feminineRow += row[i] + ","
                    
                else:
                    firstFemPosition = 2 + (len(row) - firstRealPosition) / 2

                    for i in range(firstRealPosition, len(row)):
                        if i < firstFemPosition:
                            masculineRow += row[i] + ","
                        else:
                            feminineRow += row[i] + ","

                masculineRow = masculineRow.rstrip(",") + "\n"
                feminineRow = feminineRow.rstrip(",") + "\n"
                data += masculineRow + feminineRow

    with open(csvFile, mode="w", encoding="utf-8-sig") as file:
        file.truncate()
        file.write(data)

    print("Gendered adjectives separated.")


def createDatabase(csvFile, dbFile):
    with sqlite3.connect(dbFile) as con:
        cur = con.cursor()
        
        cur.execute('''CREATE TABLE IF NOT EXISTS yorani_words (
            yorani_id INTEGER PRIMARY KEY,
            yorani_word TEXT NOT NULL
        );''')

        cur.execute('''CREATE TABLE IF NOT EXISTS czech_words (
            czech_id INTEGER PRIMARY KEY,
            czech_word TEXT NOT NULL,
            reference_id INTEGER,
            FOREIGN KEY (reference_id) REFERENCES yorani_words(yorani_id)
        );''')

        con.commit()
    
    print(f"Database created at {dbFile}")


def main(inputFile, outputFile):
    print("Initiating...")
    
    replaceDelimiters(inputFile)
    dropDescription(inputFile)
    createFeminine(inputFile)
    separateGenders(inputFile)
    createDatabase(inputFile, outputFile)

    print("Finished successfully!")


if (__name__ == "__main__"):
    inputFile = str(sys.argv[1])
    outputFile = str(sys.argv[2])
    
    main(inputFile, outputFile)