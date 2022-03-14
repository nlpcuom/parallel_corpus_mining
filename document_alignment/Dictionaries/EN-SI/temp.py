def printer(filename):
    lines = open(filename,"r").readlines()
    x = 0
    for line in lines:
        word = line.strip().replace("\n","")
        if (len(word) < 3):
            x = x + 1
            # print(word)
    print(x)

printer("test.en")
printer("existingdictionary.en")