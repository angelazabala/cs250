import enchant

def create_dict():
    dictionary = set()

    for i in range(1, 75420):
        mail = open("data2/inmail."+str(i), "r")
        print("Creating dictionary for data2/inmail."+str(i))
        words = str(mail.read()).split()
        for j in words:
            dictionary.add(j)

    file = open("dictionary.txt", "w")

    word_list=list(dictionary)
    word_list.sort()
    for i in word_list:
        file.write(str(i)+"\n")

    print(word_list)
