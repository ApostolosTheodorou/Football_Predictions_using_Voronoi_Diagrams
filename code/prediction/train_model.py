import time
import os
import shutil
import cv2
import numpy as np
import pandas as pd
import argparse
from enum import Enum
#from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import *
from skops.io import dump, load, get_untrusted_types

IMAGE_HEIGHT= 160
IMAGE_WIDTH= 240
IMAGE_HEIGHT_AFTER_CROP= int(0.9*IMAGE_HEIGHT)-int(0.15*IMAGE_HEIGHT)
IMAGE_WIDTH_AFTER_CROP= int(0.82*IMAGE_WIDTH)-int(0.2*IMAGE_WIDTH)
FEATURES_AFTER_IMAGE_SIZE_REDUCTION= ((int(0.9*IMAGE_HEIGHT)-int(0.15*IMAGE_HEIGHT))       # Image height
                                      * (int(0.82*IMAGE_WIDTH)-int(0.2*IMAGE_WIDTH))      # Image width
                                      * 3)                                                 # RGB 3 values per pixel

#Command line arguments handling
parser= argparse.ArgumentParser()
parser.add_argument('-p', '--path', metavar='path', required= True, 
                    help='The path to the folder where the matchdays are stored')
parser.add_argument('-t', '--team', metavar='team', required= False,
                    default= 'All', help="The code name of the team whose attempts\
                    will train the model\nCode names for super league 2021-2022:\n\
                    aek for A.E.K\napo for APOLLON SM.\nari for ARIS\n\
                    ast for ASTERAS TRIP.\natr for ATROMITOS ATH.\nion for IONIKOS\n\
                    gia for PAS GIANNINA\nlam for PAS LAMIA\noly for OLYMPIAKOS\n\
                    ofi for O.F.I.\npan for PANETOLIKOS\npao for PANATHINAIKOS\n\
                    the for P.A.O.K.\nvol for VOLOS NFC" )
parser.add_argument('-c', '--classifier', metavar='classifier', required= False,
                    default= 'Decision Tree', help="The classifier that will be used\
                    to train the model\nThe available choices are:\n\
                    Decision Tree\n SVC (Support vector classification)\n\
                    Random Forest\nNearest Neighbors\nNaive Bayes\nNeural Network\n\
                    Multinomial Logistic Regression")
parser.add_argument('-str', '--trainingSetFirstDay', required= True,
                      help= 'The first matchday of the training set')
parser.add_argument('-etr', '--trainingSetLastDay', required= True,
                      help= 'The last matchday of the training set')
parser.add_argument('-ste', '--testingSetFirstDay', required= True,
                      help='The first matchday of the testing set')
parser.add_argument('-ete', '--testingSetLastDay', required= True,
                      help= 'The last matchday of the testing set')
parser.add_argument('-s', '--save', required= False, default= False,
                      help= 'A boolean that determines wether the model will be\
                            saved locally after it has been trained, so that it\
                            can e used to other testing sets later')
parser.add_argument('-l', '--load', required= False, default= False,
                      help= 'The name of the file where the pretrained model\
                             that will be loaded and used is stored')
args= parser.parse_args()

def showArgs():
    print(args.load)

''' This function receives a path to a file 
    strips the file hierarchy tree and returns only the file's name
    Example: Input: ./Desktop\\Matchdays\1\aek-ion\1-aek-ion-ion-25.png
    Output: 1-aek-ion-ion-25.png '''  
def stripFilesName(path):
    pos= -1
    char= path[pos]
    while char != "\\" and char != "/":
        pos-=1
        char=path[pos]
    pos+=1
    return path[pos:]

''' This function receives a team and a match and examines wether the team 
    participates in that match
    Example 1: isTeamsMatch('pao', 'oly-pao') --> True
    Example 2: isTeamsMatch('pao', 'the-ari') --> False '''
def isTeamsMatch (team, match):
    if team == match[0:3] or team == match[4:] or team == 'All':
        return True
    else:
        return False
    
''' This function receives a team and an attempt and examines wether the 
    attempt was made by the team
    Example 1: isTeamsAttempt('pan', '2-pan-atr-pan-16.png') --> True
    Example 2: isTeamsAttempt('pan', '5-the-ari-the-87.png') --> False 
    Example 3: isTeamsAttempt('pan', '3-pan-lam-lam-11.png') --> False '''
def isTeamsAttempt (team, attempt):
    if team == attempt[10:13] or team == 'All':
        return True
    else:
        return False


