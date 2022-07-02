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

def main(file):
    replaceDelimiters(file)
    dropDescription(file)

if (__name__ == "__main__"):
    file = str(sys.argv[1])
    main(file)