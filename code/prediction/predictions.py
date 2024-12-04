import copy
import os
import numpy as np
from utilities import detectOpponents, detectAttackingTeam
from pngConvert import png2ndarray
from skops.io import load
import team
import random

def probablePrediction(predictedLabel, choice):
    '''Returns the  first second or third most common real label
       when the model predicts the predicted label

       Arguments:
        - predictedLabel: integer in space [1,5], the label that the 
                          model predicted for a specific attempt
        - choice: integer in space [1,3], 
                  1 --> first most usuall real label, when predictedLabel is predicted 
                  2 --> second most usuall real label, when predictedLabel is predicted
                  3 --> third most usuall real label, when predictedLabel is predicted

       E.g. If it has been observed that when the model predicts 
            an attempt to belong to class 5 then 
            50% of the times it is indeed a 5
            25% of the times it is a 3
            10% of the times is a 4
            9% of the times is a 1
            6% of the times is a 2

            then 
            
            probablePrediction(5, 0) returns 5
            probablePrediction(5, 1) returns 3
            probablePrediction(5, 2) returns 4
        
        Returns:
            A label, an integer in space [1,5]  
            '''
    # Lists with the most common real labels per predicted label
    # These lists came from statistical analysis of the training set
    one=   [1, 2, 3]
    two=   [3, 2, 5]
    three= [5, 2, 4]
    four=  [4, 3, 1]
    five=  [5, 3, 4]
    match predictedLabel:
        case 1:
            return one[choice-1] 
        case 2:
            return two[choice-1] 
        case 3:
            return three[choice-1]
        case 4:
            return four[choice-1]
        case 5:
            return five[choice-1]
        

