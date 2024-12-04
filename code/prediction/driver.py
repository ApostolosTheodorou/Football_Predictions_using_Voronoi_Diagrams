'''
This file contains the code which run the whole prediction process for
both the completed and the future matches. The first section is for the
future matches and the second for the completed. Comment or uncomment
depending on the section you want to run and the strategy to be used.
'''

import teamsStats
import team
import predictions
import os

# FUTURE MATCHES PREDICTIONS
# The matches that will be predicted and their results
realResults= {'ast-pan: home', 'gia-the: away', 'lam-vol: draw', 'atr-oly: away', 
              'ofi-ari: draw', 'ion-aek: away', 'apo-pao: away', 'pan-atr: home',
              'oly-lam: home', 'the-ast: home', 'pao-gia: home', 'aek-ofi: away',
              'ari-ion: home', 'vol-apo: home', 'gia-ion: home', 'ast-ofi: home',
              'lam-aek: away', 'apo-oly: away', 'pao-ari: home', 'the-pan: home',
              'atr-vol: home', 'ofi-gia: draw', 'vol-pao: home', 'pan-lam: home',
              'ari-atr: home', 'ion-apo: home', 'oly-ast: home', 'aek-the: draw',
              'ast-vol: home', 'lam-ion: home', 'apo-ari: draw', 'the-ofi: home',
              'aek-pan: away', 'pao-oly: draw', 'gia-atr: draw', 'ofi-pan: away',
              'ion-pao: away', 'ari-lam: draw', 'atr-aek: away', 'vol-the: away',
              'oly-gia: home', 'ast-apo: home', 'pao-ast: away', 'lam-ofi: home',
              'ion-atr: home', 'pan-ari: away', 'gia-apo: home', 'aek-vol: away',
              'the-oly: draw', 'ast-gia: home', 'ofi-pao: home', 'oly-pan: home',
              'ari-aek: home', 'vol-ion: draw', 'apo-the: away', 'atr-lam: home',
              'ari-vol: away', 'pan-gia: away', 'aek-apo: home', 'ion-oly: away',
              'the-pao: home', 'atr-ofi: draw', 'lam-ast: away', 'apo-pan: draw',
              'ast-ion: away', 'ofi-vol: home', 'pao-lam: home', 'the-atr: home',
              'oly-aek: home', 'gia-ari: home', 'ion-ofi: draw', 'atr-ast: home',
              'pan-pao: home', 'lam-apo: away', 'vol-oly: away', 'aek-gia: home',
              'ari-the: draw', 'ast-ari: away', 'pan-vol: draw', 'the-ion: draw',
              'oly-ofi: home', 'pao-aek: home', 'apo-atr: away', 'gia-lam: home',
              'aek-ast: home', 'ari-oly: home', 'atr-pao: away', 'vol-gia: draw',
              'ion-pan: away', 'ofi-apo: home', 'lam-the: away'}
teamNames= {'aek':'aek', 'ion': 'ionikos', 'ari': 'aris', 'ofi':'ofi', 
        'oly':'olympiakos', 'atr':'atromitos', 'pan':'panaitolikos',
        'ast':'asteras tripolis', 'pao':'panathinaikos', 
        'apo':'apollon smyrnis', 'the':'paok', 'gia':'pas giannena',
        'vol':'volos', 'lam':'lamia'}

# The ranking of the first half of the season
ranking= {'aek':27, 'ion':14, 'ari':23, 'ofi':21, 'oly':35, 'atr':9, 'pan':11,
        'ast':14, 'pao':20, 'apo':7, 'the':22, 'gia':22, 'vol':14, 'lam':10}

# The points that each team has collected in the second half of the season 
collectedPoints= {'aek':0, 'ion':0, 'ari':0, 'ofi':0, 'oly':0, 'atr':0, 'pan':0,
        'ast':0, 'pao':0, 'apo':0, 'the':0, 'gia':0, 'vol':0, 'lam':0}

# A list that stores every team of the league as an object of the Team class
teams= {}

for name in teamNames.keys():
    teams.update({name:team.Team(teamNames[name], name)})
teamsStats.extractStats('./matchdays', teams, 1, 13)
for teeam in teams.values():
    teeam.printTeamStats()
