import os
import requests
from datetime import datetime, timedelta
from pprint import pprint
# import json

    
date_today = datetime.today()
date_last_week = datetime.today() - timedelta(7)
start_date = date_last_week.strftime("%Y-%m-%d")
end_date = date_today.strftime("%Y-%m-%d")

vital_api_key = os.environ['vital-api-key']
user_id = '16643d73-456e-4f5a-af85-b6639bfa9eed'
headers = {'Accept': 'application/json', 'x-vital-api-key': vital_api_key}
params = {'start_date': start_date, 'end_date': end_date}

def getWorkoutData():
  """
  Function to request all workout data in the past 7 days. 
  """
  api_url: str = f'https://api.sandbox.tryvital.io/v2/summary/workouts/{user_id}'
  r = requests.get(api_url, headers=headers, params=params)
  # res = json.dumps(r.json(), indent=2)
  # print(res)
  return r

def getRunningData():
  """
  Function that returns data about runs completed in the past 7 days.  
  """
  res = getWorkoutData()
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

def createSummary():
  runningData = getRunningData()
  walkingData = getWalkingData()
  strengthData = getStrengthTrainingData()

  totalRuns = len(runningData)
  totalRunningDistance = 0
  for item in runningData:
    totalRunningDistance += item['distance']
    
  summary = f"""
    Total runs: {totalRuns}
    Total distance: {totalRunningDistance/1000}
  """

  return summary
    

createSummary()
  