def predictOutcome(model, homeTeamAttempts, awayTeamAttempts, strategy):
    '''
    Predicts the outcome of a match (home team wins, draw or away team wins)
    based on the Voronoi diagrams of the match attempts
    
    Arguments: 
    - model: a trained machine learning model that will predict the winner
    - homeTeamAttempts: 2-dimension array with the attempts of the home team
    - awayTeamAttempts: 2-dimension array with the attempts of the away team
    
    Note: An attempt is a list/1-d array that contains the pixel values of a 
          png image depicting the voronoi diagram of the attempt

    - strategy: The algorithm that determines the outcome of the match by
               handling the classification of the attempts into categories.
               Two strategies available:
               1) absolute: the prediction for each attempt is absolutely 
                            trusted (consequently team with the most attempts
                            classified as 5 wins)
               2) probabilistic: the three(out of five) most possible categories
                                 participate equally in the prediction of the
                                 winner. The winner is determined by the
                                 3^number_of_attempts combinations that come of
                                 this procedure
               3) cumulative: the predictions of each team are added and the 
                              winner is determined by the sums

    Returns (depending on the chosen strategy):
        - winner (string)
        - goal_diff (integer)
        - probabilities (list of 3 values) [homeTeamWinProbability, drawProbability, awayTeamWinProbability]
        - score (list of 2 values) [homeTeamGoals, awayTeamGoals]
        
        Note: Whatever is not required by the dislay argument is being returned with the None value
     
    '''
    yPredHome= model.predict(homeTeamAttempts)                                  # Predict the attempts of the home team
    yPredAway= model.predict(awayTeamAttempts)                                  # Predict the attempts of the away team

    print(yPredHome)
    print(yPredAway)
    # Predict the winner according to the requested strategy
    match strategy:
        case 'absolute':
            # Count how many goals each team scored
            homeGoals= 0
            awayGoals= 0
            for attempt in yPredHome:
                if attempt == 5:
                    homeGoals+= 1
            for attempt in yPredAway:
                if attempt == 5:
                    awayGoals+= 1
            # Return values
            # Winner
            if homeGoals > awayGoals:
                winner= 'home'
            elif homeGoals == awayGoals:
                winner= 'draw'
            else:
                winner= 'away'
            # Goal difference
            goalDiff= abs(homeGoals-awayGoals)
            # Score
            score= [homeGoals, awayGoals]
            return winner, goalDiff, score
        
        case 'probabilistic':
            predictionsCombinations= [[]]
            numOfHomeAttempts= len(yPredHome)
            numOfAwayAttempts= len(yPredAway)
            allAttempts= list(yPredHome) + list(yPredAway)
            numOfAllAttempts= len(allAttempts)
            # Create all the combinations
            for attempt in allAttempts:
                numOfCombinations= len(predictionsCombinations)                 # Find the number of combinations so far
                firstCopy= copy.deepcopy(predictionsCombinations)
                secondCopy= copy.deepcopy(predictionsCombinations)
                predictionsCombinations= (predictionsCombinations               # Triple the existing combinations
                                          + firstCopy
                                          + secondCopy)
                # Update the combinations with the new attempt's possible predictions
                for i in range(0, numOfCombinations * 3):
                    if i < numOfCombinations:
                        (predictionsCombinations[i].
                        append(probablePrediction(attempt,1)))                  # Append the first probable value to the
                                                                                # first 1/3 of the combinations 
                    elif i < numOfCombinations * 2:
                        (predictionsCombinations[i].
                         append(probablePrediction(attempt,2)))                 # Append the second probable value to the
                                                                                # second 1/3 of the combinations 
                    else:
                        (predictionsCombinations[i].
                         append(probablePrediction(attempt,3)))                 # Append the third probable value to the
                                                                                # last 1/3 of the combinations
            # Divide the combinations in three parts and define counters for the
            # winners in every part
            partSize= len(predictionsCombinations)/3
            homeWin= [0, 0, 0]
            draw= [0, 0, 0]
            awayWin= [0, 0, 0]
            # Find the winner in each combination of every part and update the counters
            i=1
            for combination in predictionsCombinations:
                homeGoals= 0
                awayGoals= 0
                for j in range(0, numOfHomeAttempts):                           # Examine the home team's attempts
                    if combination[j] == 5:
                        homeGoals+= 1                                           # Count the goals of home team in this combination
                for j in range(numOfHomeAttempts, numOfAllAttempts):            # Examine the away team's attempts
                    if combination[j] == 5:
                        awayGoals+= 1                                           # Count the goals of away team in this combination
                if i <= partSize:                                               # If the combination belongs to the first 1/3
                                                                                # of the combinations
                    if homeGoals > awayGoals:
                        homeWin[0] += 1
                    elif homeGoals == awayGoals:
                        draw[0] += 1
                    else:
                        awayWin[0] += 1
                    i += 1
                elif i <= 2 * partSize:                                         # If the combination belongs to the second 1/3
                                                                                # of the combinations
                    if homeGoals > awayGoals:
                        homeWin[1] += 1
                    elif homeGoals == awayGoals:
                        draw[1] += 1
                    else:
                        awayWin[1] += 1
                    i += 1
                else:                                                           # If the combination belongs to the last 1/3
                                                                                # of the combinations
                    if homeGoals > awayGoals:
                        homeWin[2] += 1
                    elif homeGoals == awayGoals:
                        draw[2] += 1
                    else:
                        awayWin[2] += 1        
            # Find the probabilities of the final winner by compositing the counters
            # of the three parts together with some weights
            finalHomeWin= 0.0
            finalDraw= 0.0
            finalAwayWin= 0.0
            weights= [1.33, 1.00, 0,66]                                         # The counters of the first part of combinations
                                                                                # are more significant, because the values of the
                                                                                # predictions of the first combinations are more 
                                                                                # possible to be the real categories than those
                                                                                # of the last part 
            for i in range (0, 3):                                              
                finalHomeWin+= weights[i] * homeWin[i]
                finalDraw+= weights[i] * draw[i]
                finalAwayWin+= weights[i] * awayWin[i]
            finalHomeWin= int(finalHomeWin)
            finalDraw= int(finalDraw)
            finalAwayWin= int(finalAwayWin)
            # Find and return the winner
            if finalHomeWin > finalAwayWin and finalHomeWin > finalDraw :
                winner= 'home'
            elif finalAwayWin > finalHomeWin and finalAwayWin > finalDraw:
                winner= 'away'
            else:
                winner= 'draw'
            total= finalHomeWin + finalDraw + finalAwayWin
            probabilities= [finalHomeWin/total, finalDraw/total, finalAwayWin/total]
            return winner, probabilities      
        
        case 'cumulative':
            MINIMUM_DIFFERENCE= 3
            WIDE_GOAL_DIFFERENCE= 21
            MEDIUM_GOAL_DIFFERENCE= 14
            # Sum the predictions of each team
            sumHome= sum(yPredHome)
            sumAway= sum(yPredAway)
            print(f"Sum home= {sumHome}\nSum away= {sumAway}\n")
            # Return values
            # Winner
            winner= 'draw'
            goalDiff= '0-1 Goals'
            if abs(sumHome-sumAway) > MINIMUM_DIFFERENCE:
                if sumHome > sumAway:
                    winner= 'home'
                else:
                    winner= 'away'
            # Goal difference
            if abs(sumHome-sumAway) > WIDE_GOAL_DIFFERENCE:
                goalDiff= "2-4 Goals"
            elif abs(sumHome-sumAway) > MEDIUM_GOAL_DIFFERENCE:
                goalDiff= '1-2 Goals'
            else: 
                goalDiff= '0-1 Goals'
            return winner, goalDiff
        