totalCorrectPredictions= 0
totalNumOfMatches= 0
for matchday in range (14,27):
    print(f'-----------\nMatchday {matchday}\n-----------')
    correctPredictions= 0
    numOfMatches= 0
    matches= os.listdir('./matchdays/' + str(matchday))
    for match in matches:
        homeTeam= match[0:3]
        awayTeam= match[4:]
        print(f'Match:  {teams[homeTeam].name} - {teams[awayTeam].name}')
        result= predictions.predictNewMatch(teams[homeTeam], teams[awayTeam])
        if result[-4:] == 'home':
            collectedPoints[homeTeam]= 3
            collectedPoints[awayTeam]=0
        elif result[-4:] == 'draw':
            collectedPoints[homeTeam]= 1
            collectedPoints[awayTeam]=1
        elif result[-4:] == 'away':
            collectedPoints[homeTeam]= 0
            collectedPoints[awayTeam]=3
        numOfMatches+= 1
        if result in realResults:
            correctPredictions+= 1
    print('\nCorrect Predictions:')
    print(f'{correctPredictions}/{numOfMatches}\n\n\n')
    totalCorrectPredictions+= correctPredictions
    totalNumOfMatches+= numOfMatches
    ranking= teamsStats.updateRanking(ranking, collectedPoints)
print(f'Total Correct Predictions: {totalCorrectPredictions}/{totalNumOfMatches}\n'
      f'Accuracy: {round(totalCorrectPredictions/totalNumOfMatches,2)}%')
teamsStats.showRanking(ranking)


# # COMPLETED MATCHES PREDICTIONS

# for matchday in range (14,27): 
#     matches= os.listdir('./matchdays/' + str(matchday))
#     for match in matches:
#         homeTeam= match[0:3]
#         awayTeam= match[4:]
#         # if homeTeam != 'apo' and awayTeam!= 'apo':
#         #     continue
#         print(f'Match:  {homeTeam} - {awayTeam}')
#         pathToMatchDirectory= './matchdays/' + str(matchday) + '/' + match

#         # # ABSOLUTE
#         # winner, goalDifference, score= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_NOTWEIGHTED_240_160.skops', 
#         #                          'absolute')
#         # print(f'Prediction:\nWinner:{winner}\ngoal Difference:{goalDifference}\n'
#         #       f'score:{score}\n\n')
        
#         # PROBABILISTIC
#         winner, probabilities= predictions.predictMatch(pathToMatchDirectory, 
#                                  './savedModels/MLR_All_1_13_NOTWEIGHTED_240_160.skops', 
#                                  'probabilistic')
#         print(f'Prediction:\nWinner:{winner}\nProbabilities:{probabilities}\n\n')

#         # # CUMULATIVE
#         # winner, goalDifference= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_NOTWEIGHTED_240_160.skops', 
#         #                          'cumulative')
#         # print(f'Prediction:\nWinner:{winner}\nGoal Difference:{goalDifference}\n\n')


#         # # ABSOLUTE CENTRAL VS CUSTOMIZED
#         # winner, goalDifference, score= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_WEIGHTED_240_160.skops', 
#         #                          'absolute')
        
#         # winnerCustom, goalDifferenceCustom, scoreCustom= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_APO_NOTWEIGHTED_240_160.skops', 
#         #                          'absolute')
#         # print(f'Prediction:\nWinner:{winner}\ngoal Difference:{goalDifference}\n'
#         #       f'score:{score}\n')
#         # print(f'Prediction:\nWinner Custom:{winnerCustom}\ngoal Difference Custom:{goalDifferenceCustom}\n'
#         #       f'score Custom:{scoreCustom}\n\n')


#         # # CUMULATIVE CENTRAL VS CUSTOMIZED
#         # winner, goalDifference= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_WEIGHTED_240_160.skops', 
#         #                          'cumulative')
#         # print(f'Prediction:\nWinner:{winner}\nGoal Difference:{goalDifference}\n')

#         # winnerCustom, goalDifferenceCustom= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_APO_NOTWEIGHTED_240_160.skops', 
#         #                          'cumulative')
#         # print(f'Prediction:\nWinner Custom:{winnerCustom}\nGoal Difference Custom:{goalDifferenceCustom}\n\n')


#         # # PROBABILISTIC CENTRAL VS CUSTOMIZED
#         # winner, probabilities= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_WEIGHTED_240_160.skops', 
#         #                          'probabilistic')
#         # print(f'Prediction:\nWinner:{winner}\nProbabilities:{probabilities}\n')

#         # winnerCustom, probabilitiesCustom= predictions.predictMatch(pathToMatchDirectory, 
#         #                          './savedModels/MLR_All_1_13_APO_NOTWEIGHTED_240_160.skops', 
#         #                          'probabilistic')
#         # print(f'Prediction:\nWinner Custom:{winnerCustom}\nProbabilities Custom:{probabilitiesCustom}\n\n')