import os
import team
import utilities

def detectAndSaveTeams(pathToMatchdaysDirectory):
    '''
    Scans the first matchdays directories to detect the teams which participate
    in the championship and stores them in a list
    '''
    MATCHDAYS_TO_SCAN= 3                                                        # Scan the three first matchdays
                                                                                # Hopefully all the teams that 
                                                                                # participate in the championship 
                                                                                # will appear at least once
    teams= []                                                                   # The teams detected so far
    matchdays= os.listdir(pathToMatchdaysDirectory)                             # List the matchdays found in the 
                                                                                # provided directory
    matchdaysScaned= 0                                                          # The number of matchdays that have 
                                                                                # been examined so far
    for matchday in matchdays:                                                  # For every matchday in the list
        matches= os.listdir(pathToMatchdaysDirectory + '/' + matchday)          # Make a list with the matches played
                                                                                # that day
        for match in matches:                                                   # For every match in the list
            homeTeam= match[0:3]                                                # Detect the home team
            awayTeam= match[4:]                                                 # Detect the away team
            if homeTeam not in teams:                                           # If the home team has not been 
                                                                                # detected yet
                teams.append(homeTeam)                                          # Add the home team in the teams' list
            if awayTeam not in teams:                                           # If the away team has not been
                                                                                # detected yet
                teams.append(awayTeam)                                          # Add the away team in the teams' list
        matchdaysScaned+= 1                                                     # One more matchday has been scaned
        if matchdaysScaned > MATCHDAYS_TO_SCAN:                                 # If the predefined number of matchdays
                                                                                # to be examined has been reached
            break                                                               # Stop scanning new matchdays
    return teams                                                                # Return a list of the teams that were
                                                                                # detected

def makeRanking(teamsList):
    '''
    Creates a ranking with the teams that are in the provided list

    Arguments:
        - teamsList: the list of teams returned by the detectAndSaveTeams function

    Returns:
        A dictionary where the keys are the teams' names
        and the values are their collected points in the
        championship
    '''
    ranking= {}
    for team in teamsList:
        ranking.update({team:0}) 
    return ranking


def showRanking(ranking):
    '''
    Prints the ranking (a dictionary) it receives as an argument in descending order

    Arguments:
        - ranking: A dictionary with keys the teams participating in the championship
                   and values the points they have collected  
    Returns:
        Nothing
    '''
    items= ranking.items()
    sortedItems= sorted(items, key= lambda pair: pair[1], reverse= True)
    i= 1 
    for item in sortedItems:
        print(f'{i}. {item[0]}\t\t{item[1]}')
        i+= 1


def updateRanking(ranking, teamPointsDict):
    '''
    Updates the ranking according to the dictionary given

    Arguments:
        - ranking: The ranking that will be updated (a dictionary)
        - teamPointsDict: a dictionary with keys the teams whose points will change
                          and values the points that the teams gain or lose 
    Returns:
        - the updated ranking   
    '''
    teams= teamPointsDict.keys()
    for team in teams:
        if team not in ranking:
            print(f'Team {team} was not found in the given ranking')
        else:
            ranking[team]+= teamPointsDict[team]
    return ranking


