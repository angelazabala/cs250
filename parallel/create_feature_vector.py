def count_instance(mail_name, dictionary):
	mail = str(open(mail_name, "r").read()).split()
	instance = ""
	for i in dictionary:
		instance += (str(mail.count(i))+",")

	return instance[:-1]

def create_feature(start, end, csv, rank):
	dictionary = str(open(str(rank)+"dictionary.txt", "r").read()).split()
	feature_vector = open(csv, "w")

	for i in range(start, end):
		print("Creating feature_vector for "+str(rank)+"data2/inmail."+str(i))
		feature_vector.write(count_instance(str(rank)+"data2/inmail."+str(i), dictionary)+"\n")
	feature_vector.close()