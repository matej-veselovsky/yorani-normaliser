def replaceDelimiters(csv_file):
    data = ""

    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        data = file.read().replace("\\,", ",").replace("\\", ",").replace("/", ",")

    with open(csv_file, mode="w") as file:
        file.truncate()
        file.write(data)

def main():
    replaceDelimiters("yoranish.csv")

if (__name__ == "__main__"):
    main()