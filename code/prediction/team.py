class Team:
    '''
    A class for the representation of every team of the championship.
    For every team performance statistics are stored which contribute
    to the prediction of future matches of that team.
    Statistics are separated in home and away categories to discern
    the team's performance when playing home and away matches 
    '''
    def __init__(self, name, code):
        self.name= name
        self.code= code
        self.goals= {'home':0, 'away':0}
        self.goalsAgainst= {'home':0, 'away':0}
        self.attempts= {'home':{1:0, 2:0, 3:0, 4:0}, 'away':{1:0, 2:0, 3:0, 4:0}}
        self.minGoal= 0
        self.maxGoal= 0
        self.matches= {'home': {'win':0, 'draw':0, 'loss':0}, 'away': {'win':0, 'draw':0, 'loss':0}}    
        self.results= {}
        self.predictions= {}
    

    def update(self, data):
        '''
        Updates the statistics of the team with the new statistics provided
        '''
        self.goals['home']+= data['goalsHome']
        self.goals['away']+= data['goalsAway']
        self.goalsAgainst['home']+= data['goalsAgainstHome']
        self.goalsAgainst['away']+= data['goalsAgainstAway']
        self.attempts['home'][1]+= data['attemptsHome1']
        self.attempts['home'][2]+= data['attemptsHome2']
        self.attempts['home'][3]+= data['attemptsHome3']
        self.attempts['home'][4]+= data['attemptsHome4']
        self.attempts['away'][1]+= data['attemptsAway1']
        self.attempts['away'][2]+= data['attemptsAway2']
        self.attempts['away'][3]+= data['attemptsAway3']
        self.attempts['away'][4]+= data['attemptsAway4']
        if self.minGoal > data['goals']:
            self.minGoal= data['goals']
        if self.maxGoal < data['goals']:
            self.maxGoal= data['goals']
        self.matches['home']['win']+= data['homeWin']
        self.matches['home']['draw']+= data['homeDraw']
        self.matches['home']['loss']+= data['homeLoss']
        self.matches['away']['win']+= data['awayWin']
        self.matches['away']['draw']+= data['awayDraw']
        self.matches['away']['loss']+= data['awayLoss']
        if data['prediction'] == True:                                          # If the match belongs NOT to training set
                                                                                # and the statistics provided were randomly
                                                                                # generated, based on the team's performance
                                                                                # on previous matches 
            self.predictions.update({data['match']:data['score']})              # Update the predictins dictionary were 
                                                                                # fictitious results are stored
        else:                                                                   # If the match belongs to training set
                                                                                # and the statistics provided are real
            self.results.update({data['match']:data['score']})                  # Update the results dictionary were real
                                                                                # results are stored


    def printTeamStats(self):
        '''
        Prints the statistics of the team
        '''
        print('\n')
        print(self.name)
        print('-'*len(self.name))
        print('Home Statistics:')
        print(f"Wins: {self.matches['home']['win']}\t",
        f"Draws: {self.matches['home']['draw']}\t",
        f"Losses: {self.matches['home']['loss']}")
        print(f"Goals:    Scored: {self.goals['home']}\t\t"
              f"Conceded: {self.goalsAgainst['home']}")
        print(f"Attempts: 1: {self.attempts['home'][1]}      "
              f"2: {self.attempts['home'][2]}      "
              f"3: {self.attempts['home'][3]}      "
              f"4: {self.attempts['home'][4]}      "
              f"5: {self.goals['home']}")
        print('\nAway Statistics:')
        print(f"Wins: {self.matches['away']['win']}    ",
              f"Draws: {self.matches['away']['draw']}   ",
              f"Losses: {self.matches['away']['loss']}")
        print(f"Goals:  Scored: {self.goals['away']}     ",
              f"Conceded:  {self.goalsAgainst['away']}")
        print(f"Attempts: 1: {self.attempts['away'][1]}      ",
              f"2: {self.attempts['away'][2]}     ",
              f"3: {self.attempts['away'][3]}     ",
              f"4: {self.attempts['away'][4]}     ",
              f"5: {self.goals['away']}")
        print('\nMatches Played:')
        for item in self.results.items():
            print(item)
        print('\n')
