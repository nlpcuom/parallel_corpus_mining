silines = open("person-names.si").readlines()

talines = open("person-names.ta").readlines()

dict = {}

for i in range(len(silines)):
    temp = silines[i].strip().replace("\n", "")
    if (dict.get(temp, False)):
        arr = dict[temp]
        if (talines[i].strip().replace("\n", "") not in arr):
            arr.append(talines[i].strip().replace("\n", ""))
            dict[temp] = arr
    else:
        dict[temp] = [talines[i].strip().replace("\n", "")]


with open("./a.si", "w") as enwritefile:
    with open("./b.ta", "w") as siwritefile:
        for key, values in dict.items():
            for value in values:
                enwritefile.write(key + "\n")
                siwritefile.write(value + "\n")
            print(key, values)