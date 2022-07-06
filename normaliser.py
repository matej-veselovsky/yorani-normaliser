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

                    screener = len(masculineForm) - 1
                    
                    if suffix == "cekaa":
                        screener -= len("sikayi")
                    elif suffix == "wiā":
                        screener -= len("veyi")
                    elif suffix == "liā":
                        screener -= len("neyi")
                    elif suffix == "huā":
                        screener -= len("gayi")
                    elif suffix == "tuneā":
                        screener -= len("neyi")
                    elif suffix == "ā":
                        screener -= len("neyi")
                    else:
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
    oddList = ""

    with open(csvFile, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:            
            if row[1][0] != "0":        # check if row even needs to be separated
                for element in row:
                    data += element + ","
                data = data.rstrip(",") + "\n"
            else:
                firstRealPosition = 2
                masculineRow = ""
                feminineRow = ""
                
                while row[firstRealPosition][0] == "-": # skips unnecessary suffixes
                    firstRealPosition += 1

                masculineRow += row[0] + ","
                feminineRow += row[1][1:] + ","     #get rid of 0
                currentPosition = firstRealPosition
                skips = currentPosition
                
                while currentPosition < len(row):                    
                    if currentPosition < skips:
                        currentPosition += 1
                        continue
                    
                    softMarkerElement = row[currentPosition].strip()
                    softMarker = softMarkerElement[-1]                 
                    
                    if softMarker == "í":   # soft adjectives
                        addition = ""
                        seMarker = softMarkerElement[:3]

                        if seMarker == "se ":
                            addition += softMarkerElement[3:] + " " + seMarker.rstrip() + ","
                        else:                        
                            addition += softMarkerElement + ","

                        masculineRow += addition
                        feminineRow += addition

                        
                    else:                   # hard adjectives
                        skips = currentPosition + 1

                        while skips < len(row): # search for length of hard adjective chain
                            consideredElement = row[skips].rstrip() 
                            if consideredElement[-1] != "í":
                                skips += 1
                            else:
                                break

                        currentLength = skips - currentPosition
                        firstFemPosition = currentPosition + currentLength / 2

                        if currentLength % 2 != 0:
                            oddList += row[0] + "\n"
                            raiseSeparatorWarning(row[0], "odd")                            

                        if firstFemPosition < currentPosition:
                            raiseSeparatorWarning(row[0], "position")


                        for i in range(currentPosition, skips):
                            if i < firstFemPosition:
                                masculineRow += row[i] + ","
                            else:
                                feminineRow += row[i] + ","

                    currentPosition += 1


                masculineRow = masculineRow.rstrip(",") + "\n"
                feminineRow = feminineRow.rstrip(",") + "\n"
                data += masculineRow + feminineRow

    with open(csvFile, mode="w", encoding="utf-8-sig") as file:
        file.truncate()
        file.write(data)

    with open("./testfiles/odds.txt", mode="w", encoding="utf-8-sig") as file:
        file.write(oddList)

    print("Gendered adjectives separated.")

def raiseSeparatorWarning(row, type):
    if type == "odd":
        print(f"Warning! Found odd separated length at {row}")

    if type == "position":
        print(f"Warning! Found nonsensical order at {row}")


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

        with open(csvFile, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            reader.__next__     # skips column names

            temp = []
            n = 1

            for row in reader:
                cur.execute('''INSERT INTO yorani_words(yorani_word) VALUES (?);''', (row[0],))

                for element in row[1:]:
                    temp.append([n, element])

                n += 1

            for row in temp:
                cur.execute('''INSERT INTO czech_words(czech_word, reference_id) 
                VALUES (?,?);''', (row[1], row[0]))

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