class Analytics:        
    def countAttemptsPerClass(self, team, startingMatchday, endingMatchday):
        # Create the lists of the classes and a counter for each class
        classes=[]                                                              # A list to store the classes
        counters=[]                                                             # A list to store the counter of each class
        # Examine the attempts of the requested in the requested range 
        for matchday in os.listdir(args.path):                                  # For every matchday
            if int(matchday) >= int(startingMatchday) and int(matchday) <= int(endingMatchday):   # That is inside the requested range
                matchdayFolder= os.path.join(args.path, matchday)               # Update the current directory's path
                for match in os.listdir(matchdayFolder):                        # For every match
                    if isTeamsMatch(team, match):                               # If it is a match that was palyed by the requested team
                        matchFolder= os.path.join(matchdayFolder, match)        # Update the current directory's path
                        for attempt in os.listdir(matchFolder):                 # For every attempt of this match
                            if isTeamsAttempt(team, attempt):                   # In which the requested team was the attacking team
                                category= int(attempt[0])                            # Detect the class of the attempt (0->poor ... 5->goal)
                                if category in classes:                         # If another attempt of the same class has been recorded
                                                                                # and inserted in the classes list
                                    counters[classes.index(category)]+= 1       # Augment the counter of this category
                                else:                                           # If it is the first time that this class is being recrded
                                    classes.append(int(category))                    # Create a record for this class in the classes list
                                    counters.append(int(1))                     # Initialize the counter of the class in the classes counters
                            else: continue                                      # If the requested team was defending move on to the next attempt
                    else: continue                                              # If the requested team does not play in this match move on
            else: continue                                                      # If the matchday is out of the specified range
        print('Classes: ')
        print(classes)
        print('Counters: ')
        print(counters)
        # Sort the classes in ascendind order
        classesAndCounters=[]                                                   # Create a list of pairs [(class1, counter1),...]
        for i in range(len(classes)):
            classesAndCounters.append((classes[i], counters[i]))                # Initialize the list of pairs
        classesAndCounters.sort(key= lambda pair: pair[0])                      # Sort the list depending on the class value 
        # Calculate the sum of the attempts 
        total= sum(pair[1] for pair in classesAndCounters)
        # Print the results
        print(f'Total attempts: {total}')
        print('\nAttempts per class\n')
        for pair in classesAndCounters:
            print(f'Class {pair[0]}:\t{pair[1]} attempts\t({round(pair[1]/total*100, 2)} %)\n')

    def printAttemptsPerTeam(team):
        matches= 0
        attemptsPerCategory= {'1':0, '2':0, '3':0, '4':0, '5':0}
        matchdaysDirectory= './matchdays'
        for matchday in os.listdir(matchdaysDirectory):
            matchdayDirectory= matchdaysDirectory + '/' + matchday
            for match in os.listdir(matchdayDirectory):
                if isTeamsMatch(team, match):
                    matchDirectory= matchdayDirectory + '/' + match
                    for attempt in os.listdir(matchDirectory):
                        if isTeamsAttempt(team, attempt):
                            category= attempt[0]
                            attemptsPerCategory[category]+= 1
        totalAttempts= sum(attemptsPerCategory)
        
        print(f'{team}   {totalAttempts}   {attemptsPerCategory["1"]}'
              f'{attemptsPerCategory["2"]}   {attemptsPerCategory["3"]}'   
              f'{attemptsPerCategory["4"]}   {attemptsPerCategory["5"]}')



# A class enumerating the possible categories an attempt can belong to 
class Attempt(Enum):
    POOR= 1
    MEDIOCORE= 2
    GOOD= 3
    SAVE= 4
    GOAL= 5
        

class Set(Enum):
    training= 1
    testing= 2


