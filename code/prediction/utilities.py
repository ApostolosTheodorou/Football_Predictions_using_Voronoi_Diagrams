def stripFilesName(path):
    ''' Strips the file hierarchy tree and returns only the file's name
    
        Arguments:
            -path to the file

        E.g. Input: ./Desktop\\Matchdays\1\aek-ion\1-aek-ion-ion-25.png
             Output: 1-aek-ion-ion-25.png '''
    pos= -1
    char= path[pos]
    while char != "\\" and char != "/":
        pos-=1
        char=path[pos]
    pos+=1
    return path[pos:]


def detectOpponents(path):
    '''
    Receives a directory path and returns the home and away team names

    E.g. detectOpponents('C:/users/aUser/Desktop/aDirectory/aSubDirectory/matches/aek-pao')
         will return strings 'aek' and 'pao'
         
    '''
    pos= -1
    char= path[pos]
    while char != "\\" and char != "/":
        pos-=1
        char=path[pos]
    pos+=1
    return path[pos:pos+3], path[pos+4:]


def detectAttackingTeam (attempt):
    '''
    Receives a png files name and returns the team which made the attempt

    png file name has the following format: 
    'attemptClass-homeTeam-awayTeam-attackingTeam-minute.png'
    attemptClass: int [1-5]
    homeTeam, awayTeam, attackingTeam: 3 characters each
    minute: int [1-99]

    E.g. '3-oly-pan-oly-12.png'
    
    '''

    return attempt[10:13]