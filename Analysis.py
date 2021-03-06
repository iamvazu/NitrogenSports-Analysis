# Nitrogen Sports Betting Analysis

# Format of NS Betslip ---------- list size 9
# Game
# Game Prediction
# Odds
# Risk BTC
# Winnings BTC
# Win/Lose
# Sport
# Subcategory
# Betslip ID

# Format of NS parlays ------- list size 8x + 5, 21, 29
# Individual Risk/Winnings 0.0
# 8 lines then start next bet (8 lines)...and etc
# Betslip ID
# Parlay Keyword
# Odds
# Risk BTC
# Winnings BTC

import requests

# Retrieve current Bitcoin spot price via Coinbase
PRICE_JSON = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
BTC = float(PRICE_JSON.json()['data']['amount'])


# Enter your bankroll size
bankroll = 0.0


def main():

    # get data in organized list
    betslips = getData()

    # Filter what you want
    #######################################

    getRecord("All", betslips)

    #######################################


def getRecord(betType, nitroList):

    wins = 0
    losses = 0
    pushes = 0
    betSize = 0.0
    netProfit = 0.0
    unitSize = .003
    units = 2

    if betType == "All":

        for nitro in nitroList:

            print(nitro)

            if (len(nitro) < 10):
                if nitro[5] == "win":
                    wins = wins + 1
                    betSize = betSize + float(nitro[3])
                    netProfit = netProfit + float(nitro[4])
                    units = units + (float(nitro[4])/unitSize)
                if nitro[5] == "lose":
                    losses = losses + 1
                    betSize = betSize + float(nitro[3])
                    netProfit = netProfit - float(nitro[3])
                    units = units - (float(nitro[3])/unitSize)
                if nitro[5] == "push":
                    pushes = pushes + 1
            else:
                if nitro[5] == "win" and nitro[13] == "win":
                    wins = wins + 1
                    betSize = betSize + float(nitro[len(nitro)-1].split(" ")[0])
                    netProfit = netProfit + float(nitro[len(nitro)-1].split(" ")[0])
                    units = units + (float(nitro[len(nitro)-1].split(" ")[0])/unitSize)
                else:
                    losses = losses + 1
                    betSize = betSize + float(nitro[len(nitro)-2].split(" ")[0])
                    netProfit = netProfit - float(nitro[len(nitro)-2].split(" ")[0])
                    units = units - (float(nitro[len(nitro)-2].split(" ")[0])/unitSize)


    elif (betType == "ML"):

        for nitro in nitroList:

            if "ML" in nitro[1]:
                 
                print(nitro)
                if nitro[5] == "win":
                    wins = wins + 1
                    betSize = betSize + float(nitro[3])
                    netProfit = netProfit + float(nitro[4])
                    units = units + (float(nitro[4])/unitSize)
                if nitro[5] == "lose":
                    losses = losses + 1
                    betSize = betSize + float(nitro[3])
                    netProfit = netProfit - float(nitro[3])
                    units = units - (float(nitro[3])/unitSize)
                if nitro[5] == "push":
                    pushes = pushes + 1

    elif (betType == "Spread"):

        for nitro in nitroList:

                if "+" in nitro[1] or "-" in nitro[1]: 
                     
                    print(nitro)
                    if nitro[5] == "win":
                        wins = wins + 1
                        betSize = betSize + float(nitro[3])
                        netProfit = netProfit + float(nitro[4])
                        units = units + (float(nitro[4])/unitSize)
                    if nitro[5] == "lose":
                        losses = losses + 1
                        betSize = betSize + float(nitro[3])
                        netProfit = netProfit - float(nitro[3])
                        units = units - (float(nitro[3])/unitSize)
                    if nitro[5] == "push":
                        pushes = pushes + 1

    elif (betType == "OverUnder"):

        for nitro in nitroList:
            
            if " over " in nitro[1] or " under " in nitro[1] or " Over " in nitro[1] or " Under " in nitro[1]:
                     
                print(nitro)
                if nitro[5] == "win":
                    wins = wins + 1
                    betSize = betSize + float(nitro[3])
                    netProfit = netProfit + float(nitro[4])
                    units = units + (float(nitro[4])/unitSize)
                if nitro[5] == "lose":
                    losses = losses + 1
                    betSize = betSize + float(nitro[3])
                    netProfit = netProfit - float(nitro[3])
                    units = units - (float(nitro[3])/unitSize)
                if nitro[5] == "push":
                    pushes = pushes + 1

    posOrNeg = ""
    if (units > 0):
        posOrNeg = "+"

    unitString = format(units, '.2f')
    percent = format(float(wins)*100/(float(wins)+float(losses)), '.2f')

    print(' ')
    print(str(wins) + "-" + str(losses) + "-" + str(pushes))
    print(percent + "% Success Rate")
    print("Total Profit : " + str(netProfit) + " BTC")
    print("Total Profit : $" + str(netProfit * BTC))
    print("ROI : " + str((((netProfit + betSize) - betSize)/betSize) * 100) + "%")
    print(posOrNeg + unitString + " units")
    print("Bitcoin : $" + str(BTC))
    print("Bankroll : $" + str(bankroll * BTC))
    print(' ')


# Function to perform calculations
def calculate(betslips):
    return []


# Function to open file of data and parse it into a list of betslips
def getData():

    f = open('Wagers.txt', 'r')

    betslips = []
    temp = []

    for line in f:
        line = line.strip('\n')

        # break to start after model following, continue for prior
        if "PHASE" in line:
            break

        # Parse out Blank lines and Parlays
        if len(line) is not 0:
            temp.append(line)
        else:
            betslips.append(temp)
            temp = []

    # to remove empty lists (spaces)
    bets = [x for x in betslips if x]
    return bets
 
if __name__ == '__main__':
    main()
