# JAcob Auman
# This file takes the weight, and the current number of reps to calculate the max weight that can be curled for 1 rep

# WORKING!!!!

# Import Statements
import json


def readData():
    # Read the data.json file for the weight and reps
    with open('CoC_Curls\\BIG_COC\\data.json', 'r') as f:
        data = json.load(f)
    # Access specific values using their keys
    weight = data['weight']
    reps = data['reps']
    return weight, reps

def writeData(maxCurl):
    # Write the updated data to the file
    with open('CoC_Curls\\BIG_COC\\data.json', 'r') as f:
        data = json.load(f)
    data['maxCurl'] = maxCurl
    with open('CoC_Curls\\BIG_COC\\data.json', 'w') as f:
        json.dump(data, f)

def maxCurl_brzycki(weight, reps):
    # Calculate Max Curl using Brzycki Formula
    maxCurl = int(weight * (36 / (37 - reps)))
    return maxCurl

def main():
    weight, reps = readData()
    maxCurl = maxCurl_brzycki(weight, reps)
    print(f"Max Curl: {maxCurl} LBS")
    writeData(maxCurl)

if __name__ == "__main__":
    main()