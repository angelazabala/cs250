from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from mlxtend.classifier import EnsembleVoteClassifier
import numpy as np

def get_labels(start, end):
    label_file = open("full/index", "r")
    labels = []
    for i in range(1, start):
        label_file.readline()

    for i in range(start, end):
        x = label_file.readline()
        if(x[:3]=="ham"):
            labels.append(1)
        else:
            labels.append(0)

    return labels

def multinomial_train(start, end, multinomial, rank):
    #print("Training Multinomial Model")
    labels = get_labels(start, end)
    feature_matrix = []
    file = open(str(rank)+"train.csv", "r")
    for i in range(start, end):
        instance=file.readline().split(',')
        try:
            row=list(map(int, instance))
        except:
            print("hello")
            row=[]
        feature_matrix.append(row)
        if((i+1-start)%1000==0 and i!=start):
            print(len(feature_matrix))
            print(len(labels[i-start-999:i-start+1]))
            print(rank)
            multinomial.partial_fit(feature_matrix, np.array(labels[i-start-999:i-start+1]), classes=[0,1])
            feature_matrix=[]
            m=i-start+1
        elif(i==end-1):
            print(len(feature_matrix))
            print("we here")
            print(np.array(labels[4000:]))
            print(rank)
            print(m)
            print(start)
            print(end)
            multinomial.partial_fit(feature_matrix, np.array(labels[m:end]), classes=[0,1])
            feature_matrix=[]
    file = open(str(rank)+"train.csv", "r")
    prediction = []
    print("Predicting Training Data...")
    for i in range(start, end):
        instance = file.readline().split(',')
        row = list(map(int,instance))
        k=multinomial.predict((np.array(row)).reshape(-1,len(row)))
        prediction.append(k)
    accuracy = accuracy_score(labels, prediction)
    file = open(str(rank)+"train_results.txt", "w")
    file.write(str(accuracy)+"\n")
    file.close()
    print(str(rank)+" "+str(accuracy))
    return (multinomial, accuracy)

def multinomial_predict_test(start, end, multinomial, rank):
    labels = get_labels(start, end)
    file = open(str(rank)+"test.csv", "r")
    prediction = []
    for i in range(start, end):
        instance = file.readline().split(',')
        row = list(map(int,instance))
        k = multinomial.predict((np.array(row)).reshape(-1,len(row)))
        prediction.append(k)
    accuracy = accuracy_score(labels, prediction)
    file = open(str(rank)+"predict_test_results.txt", "w")
    file.write(str(accuracy)+"\n")
    file.close()
    print(str(accuracy))

    return accuracy