from fastapi import FastAPI, HTTPException, Request

import requests
import time
from datetime import datetime
import pytz

app = FastAPI()


app_name = "leadership-initiatives"
api_token = "4e8f92dd-7bde-49e5-8cb3-2c48d29d7ba8"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/vnd.heroku+json; version=3",
    "Content-Type": "application/json"
}

while True:
    # Define the endpoint URL
    url = "http://leadership-initiatives-0c372bea22f2.herokuapp.com/status"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Assuming your response is a JSON with a "content" key
        status_content = response.json()["content"]
        
    except requests.RequestException as e:
        print(headers)
        # To restart all dynos
        response = requests.delete(f"https://api.heroku.com/apps/{app_name}/dynos", headers=headers)
        # Convert the current UTC time to EST
        est = pytz.timezone('US/Eastern')
        current_time = datetime.now(pytz.utc).astimezone(est).strftime('%m/%d/%y %I:%M%p EST')
        # Check if the request was successful
        if response.status_code == 202:
            print(f"[{current_time}]: Dynos are restarting...")
        else:
            print("Error:", response.content)
        time.sleep(45)

    time.sleep(15)
