import os
import requests
import json
from datetime import datetime, timedelta
    
date_today = datetime.today()
date_last_week = datetime.today() - timedelta(7)
start_date = date_last_week.strftime("%Y-%m-%d")
end_date = date_today.strftime("%Y-%m-%d")

vital_api_key = os.environ['vital-api-key']
user_id = '16643d73-456e-4f5a-af85-b6639bfa9eed'
headers = {'Accept': 'application/json', 'x-vital-api-key': vital_api_key}
params = {'start_date': start_date, 'end_date': end_date}

api_url = f'https://api.sandbox.tryvital.io/v2/summary/workouts/{user_id}'

r = requests.get(api_url, headers=headers, params=params)
res = json.dumps(r.json(), indent=2)
print(res)