IMAGE_HEIGHT= 160
IMAGE_WIDTH= 240
FEATURES_AFTER_IMAGE_SIZE_REDUCTION= ((int(0.9*IMAGE_HEIGHT)-int(0.15*IMAGE_HEIGHT))       # Image height
                                      * (int(0.82*IMAGE_WIDTH)-int(0.2*IMAGE_WIDTH))      # Image width
                                      * 3)                                                 # RGB 3 values per pixel


def predictMatch (pathToMatchDirectory, model, strategy):
    ''' Predicts the winner of a match based on the Voronoi 
        diagrams of the attempts made by both of the teams
        
        Arguments:
            - pathToMatchDirectory: The path to the directory were the Voronoi 
                                    diagrams of both teams are stored (type: string)
            - model: A machine learning algorithmic model that has been trained to
                     classify attempts according to their significance (poor attempt,
                     mediocore, good, save, goal) (type: string, path to the saved model
                     file)
            - strategy: Determines the way the predictions of the model will be used 
                        to predict the matches outcome (string ['absolute', 'probabilistic',
                        'cumulative'])
        Returns:
            Depending on the chosen strategy:
                For 'absolute': 
                    - winner: The unique team code that is predicted to win the match
                              (type: string of 3 characters     E.g.'oly')
                              In case of draw, the string 'draw' (type: string)
                    - goalDiff: The goal difference between the goals of the two teams
                                (type: int)
                    - score: A list of 2 values [homeTeamGoals, awayTeamGoals]
                For 'probabilistic':
                    - winner: As in 'absolute' case
                    - probabilities: A list of 3 values [probability of home team win, 
                                     probability of draw, probability of away team win]
                For 'cumulative':
                    - winner: As in 'absolute' case
                    - goalDiff: As in 'absolute' case
            '''
    attemptsClassifier= load(model, trusted=None)                               # Load the trained machine learning model
    homeTeam, awayTeam= detectOpponents(pathToMatchDirectory)                   # Detect the home team and the awat team
    homeTeamAttempts= np.empty([1, FEATURES_AFTER_IMAGE_SIZE_REDUCTION], dtype=int)                                          # Create an empty numpy array where the home
                                                                                # team's attempts will be stored
    awayTeamAttempts= np.empty([1,FEATURES_AFTER_IMAGE_SIZE_REDUCTION], dtype=int)                                          # Create an empty numpy array where the away 
                                                                                # team's attempts will be stored
    # Fill each team's attempt array with the team's attempts
    for attempt in os.listdir(pathToMatchDirectory):                            # For every attempt of the match
        attacker= detectAttackingTeam(attempt)                                  # Find which team made the attempt
        if attacker == homeTeam:                                                # If the attempt belongs to the home team
            homeTeamAttempts= np.vstack((homeTeamAttempts, png2ndarray          # Append the attempt's (png image) pixel
                      (pathToMatchDirectory + '/' + attempt))                   # values into the home team's attempts array
                      )                                                                                          
        else:                                                                   # If the attempt belongs to the home team            
            awayTeamAttempts= np.vstack((awayTeamAttempts, png2ndarray          # Append the attempt's (png image) pixel
                      (pathToMatchDirectory + '/' + attempt))                   # values into the home team's attempts array  
                      )       
    homeTeamAttempts= np.delete(homeTeamAttempts, [0], axis=0)
    awayTeamAttempts= np.delete(awayTeamAttempts, [0], axis=0)        
    # Predict the match outcome
    match strategy:
        case 'absolute':
            winner, goalDiff, score= predictOutcome(attemptsClassifier, 
                                                    homeTeamAttempts, 
                                                    awayTeamAttempts, 
                                                    strategy)
            return winner, goalDiff, score
        case 'probabilistic':
            winner, probabilities= predictOutcome(attemptsClassifier, 
                                                    homeTeamAttempts, 
                                                    awayTeamAttempts, 
                                                    strategy)
            return winner, probabilities
        case 'cumulative':
            winner, goalDiff= predictOutcome(attemptsClassifier, 
                                                    homeTeamAttempts, 
                                                    awayTeamAttempts, 
                                                    strategy)
            return winner, goalDiff


