lines = open("english-sinhala_dictionary.txt", "r").readlines()

asas = 0

with open("ensidic.en", "w") as wfile1:
    with open("ensidic.si", "w") as wfile2:
        for line in lines:
            x = line.strip().replace("\n", "").split("-")
            if (len(x) == 2):
                y = x[1].strip().split("|")
                for word in y:
                    wfile1.write(x[0].strip().lower() + "\n")
                    wfile2.write(word.strip() + "\n")
            else:
                asas = asas + 1
                # print(x)

print(asas)