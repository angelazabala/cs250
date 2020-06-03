import preprocess as p
import create_dict as cd
import create_feature_vector as cf
import machinelearn as ml
import datetime

start = datetime.datetime.now()
p.preprocess()
cd.create_dict()
cf.create_feature(1, 52794, "train.csv")
cf.create_feature(52794, 75420, "test.csv")
ml.multinomial_test(52793, 75420, ml.multinomial_train(0, 52793))
end = datetime.datetime.now()

runtime = end-start
time_file = open("runtime.txt", "w")
time_file.write(str(runtime))
time_file.close()