def predictNewOutcome(homeTeamAttempts, awayTeamAttempts, strategy):
    '''
    Predicts the outcome of a match (home team wins, draw or away team wins)
    
    Arguments: 
    - model: a trained machine learning model that will predict the winner
    - homeTeamAttempts: 2-dimension array with the attempts of the home team
    - awayTeamAttempts: 2-dimension array with the attempts of the away team
    
    Note: An attempt is a list/1-d array that contains the pixel values of a 
          png image depicting the voronoi diagram of the attempt

    - strategy: The algorithm that determines the outcome of the match by
               handling the classification of the attempts into categories.
               Two strategies available:
               1) absolute: the prediction for each attempt is absolutely 
                            trusted (consequently team with the most attempts
                            classified as 5 wins)
               2) probabilistic: the three(out of five) most possible categories
                                 participate equally in the prediction of the
                                 winner. The winner is determined by the
                                 3^number_of_attempts combinations that come of
                                 this procedure
               3) cumulative: the predictions of each team are added and the 
                              winner is determined by the sums

    Returns (depending on the chosen strategy):
        - winner (string)
        - goal_diff (integer)
        - probabilities (list of 3 values) [homeTeamWinProbability, drawProbability, awayTeamWinProbability]
        - score (list of 2 values) [homeTeamGoals, awayTeamGoals]
        
        Note: Whatever is not required by the dislay argument is being returned with the None value
     
    '''
    print(homeTeamAttempts)
    print(awayTeamAttempts)
    # Predict the winner according to the requested strategy
    match strategy:
        case 'absolute':
            # Count how many goals each team scored
            homeGoals= 0
            awayGoals= 0
            for attempt in homeTeamAttempts:
                if attempt == 5:
                    homeGoals+= 1
            for attempt in awayTeamAttempts:
                if attempt == 5:
                    awayGoals+= 1
            # Return values
            # Winner
            if homeGoals > awayGoals:
                winner= 'home'
            elif homeGoals == awayGoals:
                winner= 'draw'
            else:
                winner= 'away'
            # Goal difference
            goalDiff= abs(homeGoals-awayGoals)
            # Score
            score= [homeGoals, awayGoals]
            return winner, goalDiff, score
        
        case 'probabilistic':
            predictionsCombinations= [[]]
            numOfHomeAttempts= len(homeTeamAttempts)
            numOfAwayAttempts= len(awayTeamAttempts)
            allAttempts= list(homeTeamAttempts) + list(awayTeamAttempts)
            numOfAllAttempts= len(allAttempts)
            # Create all the combinations
            for attempt in allAttempts:
                numOfCombinations= len(predictionsCombinations)                 # Find the number of combinations so far
                firstCopy= copy.deepcopy(predictionsCombinations)
                secondCopy= copy.deepcopy(predictionsCombinations)
                predictionsCombinations= (predictionsCombinations               # Triple the existing combinations
                                          + firstCopy
                                          + secondCopy)
                # Update the combinations with the new attempt's possible predictions
                for i in range(0, numOfCombinations * 3):
                    if i < numOfCombinations:
                        (predictionsCombinations[i].
                        append(probablePrediction(attempt,1)))                  # Append the first probable value to the
                                                                                # first 1/3 of the combinations 
                    elif i < numOfCombinations * 2:
                        (predictionsCombinations[i].
                         append(probablePrediction(attempt,2)))                 # Append the second probable value to the
                                                                                # second 1/3 of the combinations 
                    else:
                        (predictionsCombinations[i].
                         append(probablePrediction(attempt,3)))                 # Append the third probable value to the
                                                                                # last 1/3 of the combinations
            # Divide the combinations in three parts and define counters for the
            # winners in every part
            partSize= len(predictionsCombinations)/3
            homeWin= [0, 0, 0]
            draw= [0, 0, 0]
            awayWin= [0, 0, 0]
            # Find the winner in each combination of every part and update the counters
            i=1
            for combination in predictionsCombinations:
                homeGoals= 0
                awayGoals= 0
                for j in range(0, numOfHomeAttempts):                           # Examine the home team's attempts
                    if combination[j] == 5:
                        homeGoals+= 1                                           # Count the goals of home team in this combination
                for j in range(numOfHomeAttempts, numOfAllAttempts):            # Examine the away team's attempts
                    if combination[j] == 5:
                        awayGoals+= 1                                           # Count the goals of away team in this combination
                if i <= partSize:                                               # If the combination belongs to the first 1/3
                                                                                # of the combinations
                    if homeGoals > awayGoals:
                        homeWin[0] += 1
                    elif homeGoals == awayGoals:
                        draw[0] += 1
                    else:
                        awayWin[0] += 1
                    i += 1
                elif i <= 2 * partSize:                                         # If the combination belongs to the second 1/3
                                                                                # of the combinations
                    if homeGoals > awayGoals:
                        homeWin[1] += 1
                    elif homeGoals == awayGoals:
                        draw[1] += 1
                    else:
                        awayWin[1] += 1
                    i += 1
                else:                                                           # If the combination belongs to the last 1/3
                                                                                # of the combinations
                    if homeGoals > awayGoals:
                        homeWin[2] += 1
                    elif homeGoals == awayGoals:
                        draw[2] += 1
                    else:
                        awayWin[2] += 1        
            # Find the probabilities of the final winner by compositing the counters
            # of the three parts together with some weights
            finalHomeWin= 0.0
            finalDraw= 0.0
            finalAwayWin= 0.0
            weights= [1.33, 1.00, 0,66]                                         # The counters of the first part of combinations
                                                                                # are more significant, because the values of the
                                                                                # predictions of the first combinations are more 
                                                                                # possible to be the real categories than those
                                                                                # of the last part 
            for i in range (0, 3):                                              
                finalHomeWin+= weights[i] * homeWin[i]
                finalDraw+= weights[i] * draw[i]
                finalAwayWin+= weights[i] * awayWin[i]
            finalHomeWin= int(finalHomeWin)
            finalDraw= int(finalDraw)
            finalAwayWin= int(finalAwayWin)
            # Find and return the winner
            if finalHomeWin > finalAwayWin and finalHomeWin > finalDraw :
                winner= 'home'
            elif finalAwayWin > finalHomeWin and finalAwayWin > finalDraw:
                winner= 'away'
            else:
                winner= 'draw'
            total= finalHomeWin + finalDraw + finalAwayWin
            probabilities= [finalHomeWin/total, finalDraw/total, finalAwayWin/total]
            return winner, probabilities      
        
        case 'cumulative':
            MINIMUM_DIFFERENCE= 3
            WIDE_GOAL_DIFFERENCE= 20
            MEDIUM_GOAL_DIFFERENCE= 10
            # Sum the predictions of each team
            sumHome= sum(homeTeamAttempts)
            sumAway= sum(awayTeamAttempts)
            print(f"Sum home= {sumHome}\nSum away= {sumAway}\n")
            # Return values
            # Winner
            winner= 'draw'
            goalDiff= '0-1 Goals'
            if abs(sumHome-sumAway) > MINIMUM_DIFFERENCE:
                if sumHome > sumAway:
                    winner= 'home'
                else:
                    winner= 'away'
            # Goal difference
            if abs(sumHome-sumAway) > WIDE_GOAL_DIFFERENCE:
                goalDiff= "2-4 Goals"
            elif abs(sumHome-sumAway) > MEDIUM_GOAL_DIFFERENCE:
                goalDiff= '1-2 Goals'
            else: 
                goalDiff= '0-1 Goals'
            return winner, goalDiff