class Voronoi_Match_Prediction:

    def __init__(self, trainingSetFirstDay, trainingSetLastDay, testingSetFirstDay,
                 testingSetLastDay, path, classifier, specificTeam= 'All'):
        
        self.trainingSetFirstDay= int(args.trainingSetFirstDay)          # The first matchday of the training set
        self.trainingSetLastDay= int(args.trainingSetLastDay)            # The last matchday of the training set
        self.testingSetFirstDay= int(args.testingSetFirstDay)            # The first matchday of the testing set
        self.testingSetLastDay= int(args.testingSetLastDay)              # The last matchday of the testing set
        self.voronoiDiagramsDirectory= args.path         # The path of the directory that contain the voronoi diagrams.
                                                    # The directory contains a subdirectory for every matchday of 
                                                    # of the season, which contains a subdirectory for every match
                                                    # played this matchday
        self.team= specificTeam                     # The team whose attempts will be used to train the model
                                                    # If team == "All" then all the available attempts will be
                                                    # used independently of the team
        self.classifierAlgorithm= classifier                 # The algorithm that will classify the attempts of the testing 
                                                    # set into classes
        self.clf= None                             # The classifier
        self.trainingData= None                     # A csv file that will contain all the trainig data, will be initialized later
        self.testingData= None                      # A csv file that will contain all the testig data, will be initialized later
        # Lists that contain the variable vectors and the category vectors
        self.X_train=[]
        self.X_test=[]
        self.Y_train=[]
        self.Y_test=[]
        self.y_pred= None
        self.csvFiles=[]                           # A list of all the csv files (training and testing) for each category

    ''' This function converts a png image into a csv file
        The initial png image is a voronoi diagram
        The csv outpout format is used to train and test the model '''
    def png2csv(self, pngImg, csvFile):
        img= cv2.imread(pngImg)     
        print(img.shape)                                            # Read the voronoi diagram as a png image
        img= cv2.resize(img, (IMAGE_WIDTH,IMAGE_HEIGHT))                        # Give the image a smaller size
        img= img[int(0.15*IMAGE_HEIGHT):int(0.9 * IMAGE_HEIGHT), 
                 int(0.2 * IMAGE_WIDTH):int(0.82 * IMAGE_WIDTH)]
        print(img.shape)
        #newWidth, newHeight= img.shape
        img= img.flatten()        
        print(img.shape)       
        print(f'Features after reduction: {FEATURES_AFTER_IMAGE_SIZE_REDUCTION}')                                       # Convert the image into an one dimensional array
        fileName= stripFilesName(pngImg)                                        # Take the file's name without hierarchy folders above (path)
        img= np.append(img,fileName[0]).reshape(1, FEATURES_AFTER_IMAGE_SIZE_REDUCTION+1)                 # Add the category (label)(0-5) as the last value of the array
        pd.DataFrame(img).to_csv(csvFile, mode='a', header=False, index=False)  # Insert the numeric array as a new line into a csv file 


    ''' This functios creates one empty csv file per category for training and testing
        and two empty accumulative csv files that will contain the whole training and testing datasets '''
    def createEmptyCsvFiles(self):
        self.trainingData= open('trainingSet.csv', 'a') # A csv file that will contain all the trainig data
        self.testingData= open('testingSet.csv', 'a')   # A csv file that will contain all the testig data
        for attempt in Attempt:
            csvsPerAttempt=[]
            for set in Set:
                csvsPerAttempt.append(open("csv_"+ str(attempt.value)+ "_" + set.name +".csv", 'a'))
                os.mkdir('./' + str(attempt.value) + '_' +  set.name)    
            self.csvFiles.append(csvsPerAttempt)

    ''' This function deletes the directories and the csv files which were created 
        during the training of the last model'''
    def deleteCsvFilesFromPreviousTrainings(self):
        # Delete the folders and the csv files of the previous model (if exist any of those)
        if os.path.isfile('testingSet.csv'):
            os.remove('testingSet.csv')
        if os.path.isfile('trainingSet.csv'):
            os.remove('trainingSet.csv')
        for attempt in Attempt:
            for set in Set:
                path= "csv_"+ str(attempt.value)+ "_" + set.name +".csv"
                if os.path.isfile(path):
                    os.remove(path)
                path= str(attempt.value) + '_' +  set.name
                if os.path.isdir(path):
                    directoryContents= os.listdir(path)
                    for file in directoryContents:
                        os.remove(path + '/' + str(file))
                    os.rmdir(path)

    ''' This function reads the directory that contains all diagrams and separates
        them according to their category (1->poor attemp, 2-> mediocore attempt,
        3->good attempt, 4-> save, 5->goal) into directories as images
        and into csv files as numeric data (pixel values) '''
    def splitDiagramsIntoDirectoriesAndCsvs(self):    
        testSetCreation= False                                      
        for matchday in os.listdir(self.voronoiDiagramsDirectory):  # For every matchday
            print(matchday)
            testSetCreation= False    ################# 
            if (int(matchday) >= self.testingSetFirstDay 
            and int(matchday) <= self.testingSetLastDay):    
                testSetCreation= True                               # The new diagrams will be used as a testing set
                print("TEST MODE")
            if ((int(matchday) < self.testingSetFirstDay or int(matchday) > self.testingSetLastDay)
            and (int(matchday) < self.trainingSetFirstDay or int(matchday) > self.trainingSetLastDay)):
                print('Not interested, thank you!')
                continue                               
            currentDay= os.path.join(self.voronoiDiagramsDirectory, matchday)
            for match in os.listdir(currentDay):                    # For every match of the matchday
                if self.team != 'All' and not isTeamsMatch(self.team, match):   # If the model corresponds to a specific
                    continue                                                    # team, ignore the matches in which the 
                                                                                # team does not participate
                print(match)
                currentMatch= os.path.join(currentDay, match)
                for attempt in os.listdir(currentMatch):            # For every attempt of the match
                    if self.team != 'All' and not isTeamsAttempt(self.team, attempt): # If the attempt was made by the 
                        continue                                                      # opponent do not use it in the training
                                                                                      # of the team's model
                    print(attempt)
                   # Classify the attempt to one of the classes (1-5)
                    if not testSetCreation:                         # If the collected data will be used for training the model
                        # Classify the voronoi diagram into the corresponding folder as an image
                        shutil.copy(os.path.join(currentMatch, attempt), './' + attempt[0] + '_training')
                        # Convert the voronoi diagram image into numeric data and store them in the category's csv file
                        self.png2csv(os.path.join(currentMatch, attempt), self.csvFiles[int(attempt[0])-1][Set.training.value-1])
                        # Convert the voronoi diagram image into numeric data and store them in the accumulative csv file as well
                        self.png2csv(os.path.join(currentMatch, attempt), self.trainingData)
                    elif testSetCreation:                           # If the collected data will be used for testing the model
                        # Classify the voronoi diagram into the corresponding folder as an image
                        shutil.copy(os.path.join(currentMatch, attempt), './' + attempt[0] + '_testing')
                        # Convert the voronoi diagram image into numeric data and store them in the category's csv file
                        self.png2csv(os.path.join(currentMatch, attempt), self.csvFiles[int(attempt[0])-1][Set.testing.value-1])
                        # Convert the voronoi diagram image into numeric data and store them in the accumulative csv file as well
                        self.png2csv(os.path.join(currentMatch, attempt), self.testingData)
                        
    def defineTrainingAndTestingSets(self):
        trainingSet= pd.read_csv('./trainingSet.csv',header=None)# trainingSet= pd.read_csv('./testCSV.csv',header=None)# trainingSet= pd.read_csv(self.trainingData,header=None)
        self.X_train= trainingSet.iloc[:, :(trainingSet.shape[1]-1)].values# self.X_train= trainingSet.iloc[:, :(self.trainingData.shape[1]-1)].values 
        self.Y_train= trainingSet.iloc[:, -1].values
        print(f'Training Set:  {self.X_train}')
        print(f'Test set:  {self.Y_train}')
        print(f'Training Set Len: {len(self.X_train)}')
        print(f'Test set len: {self.Y_train}')
        testingSet= pd.read_csv('./testingSet.csv',header=None)
        self.X_test= testingSet.iloc[:, :(testingSet.shape[1]-1)].values 
        self.Y_test= testingSet.iloc[:, -1].values

    def scaleData(self):
        min_max_scaler= MaxAbsScaler()
        self.X_train= min_max_scaler.fit_transform(self.X_train)
        self.X_test= min_max_scaler.fit_transform(self.X_test)

    def trainModel(self):
        # Select classification algorithm
        match self.classifierAlgorithm:
            case "Decision Tree":
                from sklearn import tree
                self.clf = tree.DecisionTreeClassifier()
            
            case "SVC":                                                         # Stands for Support Vector Classification
                from sklearn import svm
                self.clf= svm.SVC()

            case "Multinomial Logistic Regression":
                from sklearn.linear_model import LogisticRegression
                #self.clf = LogisticRegression(solver='lbfgs', class_weight= {1:1.00, 2:1.00, 3:0.60, 4:1.20, 5:1.25})
                self.clf = LogisticRegression(solver='lbfgs')
            case "Naive Bayes":
                from sklearn.naive_bayes import MultinomialNB
                self.clf = MultinomialNB()

            case 'Random Forest':
                from sklearn.ensemble import RandomForestClassifier
                #self.clf= RandomForestClassifier(n_estimators=100, max_depth= None)
                self.clf= RandomForestClassifier(n_estimators=50, max_features= 150, max_depth= 10,
                                                  min_samples_leaf= 5, class_weight={1:1.45, 2:1.16, 3:0.87, 4:1.24, 5:0.83})
            
            case 'Nearest Neighbors':
                from sklearn.neighbors import KNeighborsClassifier
                self.clf= KNeighborsClassifier(n_neighbors= 5)

            case 'Neural Network':
                from sklearn.neural_network import MLPClassifier
                self.clf= MLPClassifier(hidden_layer_sizes= 7, activation='relu', solver='adam')
        
        self.scaleData()                                                        # Scale the data
        self.clf= self.clf.fit(self.X_train, self.Y_train)                      # Train the model
        if args.save != False:
            self.saveModel(self.clf, args.save)

    ''' This function prints evaluation metrics for checking 
        the efficiency of the requested trained model'''
    def showMetrics(self):
        # Metric functions for evaluation of the model's quality
        print(cross_val_score(self.clf, self.X_test, self.Y_test, cv=5))
        accuracy = accuracy_score(self.Y_test, self.y_pred)
        balancedAccuracy= balanced_accuracy_score(self.Y_test, self.y_pred)          # The average of recall obtained on each class
        precision= precision_score(self.Y_test, self.y_pred, labels=None, average='macro', zero_division='warn')
        recall= recall_score(self.Y_test, self.y_pred, labels=None, average='macro', zero_division='warn')
        f1= f1_score(self.Y_test, self.y_pred, labels=None, average='macro', zero_division='warn')
        matthewsCorCoef= matthews_corrcoef(self.Y_test, self.y_pred)
        print(f"Accuracy: {accuracy}\nBalanced Accuracy: {balancedAccuracy}\n\
              Precision: {precision}\nRecall: {recall}\nF1 score: {f1}\nMatthews correlation coefficient: {matthewsCorCoef}")
        for i in range(len(self.Y_test)):
            print(f'Real value: {self.Y_test[i]} ---> Predicted value: {self.y_pred[i]}  Difference: {self.y_pred[i]-self.Y_test[i]}')
        
    def showConfusionMatrix(self):
        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        import matplotlib.pyplot as plt

        cm= confusion_matrix(self.Y_test, self.y_pred, labels=[1, 2, 3, 4, 5])
        disp = ConfusionMatrixDisplay(cm, display_labels=[1, 2, 3, 4, 5])
        disp.plot(cmap=plt.cm.Blues)
        plt.show()


    ''' This function saves a trained model using the skops library
        For more information about skops see: https://skops.readthedocs.io/en/stable/index.html'''
    def saveModel(self, clf, fileName):
        os.makedirs('./savedModels', mode=0o777, exist_ok=True)
        fileName= './savedModels/' + fileName + '.skops'
        open(fileName, 'w+')
        dump(clf, fileName)
    
    ''' This functions loads a trained model using skops library
        For more information about skops see: https://skops.readthedocs.io/en/stable/index.html'''
    def loadModel(self, file):
        trainedModel= load(file, trusted=None)
        return trainedModel

    def makePrediction(self):
        self.deleteCsvFilesFromPreviousTrainings()
        self.createEmptyCsvFiles()
        self.splitDiagramsIntoDirectoriesAndCsvs()
        self.defineTrainingAndTestingSets()
        if args.load == False:
            modelTrainingTimeStart= time.time()
            self.trainModel()
            modelTrainingTimeEnd= time.time()
            print(f'Model training time: {modelTrainingTimeEnd-modelTrainingTimeStart} s')
        else:
            self.clf= self.loadModel(args.load)
        self.y_pred= self.clf.predict(self.X_test)                                        # Make predictions for the given test set
        self.showMetrics()

  
def runPrediction ():
    programExecutionStart = time.time()
    analytics= Analytics()
    analytics.countAttemptsPerClass(args.team, args.testingSetFirstDay, args.testingSetLastDay)
    myPrediction= Voronoi_Match_Prediction(args.trainingSetFirstDay, args.trainingSetLastDay,
                                           args.testingSetFirstDay, args.testingSetLastDay,
                                           args.path, args.classifier, args.team)
    myPrediction.makePrediction()
    programExecutionEnd= time.time()
    print(f'Total execution time: {programExecutionEnd- programExecutionStart}')

#showArgs()
#runPrediction()
analytics= Analytics()
analytics.countAttemptsPerClass('All', 1, 26)
prediction= Voronoi_Match_Prediction(args.trainingSetFirstDay, args.trainingSetLastDay, args.testingSetFirstDay,
                 args.testingSetLastDay, args.path, args.classifier, args.team)
prediction.makePrediction()
prediction.showConfusionMatrix()