def extractMatchStats(pathToMatchDirectory):
    '''
    Collects and returns statistics for the two 
    teams which participate to a specific match

    Arguments:
        - pathToMatchDirectory: the path to the directory which 
          contains the voronoi diagrams of the match
    Returns:
        - homeDict: A dictionary with statistics for the home team
        - awayDict: A dictionary with statistics for the away team 
    '''
    home= {'1':0, '2':0, '3':0, '4':0, '5':0}
    away= {'1':0, '2':0, '3':0, '4':0, '5':0}
    homeTeam, awayTeam= utilities.detectOpponents(pathToMatchDirectory)
    attempts= os.listdir(pathToMatchDirectory)
    for attempt in attempts:
        attackingTeam= attempt[10:13]
        category= attempt[0]
        if attackingTeam == homeTeam:
            match category:
                case '1':
                    home['1']+= 1
                case '2':
                    home['2']+= 1
                case '3':
                    home['3']+= 1
                case '4':
                    home['4']+= 1
                case '5':
                    home['5']+= 1
        else: 
            match category:
                case '1':
                    away['1']+= 1
                case '2':
                    away['2']+= 1
                case '3':
                    away['3']+= 1
                case '4':
                    away['4']+= 1
                case '5':
                    away['5']+= 1
    homeWin=homeDraw=homeLoss= 0
    awayWin=awayDraw=awayLoss= 0
    if home['5'] > away['5']:
        homeWin= awayLoss= 1
    elif home['5'] == away ['5']:
        homeDraw= awayDraw= 1
    else:
        homeLoss= awayWin= 1
    score= [home['5'], away['5']]
    homeDict= {'goalsHome': home['5'], 
        'goalsAway': 0, 
        'goalsAgainstHome': away['5'],
        'goalsAgainstAway': 0, 
        'attemptsHome1': home['1'], 
        'attemptsHome2': home['2'], 
        'attemptsHome3': home['3'],
        'attemptsHome4': home['4'], 
        'attemptsAway1': 0,
        'attemptsAway2': 0, 
        'attemptsAway3': 0, 
        'attemptsAway4': 0, 
        'goals': home['5'], 
        'homeWin':homeWin, 
        'homeDraw': homeDraw,
        'homeLoss': homeLoss, 
        'awayWin':0, 
        'awayDraw':0, 
        'awayLoss':0,
        'match':homeTeam + '-' + awayTeam, 
        'score':score,
        'prediction':False}
    awayDict= {'goalsHome': 0, 
        'goalsAway': away['5'], 
        'goalsAgainstHome': 0,
        'goalsAgainstAway': home['5'], 
        'attemptsHome1': 0, 
        'attemptsHome2': 0, 
        'attemptsHome3': 0,
        'attemptsHome4': 0, 
        'attemptsAway1': away['1'],
        'attemptsAway2': away['2'], 
        'attemptsAway3': away['3'], 
        'attemptsAway4': away['4'], 
        'goals': away['5'], 
        'homeWin':0, 
        'homeDraw': 0, 
        'homeLoss': 0, 
        'awayWin':awayWin, 
        'awayDraw': awayDraw, 
        'awayLoss':awayLoss, 
        'match':homeTeam + '-' + awayTeam, 
        'score':score,
        'prediction':False}
    return homeDict, awayDict
        

def extractStats(pathToMatchdaysDirectory, teams, startingDay, endingDay):
    '''
    Collects statistics for all teams that will be used to predict the outcome
    of 'future' matches without voronoi diagrams, based on the performance of
    each team in a specific range of matchdays

    Arguments:
        - pathToMatchdaysDirectory: the path to the directory where all the
                                    matchdays are stored
        - teams: a dictionary which contains a team class object for every 
                 team of the championship 
        - startingDay: the first day of data collection
        - endingDay: the last day of data collection

    Returns:
        Nothing
    '''
    matchdays= os.listdir(pathToMatchdaysDirectory)
    for matchday in matchdays:                                                  # For every matchday
        if int(matchday) > int(endingDay) or int(matchday) < int(startingDay):  # If the matchday is out of the 
                                                                                # specified range ignore it
            continue
        pathToMatchday= pathToMatchdaysDirectory + '/' + matchday
        matches= os.listdir(pathToMatchday)
        for match in matches:                                                   # For every match played tht day
            pathToMatch= pathToMatchday + '/' + match
            homeTeam= match[0:3]                                                # Detect the home team
            awayTeam= match[4:]                                                 # Detect the away team
            homeTeamData, awayTeamData= extractMatchStats(pathToMatch)          # Collect the data of that match
            teams[homeTeam].update(homeTeamData)                                # Update the home team's statistics
            teams[awayTeam].update(awayTeamData)                                # Update the away team's statistics


