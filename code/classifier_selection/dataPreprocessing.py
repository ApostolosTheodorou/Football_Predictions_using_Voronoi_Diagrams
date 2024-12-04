from pngConvert import png2csv
import os
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
import pandas as pd

def makeCsv(folds):
    folds= int(folds)
    testCsvs= []
    trainingCsvs=[]
    for i in range (1, folds+1):
        testCsvs.append(open('testSet-' + str(i) + '.csv', 'a'))
        trainingCsvs.append(open('trainingSet-' + str(i) + '.csv', 'a'))
    for item in os.listdir(os.getcwd()):
        if os.path.isdir(item) and item[0]=='F':
            fold= item[-1]
            # Create the testSet csv file
            for match in os.listdir('./' + item + '/testSet'):
                for attempt in os.listdir('./' + item + '/testSet/' + match):
                    png2csv(('./' + item + '/testSet/' + match + '/' + attempt), testCsvs[int(fold)-1])
            # Create the trainingSet csv file
            for match in os.listdir('./' + item + '/trainingSet'):
                for attempt in os.listdir('./' + item + '/trainingSet/' + match):
                    png2csv(('./' + item + '/trainingSet/' + match + '/' + attempt), trainingCsvs[int(fold)-1])

def scaleData(X_test, X_train):
    max_abs_scaler= MaxAbsScaler()
    X_train= max_abs_scaler.fit_transform(X_train)
    X_test= max_abs_scaler.fit_transform(X_test)
    return X_test, X_train

def defineTrainingAndTestingSets(fold):
    X_train= [] 
    Y_train= [] 
    X_test= [] 
    Y_test= []  
    trainingSet= pd.read_csv('./trainingSet-' + str(fold) + '.csv',header=None)# trainingSet= pd.read_csv('./testCSV.csv',header=None)# trainingSet= pd.read_csv(self.trainingData,header=None)
    X_train= trainingSet.iloc[:, :(trainingSet.shape[1]-1)].values# self.X_train= trainingSet.iloc[:, :(self.trainingData.shape[1]-1)].values 
    Y_train= trainingSet.iloc[:, -1].values
    testingSet= pd.read_csv('./testSet-' + str(fold) + '.csv',header=None)
    X_test= testingSet.iloc[:, :(testingSet.shape[1]-1)].values 
    Y_test= testingSet.iloc[:, -1].values
    return X_train, Y_train, X_test, Y_test