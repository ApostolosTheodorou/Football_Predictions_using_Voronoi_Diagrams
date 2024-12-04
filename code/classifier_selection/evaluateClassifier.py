from dataPreprocessing import makeCsv, scaleData, defineTrainingAndTestingSets
import time

from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, matthews_corrcoef

import pygame
import metrics

FOLDS= 5                                  # The number of different folds that will be used to evaluate the classifiers
classifiers= {0:'Random Forest', 1:'Decision Tree', 2:'Support Vector Classifier',
              3:'Logistic Regression', 4:'Multinomial Naive Bayes', 
              5:'k-Nearest Neighbors', 6:'Neural Network'}                                                                          
def testClassifiers():
    start= time.time()
    clf=[]                                                        # A list with all the classifiers that will be tested
    clf.append(RandomForestClassifier())
    clf.append(tree.DecisionTreeClassifier())
    clf.append(svm.SVC())
    clf.append(LogisticRegression())
    clf.append(MultinomialNB())
    clf.append(KNeighborsClassifier())
    clf.append(MLPClassifier())
    
    makeCsv(FOLDS)

    averagePrecision= []
    averageRecall= []
    goalPrecision= []
    goalRecall= []
    averageMcc= []
    averageF1= []
    f1PerClass= []
    for i in range(0, len(clf)):
        averagePrecision.append(0)
        averageRecall.append(0)
        goalPrecision.append(0)
        goalRecall.append(0)
        averageMcc.append(0)
        averageF1.append(0)
        f1PerClass.append([])

    for fold in range(1,FOLDS+1):
        X_train, Y_train, X_test, Y_test= defineTrainingAndTestingSets(fold)
        X_test, X_train= scaleData(X_test, X_train)
        
        print(f'FOLD {fold}')
        for i in range(0,len(clf)):
            clf[i]= clf[i].fit(X_train, Y_train) 
            y_pred= clf[i].predict(X_test)  
            print('CLF ' + str(i))
            avPrecision, avRecall, prec, rec= metrics.printMetrics(y_pred, Y_test)
            averagePrecision[i]+= avPrecision
            averageRecall[i]+= avRecall
            goalPrecision[i]+= prec
            goalRecall[i]+= rec
            averageMcc[i]+= matthews_corrcoef(Y_test, y_pred)
            averageF1[i]+= f1_score(Y_test, y_pred, average='macro')
            f1PerClass[i]= f1_score(Y_test, y_pred, average=None)
            print(f'\nf1 per class: {f1PerClass[i]}')###############
            print('\n')
    for i in range(0, len(clf)):
        averagePrecision[i]/= FOLDS
        averageRecall[i]/= FOLDS
        goalPrecision[i]/= FOLDS
        goalRecall[i]/= FOLDS
        averageMcc[i]/= FOLDS
        averageF1[i]/= FOLDS
    

    print('\n\nSummary\n-------\n-------')
    print('Average Precision:')
    for i in range(0, len(averagePrecision)):
        print(f'{classifiers[i]} {averagePrecision[i]}')
    print('\nAverage Recall:')
    for i in range(0, len(averageRecall)):
        print(f'{classifiers[i]} {averageRecall[i]}')
    print('\nGoal Precision:')
    for i in range(0, len(goalPrecision)):
        print(f'{classifiers[i]} {goalPrecision[i]}')
    print('\nGoal Recall:')
    for i in range(0, len(goalRecall)):
        print(f'{classifiers[i]} {goalRecall[i]}')
    print('\nAverage MCC:')
    for i in range(0, len(goalPrecision)):
        print(f'{classifiers[i]} {averageMcc[i]}')
    print('\nAverage F1 score:')
    for i in range(0, len(goalPrecision)):
        print(f'{classifiers[i]} {averageF1[i]}')
    end= time.time()

    print(f'Time: {end-start}s')

testClassifiers() 
pygame.mixer.init()
pygame.mixer.music.load("./sound.mp3")
pygame.mixer.music.play()
time.sleep(15)









