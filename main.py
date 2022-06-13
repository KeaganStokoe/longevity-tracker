import os
import requests
from datetime import datetime, timedelta
from pprint import pprint

current_week_start_date = (datetime.today() - timedelta(7)).strftime("%Y-%m-%d")
current_week_end_date = datetime.today().strftime("%Y-%m-%d")
previous_week_start_date = (datetime.today() - timedelta(14)).strftime("%Y-%m-%d")
previous_week_end_date = (datetime.today() - timedelta(7)).strftime("%Y-%m-%d")

vital_api_key = os.environ['vital-api-key']
user_id = '16643d73-456e-4f5a-af85-b6639bfa9eed'
headers = {'Accept': 'application/json', 'x-vital-api-key': vital_api_key}
current_week_params = {'start_date': current_week_start_date, 'end_date': current_week_end_date}
previous_week_params = {'start_date': previous_week_start_date, 'end_date': previous_week_end_date}


def getWorkoutData(time_params = current_week_params):
    """
  Function to request all workout data. By deafult, it will request data from the past 7 days. 
  To request data for the 7 days before that, pass 'previous_week_params' as an argument.
  """
    api_url: str = f'https://api.sandbox.tryvital.io/v2/summary/workouts/{user_id}'
    r = requests.get(api_url, headers=headers, params=time_params)
    return r

def getSleepData():
    """
  Function to request all sleep data in the past 7 days. 
  """
    api_url: str = f'https://api.sandbox.tryvital.io/v2/summary/sleep/{user_id}'
    r = requests.get(api_url, headers=headers, params=current_week_params)
    return r


def getRunningData(workoutData):
    """
  Function that returns running data given a list of workouts. 
  """
    res = workoutData
    runningData = []
    for item in res.json()["workouts"]:
        if item['sport']['name'] == "Running":
            runningData.append(item)
    return runningData

def getWalkingData():
    """
  Function that returns data about runs completed in the past 7 days.  
  """
    res = getWorkoutData()
    walkingData = []
    for item in res.json()["workouts"]:
        if item['sport']['name'] == "Walking":
            walkingData.append(item)
    return walkingData

def getStrengthTrainingData():
    """
  Function that returns data about runs completed in the past 7 days.  
  """
    res = getWorkoutData()
    strengthTrainingData = []
    for item in res.json()["workouts"]:
        if item['sport']['name'] == "Strength Training":
            strengthTrainingData.append(item)
    return strengthTrainingData

# Calculate percentage increase or decrease in training volume for the week  
def calculatePercentageDifferenceTrainingVolume():
# 1. get data for current and previous week
  currentWeekData = getWorkoutData()
  currentRunData = getRunningData(currentWeekData)
  
# 2. calculate difference between current week and previous week
  totalCurrentRunningDistance = 0
  for item in currentRunData:
      totalCurrentRunningDistance += item['distance']
  
  previousWeekData = getWorkoutData(previous_week_params)
  previousRunData = getRunningData(previousWeekData)
  totalPreviousRunningDistance = 0
  for item in previousRunData:
      totalPreviousRunningDistance += item['distance']
    
# 3. calculate percentage difference
  def percentage_difference(a, b):
      return ((a - b) / ((a + b) / 2)) * 100
  
  trainingVolumeDifference = percentage_difference(totalCurrentRunningDistance,totalPreviousRunningDistance)
  return trainingVolumeDifference

def createSummary():
    workoutData = getWorkoutData()
    runningData = getRunningData(workoutData)
    walkingData = getWalkingData()
    strengthData = getStrengthTrainingData()
    sleepData = getSleepData()
    runningVolumeDifference = calculatePercentageDifferenceTrainingVolume()

    totalRuns = len(runningData)
    totalRunningDistance = 0
    totalRunningTime = 0
    caloriesBurntRunning = 0
    for item in runningData:
        totalRunningDistance += item['distance']
        totalRunningTime += item['moving_time']
        caloriesBurntRunning += item['calories']

    totalWalks = len(walkingData)
    totalWalkingDistance = 0
    totalWalkingTime = 0
    caloriesBurntWalking = 0
    for item in walkingData:
        totalWalkingDistance += item['distance']
        totalWalkingTime += item['moving_time']
        caloriesBurntWalking += item['calories']

    totalStrengthSessions = len(strengthData)
    totalStrengthTime = 0
    caloriesBurntStrength = 0
    for item in strengthData:
        totalStrengthTime += item['moving_time']
        caloriesBurntStrength += item['calories']

    totalSleep = 0
    totalDeepSleep = 0
    for item in sleepData.json()['sleep']:
        totalSleep += item['total']
        totalDeepSleep += item['deep']

    summary = f"""
    Total runs: {totalRuns}<br>
    Total distance: {totalRunningDistance/1000:.2f} km<br>
    vs Previous week: {runningVolumeDifference:.2f}%<br>
    Time on the road: {totalRunningTime/60/60:.2f} hours<br>
    Calories: {caloriesBurntRunning}
    <hr>
    Total walks: {totalWalks}<br>
    Total distance: {totalWalkingDistance/1000:.2f} km<br>
    Time on the road: {totalWalkingTime/60/60:.2f} hours<br>
    Calories:{caloriesBurntWalking}
    <hr>
    Total strength sessions: {totalStrengthSessions}<br>
    Time in the gym: {totalStrengthTime/60/60:.2f} hours<br>
    Calories: {caloriesBurntStrength}
    <br>
    <hr>
    <br>
    Average sleep: {totalSleep/60/60/7:.2f} hours <br>
    Average deep sleep: {totalDeepSleep/60/60/7:.2f} hours <br>
  """
    pprint(summary)
    return summary

createSummary()