def labelsSumDifferencePerGoalDifference(pathToMatchdaysDirectory, 
                                         startingDay, endingDay):
    '''
    Makes a table with the difference of the sums of the labels of the two opponents.
    Each row is for a match. Each column coressponds to a goal difference (0 goals,
    1 goal, ... , 5+ goals). This table will be helpful in the determination of the
    thresholds for the cumulative strategy for the prediction of completed or future
    matches (see predictions.py line 225) 
    '''
    matchdays= os.listdir(pathToMatchdaysDirectory)
    total= {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    count= {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    labelsDifefrences= []
    goalsDifferences= []
    for matchday in matchdays:                                                  # For every matchday
        if int(matchday) > int(endingDay) or int(matchday) < int(startingDay):  # If the matchday is out of the 
                                                                                # specified range ignore it
            continue
        pathToMatchday= pathToMatchdaysDirectory + '/' + matchday
        matches= os.listdir(pathToMatchday)
        print(f' match    0   1   2   3   4   5   6   7')
        print(f'---------------------------------------')
        for match in matches:                                                   # For every match played tht day
            pathToMatch= pathToMatchday + '/' + match
            homeTeam= match[0:3]                                                # Detect the home team
            awayTeam= match[4:]                                                 # Detect the away team
            homeTeamData, awayTeamData= extractMatchStats(pathToMatch)
            labelsSumHome= labelsSumAway= 0
            for i in range (1,5):
                labelsSumHome+= i * homeTeamData['attemptsHome'+ str(i)]
                labelsSumAway+= i * awayTeamData['attemptsAway'+ str(i)]
            labelsSumHome+= homeTeamData['goalsHome'] * 5
            labelsSumAway+= awayTeamData['goalsAway'] * 5
            goalsDifference= abs(homeTeamData['goalsHome'] - awayTeamData['goalsAway'])
            goalsDifferences.append(goalsDifference)
            labelsSumDifference= abs(labelsSumHome - labelsSumAway)
            labelsDifefrences.append(labelsSumDifference)
            total[goalsDifference]+= labelsSumDifference
            count[goalsDifference]+= 1
            print(f'{homeTeam}-{awayTeam}   {"    " * goalsDifference}{labelsSumDifference}')
    for i in range (0,8):
        if count[i] != 0:
            print(f'Mean: {i}: {total[i]/count[i]}')
        else:
            print(f'Mean {i}: Zero matches')
    thresholdDetermination(labelsDifefrences, goalsDifferences)


def thresholdDetermination(labelsDifferences, goalsDifferences):
    ''' 
    Exhaustive search of the threshold values that achieve the best performance
    for the cumulative strategy for the prediction of completed or future matches 
    '''
    maxPerformance= 0
    for minimumLabelDifference in range(3,10):
        for mediumLabelDifference in range(4,20):
            for wideLabelDifference in range(8,30):
                performance, stats= checkPerformance(labelsDifferences, goalsDifferences,
                                                     minimumLabelDifference,
                                                     mediumLabelDifference,
                                                     wideLabelDifference)
                if performance >= maxPerformance:
                    maxPerformance= performance
                    bestThresholds= [minimumLabelDifference, 
                                     mediumLabelDifference,
                                     wideLabelDifference]
    print(f'Best Parameters:\nminimum: {bestThresholds[0]}\n'
          f'medium: {bestThresholds[1]}\n'
          f'wide: {bestThresholds[2]}\n'
          f'Performance: {maxPerformance}\n'
          f'Statistics: {stats}')
    

def checkPerformance(labelsDifferences, goalsDifferences, minimumLabelDifference,
                     mediumLabelDifference, wideLabelDifference):
    '''
    Checks the performance of the cumulative strategy for the given data
    '''
    total= {'draw':0, 'minimum':0, 'medium':0, 'wide':0}
    correct= {'draw':0, 'minimum':0, 'medium':0, 'wide':0}
    for labelDifference, goalsDifference in zip(labelsDifferences, goalsDifferences):
        if goalsDifference == 0:
            total['draw']+= 1
            if labelDifference <= minimumLabelDifference:
                correct['draw']+= 1
        elif goalsDifference == 1:
            total['minimum']+= 1
            if labelDifference > minimumLabelDifference and labelDifference < wideLabelDifference:
                correct['minimum']+= 1
        if goalsDifference == 1 or goalsDifference == 2:
            total['medium']+= 1
            if labelDifference > minimumLabelDifference and labelDifference < wideLabelDifference:
                correct['medium']+= 1
        if goalsDifference >= 2:
            total['wide']+= 1
            if labelDifference > wideLabelDifference:
                correct['wide']+= 1
    performance= ((correct['draw']+correct['minimum']+correct['medium']+correct['wide'])
                / (total['draw']+total['minimum']+total['medium']+total['wide']))
    statistics= [correct['draw']/total['draw'], correct['minimum']/total['minimum'],
                 correct['medium']/total['medium'], correct['wide']/total['wide']]
    return performance, statistics


def attemptsPerClass (pathToMatchdaysDirectory, startingDay, endingDay):
    '''
    From the starting day till the ending day counts 
    how many attempts belong to every class
    '''
    counters= [0, 0, 0, 0, 0]
    matchdays= os.listdir(pathToMatchdaysDirectory)
    for matchday in matchdays:
        if int(matchday) > endingDay or int(matchday) < startingDay:
            continue
        pathToMatchday= pathToMatchdaysDirectory + '/' + matchday
        matches= os.listdir(pathToMatchday)
        for match in matches:
            pathToMatch= pathToMatchday + '/' + match
            attempts= os.listdir(pathToMatch)
            for attempt in attempts:
                counters[int(attempt[0])-1]+= 1
    print(f'From matchday {startingDay} till matchday {endingDay}:')
    print(f'1:  {counters[0]}')
    print(f'2:  {counters[1]}')
    print(f'3:  {counters[2]}')
    print(f'4:  {counters[3]}')
    print(f'5:  {counters[4]}')
