from sklearn.metrics import *

def printMetrics(y_pred, y_true):
    labels= {0:'1', 1:'2', 2:'3', 3:'4', 4:'5'}

    # Built-in metrics by sklearn library
    accuracy= accuracy_score(y_true, y_pred)                                    # Accuracy
    mcc= matthews_corrcoef(y_true, y_pred)                                      # Mathew's Correlation Coefficient

    # Metrics per class
    classesCount= len(labels)                                                   # Calculate the number of classes
    # For every class create a list that stores the predictions' distribution for this class
    # Also create list that stores the count of the attempts in each class
    predDistribution= []                                                        # A list containing 5 sublists
                                                                                # Every sublist corresponds to a label(1-5) which is the real
                                                                                # category. The sublist stores the number of times
                                                                                # that this label was predicted as 1, 2, 3, 4 and 5
    attemptsPerClass= []                                                        # A list that stores how many attempts belong to each label
    predictionsPerClass= []                                                     # A list that stores how many attempts were predicted as 
                                                                                # 1, 2, 3, 4 and 5
    predActuallyAre= []                                                         # A list that stores what the attempts that were predicted
                                                                                # to belong to every label really are
    truePositive= []
    falsePositive= []
    falseNegative= []
    precision= []
    recall= []
    for i in range(0, classesCount):
        predDistribution.append([])
        predActuallyAre.append([])
        attemptsPerClass.append(0)
        predictionsPerClass.append(0)
        truePositive.append(0)
        falsePositive.append(0)
        falseNegative.append(0)
        for j in range(0, classesCount):
            predDistribution[i].append(0)
            predActuallyAre[i].append(0)               
    for i in range(0, len(y_pred)):                                             # Itterate through all predictions
        predDistribution[int(y_true[i])-1][int(y_pred[i])-1]+= 1                   # Update the counters for every class
        predActuallyAre[int(y_pred[i])-1][int(y_true[i])-1]+= 1
        attemptsPerClass[int(y_true[i])-1]+= 1
        predictionsPerClass[int(y_pred[i])-1]+= 1
    for i in range(0, classesCount):
        truePositive[i]= predActuallyAre[i][i]
        falsePositive[i]= predictionsPerClass[i]-truePositive[i]
        falseNegative[i]= attemptsPerClass[i]-truePositive[i]
    for i in range(0, classesCount):
        if predictionsPerClass[i] != 0:
            precision.append(round(float(truePositive[i])/float(predictionsPerClass[i]), 2))
        else: precision.append(0.0)
        if attemptsPerClass[i] != 0:
            recall.append(round(float(truePositive[i])/float(attemptsPerClass[i]), 2))
        else: recall.append(0.0)
    averagePrecision= round(sum(precision)/float(classesCount), 2)
    averageRecall= round(sum(recall)/float(classesCount), 2)
    
    # Print the results
    print('----------General Statistics----------')
    print(f'Accuracy: {round(accuracy, 3)}\nMathew\'s Correlation Coefficient: {round(mcc,2)}')
    print(f'Average Precision: {averagePrecision}%\nAverage Recall: {averageRecall}%\n')
    print('Distribution of the real labels:\t\tDistribution of predictions:')
    for i in range(0, classesCount):
        print(f'Class {labels.get(i)}:\t {attemptsPerClass[i]} attempts\t\t\t\t\tClass {labels.get(i)}:\t {predictionsPerClass[i]}\n')
    print('-------------------------------------Statistics per class--------------------------------------')
    for i in range(0, classesCount):
        print(f'\n-----------\nClass: {labels.get(i)}\n-----------')
        print(f'Total attempts: {attemptsPerClass[i]}\t\t\t\t\t\tTotal predictions: {predictionsPerClass[i]}')
        print('Were predicted as:\t\t\t\t\t\tWere actually:')
        for j in range(0, classesCount):
            if attemptsPerClass[i] != 0 and predictionsPerClass[i] != 0:
                print(f'{labels.get(j)}  --->  {predDistribution[i][j]}\t({round(predDistribution[i][j]/attemptsPerClass[i]*100, 2)}%)\
                 \t\t\t{labels.get(j)}  --->  {predActuallyAre[i][j]}\t({round(predActuallyAre[i][j]/predictionsPerClass[i]*100, 2)}%)')
            else: print(f'{labels.get(j)}  --->  {predDistribution[i][j]}\t({round(predDistribution[i][j]/attemptsPerClass[i]*100, 2)}%)')
        print(f'Precision: {round(precision[i]*100 ,3)}%\nRecall: {round(recall[i]*100, 3)}%')
    return averagePrecision, averageRecall, precision[4], recall[4]
