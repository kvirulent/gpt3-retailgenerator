import openai
import json
import os
from time import sleep

runtype = int(input("SELECT TYPE: OFFLINE (1) OR ONLINE (2)"))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def waitForInput():
    print("Press enter to return")
    input()
if runtype == 2:
    openai.api_key = input("INPUT OPENAI API KEY: ")
else:
    openai.api_key = None
def AIRequest(prompt): #Requests to OPENAI API

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response

def getDataset(): #Runs requests to OPENAI API and cleans data

    if runtype == 2:

        queries = [
            "Random unique retail store name",
            "1 Random product name and price to be sold in a retail store",
            "1 Random product name and price to be sold in a retail store",
            "1 Random product name and price to be sold in a retail store",
            "1 Random product name and price to be sold in a retail store",
            "1 Random product name and price to be sold in a retail store",
            "1 Random product name and price to be sold in a retail store",
            "Random retail store operating hours"
        ]

        data = []

        for i in queries:
            data.append(AIRequest(i))

    elif runtype == 1:
        data = json.load(open('./fallbackData.json'))

    totalDatasetTokenCost = 0
    requestStatistics = []
    EndData = {
        "name":"",
        "products":[],
        "hours":""
    }

    for c in [0,1,2,3,4,5,6,7]:
        if c == 0:
            requestStatistics.append([
                data[c]['id'],
                data[c]['usage']['total_tokens'],
                data[c]['choices'][0]['finish_reason'],
                data[c]['created']
            ])
            totalDatasetTokenCost += data[c]['usage']['total_tokens']
            EndData['name'] = data[c]['choices'][0]['text']
        elif c >= 1 and c <= 6:
            requestStatistics.append([
                data[c]['id'],
                data[c]['usage']['total_tokens'],
                data[c]['choices'][0]['finish_reason'],
                data[c]['created']
            ])
            totalDatasetTokenCost += data[c]['usage']['total_tokens']
            EndData['products'].append(data[c]['choices'][0]['text'])
        elif c == 7:
            requestStatistics.append([
                data[c]['id'],
                data[c]['usage']['total_tokens'],
                data[c]['choices'][0]['finish_reason'],
                data[c]['created']
            ])
            totalDatasetTokenCost += data[c]['usage']['total_tokens']
            EndData['hours'] = data[c]['choices'][0]['text']

    return {
        "totalDatasetTokenCost":totalDatasetTokenCost,
        "requestStatistics":requestStatistics,
        "data":EndData
    }

def menuBranch1(data):
    print("Products:")
    for i in data['data']['products']:
        print(i)
    waitForInput()

def menuBranch2(data):
    print("Hours:")
    print(data['data']['hours'])
    waitForInput()

def menuBranch3(data):
    print("DEBUG INFO:")
    print(f"Total request cost (In Tokens): {data['totalDatasetTokenCost']}")
    print("REQUEST ID | TOKEN COST | STOP REASON | GENERATION TIME")
    for i in data['requestStatistics']:
        print(i)
    waitForInput()

def menuBranch4():
    print("PROJECT INFO:")
    print("placeholder")
    waitForInput()

def menuBranch5():
    exit("Exitted!")

def menu(data):

    while True:
        clear()
        print(f"-- {data['data']['name']} --")
        print("1 } Products")
        print("2 } Hours")
        print("3 } Debug info")
        print("4 } Project info")
        print("5 } Exit ")

        try:
            uin = int(input("Select an option from the list (1-5)\n"))
        except ValueError:
            clear()
            for i in [5,4,3,2,1]:
                print(f"Enter numbers only! Returning in {i}")
                sleep(1)
                clear()
            continue

        if uin > 5 or uin < 1:
            clear()
            for i in [5,4,3,2,1]:
                print(f"Out of range, select 1-5 only! Returning in {i}")
                sleep(1)
                clear()
            continue

        opTable = {
            "1":lambda : menuBranch1(data),
            "2":lambda : menuBranch2(data),
            "3":lambda : menuBranch3(data),
            "4":lambda : menuBranch4(),
            "5":lambda : menuBranch5()
        }


        opTable[str(uin)]()

menu(getDataset())