import preprocess as p
import create_dict as cd
import create_feature_vector as cf
import machinelearn as ml
from sklearn.naive_bayes import MultinomialNB
from mpi4py import *
import datetime
import argparse

parser = argparse.ArgumentParser(description="Enter number of processes")
parser.add_argument('-p', '--process', action="store", dest="procnum", help="Number of processes", default="10")

#Used to know the dataset portion handled by the process
process_ct = int(parser.parse_args().procnum)
train_ct = 45251
test_ct = 30168
train_window = train_ct//process_ct
test_window = test_ct//process_ct
train_offset = train_ct%process_ct
test_offset = test_ct%process_ct

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def parallel_job():
    # Calculating indices of the segment to process
    if(rank<=train_offset):
        start_train = (rank-1)*train_window + rank
        end_train = rank*train_window + rank
    else:
        start_train = (rank-1)*train_window + train_offset + 1
        end_train = rank*train_window + train_offset
    if(rank<=test_offset):
        start_test = (rank-1)*test_window + rank + train_ct
        end_test = rank*test_window + rank + train_ct
    else:
        start_test = (rank-1)*test_window + test_offset + train_ct + 1
        end_test = rank*test_window + test_offset + train_ct

    # Preprocessing the segment assigned
    p.preprocess(start_train, end_train, rank)
    p.preprocess(start_test, end_test, rank)
    # Creating dictionary of the segment assigned
    dictionary_own = cd.create_dict(start_train, end_train, rank)
    # Sending own dictionary to the master node
    comm.send(dictionary_own, dest = 0)
    # Receiving combined dictionary of all processes
    dictionary_combined = comm.recv(source = 0)
    # Create local copy of combined dictionary
    file = open(str(rank)+"dictionary.txt", "w")
    word_list=list(dictionary_combined)
    word_list.sort()
    for i in word_list:
       file.write(str(i)+"\n")
    file.close()
    # Get features of the emails
    cf.create_feature(start_train, end_train, str(rank)+"train.csv", rank)
    cf.create_feature(start_test, end_test, str(rank)+"test.csv", rank)
    # Train model to dataset
    if(rank==1):
        multinomial = MultinomialNB(alpha = 0.01)
    else:
        multinomial = comm.recv(source = rank-1)

    (multinomial, accuracy_train) = ml.multinomial_train(start_train, end_train, multinomial, rank)
    
    if(rank!=process_ct):
        comm.send(multinomial, dest = rank+1)
    else:
        comm.send(multinomial, dest = 0)

    multinomial = comm.recv(source = 0)

    ml.multinomial_predict_test(start_test, end_test, multinomial, rank)

def aggregator_job():
    # Combine all dictionary of all the other nodes
    dictionary = set()
    for i in range(1, process_ct+1):
        dictionary = dictionary.union(comm.recv(source = i))
    # Send combined dictionary to all nodes
    for i in range(1, process_ct+1):
        comm.send(dictionary, dest=i)
    # Create local copy of combined dictionary
    file = open(str(rank)+"dictionary.txt", "w")
    word_list=list(dictionary)
    word_list.sort()
    for i in word_list:
       file.write(str(i)+"\n")
    file.close()

    multinomial = comm.recv(source = process_ct)
    for i in range(1, process_ct+1):
        comm.send(multinomial, dest = i)

def main():
    #other_node_job()
    if(rank == 0):
        aggregator_job()
    else:
        parallel_job()

start = datetime.datetime.now()
main()
end = datetime.datetime.now()
runtime = end-start
time_file = open(str(rank)+"runtime.txt", "w")
time_file.write(str(runtime))
time_file.close()
