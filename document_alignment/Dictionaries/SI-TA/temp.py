silines = open("name_address.tok-cl.si-ta.si", "r").readlines()
talines = open("name_address.tok-cl.si-ta.ta", "r").readlines()

siwords = []
tawords = []

# for siline in silines:
#     print(siline)
#     words = siline.replace("\n", "").strip().split()
#     for word in words:
#         siwords.append(word.strip().replace("\n", ""))
# for taline in talines:
#     words = taline.replace("\n", "").strip().split()
#     for word in words:
#         tawords.append(word.strip().replace("\n", ""))

for i in range(len(silines)):
    siwordlist = silines[i].replace("\n", "").strip().split()
    tawordlist = talines[i].replace("\n", "").strip().split()
    if len(siwordlist) == len(tawordlist):
        for j in range(len(siwordlist)):
            siwords.append(siwordlist[j])
            tawords.append(tawordlist[j])

with open("a.txt", "w") as writefile:
    for siword in siwords:
        writefile.write(siword + "\n")

with open("b.txt", "w") as writefile:
    for taword in tawords:
        writefile.write(taword + "\n")