def predictNewMatch(homeTeam, awayTeam):
    '''
    Predicts the outcome of a match using a random distribution based on 
    the performance of the teams during the first half of the season

    Arguments:
        -homeTeam: the code name of the home team 
        -awayTeam: the code name of the away team

    Returns (depending on the chosen strategy):
        - winner (string)
        - goal_diff (integer)
        - probabilities (list of 3 values) [homeTeamWinProbability, drawProbability, awayTeamWinProbability]
        - score (list of 2 values) [homeTeamGoals, awayTeamGoals]
    '''
    numOfHomeMatches= (homeTeam.matches['home']['win'] 
                   + homeTeam.matches['home']['draw']
                   + homeTeam.matches['home']['loss']) 
    numOfAwayMatches= (awayTeam.matches['away']['win'] 
                   + awayTeam.matches['away']['draw']
                   + awayTeam.matches['away']['loss'])
    # Calculate the mean number of attempts per class for the two teams
    # and the mean number of goals scored per match
    meanNumOfAttemptsPerClassH= []
    meanNumOfAttemptsPerClassA= []
    for category in range (1,5):
        meanNumOfAttemptsPerClassH.append(homeTeam.attempts['home'][category]
                                          / numOfHomeMatches)
        meanNumOfAttemptsPerClassA.append(awayTeam.attempts['away'][category]
                                          / numOfAwayMatches)
    meanGoalsH= homeTeam.goals['home']/numOfHomeMatches
    meanGoalsA= awayTeam.goals['away']/numOfAwayMatches
    # Randomly generate the attempts and goals of each team 
    homeAttempts=[]
    awayAttempts=[]
    for category in range (1,5):
        homeAttempts.append(int(max(random.normalvariate(meanNumOfAttemptsPerClassH[category-1], 1.0), 0.0))) 
        awayAttempts.append(int(max(random.normalvariate(meanNumOfAttemptsPerClassA[category-1], 1.0), 0.0)))
    goalsH= int(max(random.normalvariate(meanGoalsH, 1.0), 0.0))
    goalsA= int(max(random.normalvariate(meanGoalsA, 1.0), 0.0))
    homeAttempts.append(goalsH)
    awayAttempts.append(goalsA)
    homeTeamAttempts= []
    awayTeamAttempts= []
    for category in range (0,5):
        for i in range (0, homeAttempts[category]):
            homeTeamAttempts.append(category+1)
        for i in range (0, awayAttempts[category]):
            awayTeamAttempts.append(category+1)
    # winner, goalDiff, score= predictNewOutcome(homeTeamAttempts, awayTeamAttempts, 'absolute')
    # print(f'Winner: {winner}\nGoal Difference: {goalDiff}\nScore: {score}\n')
    
    
    winner, probabilities= predictNewOutcome(homeTeamAttempts, awayTeamAttempts, 'probabilistic')
    print(f'Winner: {winner}\nProbabilities: {probabilities}\n')

    # winner, goalDiff= predictNewOutcome(homeTeamAttempts, awayTeamAttempts, 'cumulative')
    # print(f'Winner: {winner}\nProbabilities: {goalDiff}\n')
    return homeTeam.code+'-'+awayTeam.code+': '+winner

