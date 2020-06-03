import enchant

def create_dict(start, end, rank):
    dictionary = set()

    for i in range(start, end):
        mail = open(str(rank)+"data2/inmail."+str(i), "r")
        print("Creating dictionary for"+str(rank)+"data2/inmail."+str(i))
        words = str(mail.read()).split()
        for j in words:
            dictionary.add(j)

    return dictionary
