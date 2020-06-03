from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import numpy as np

def multinomial_train(start, end):
    label_file = open("full/index", "r")
    labels = []

    for i in range(0, start):
        label_file.readline()

    for i in range(start, end):
        x = label_file.readline()
        if(x[:3]=="ham"):
            labels.append(1)
        else:
            labels.append(0)

    multinomial = MultinomialNB(alpha = 0.01)

    print("Training Multinomial Model")

    feature_matrix = []
    file = open("train.csv", "r")
    for i in range(start, end):
        instance=file.readline().split(',')
        try:
            row=list(map(int, instance))
        except:
            row=[]
        feature_matrix.append(row)
        if((i+1-start)%100==0 and i!=start):
            print(len(feature_matrix))
            multinomial.partial_fit(feature_matrix, np.array(labels[i-start-99:i-start+1]), classes=[0,1])
            print(multinomial)
            print(i)
            feature_matrix=[]
            m=i-start+1
        elif(i==end-1):
            print(len(feature_matrix))
            multinomial.partial_fit(feature_matrix, np.array(labels[m:end]), classes=[0,1])
            print(multinomial)
            print(i)
            feature_matrix=[]

    file = open("train.csv", "r")
    prediction = []
    print("Predicting Training Data...")
    for i in range(start, end):
        instance = file.readline().split(',')
        row = list(map(int,instance))
        k=multinomial.predict((np.array(row)).reshape(-1,len(row)))
        prediction.append(k)
    print(accuracy_score(labels[:end], prediction))
    print(len(labels), len(prediction))
    return multinomial

def multinomial_test(start, end, multinomial):
    print("Predicting Test Data...")
    file=open("test.csv", "r")
    labels = []
    prediction = []
    label_file = open("full/index", "r")
    for i in range(0, 75419):
        x = label_file.readline()
        if(x[:3]=="ham"):
            labels.append(1)
        else:
            labels.append(0)
    print("Len of Labels "+str(len(labels)))
    for i in range(52793, 75419):
        instance = file.readline().split(',')
        row = list(map(int,instance))
        k = multinomial.predict((np.array(row)).reshape(-1,len(row)))
        prediction.append(k)
    print(accuracy_score(labels[start:len(labels)], prediction))