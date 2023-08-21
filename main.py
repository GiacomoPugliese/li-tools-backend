from fastapi import FastAPI
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse
import secrets
from fastapi import FastAPI, HTTPException

app = FastAPI()

tokens = {}  # A simple in-memory storage for tokens

##### HEROKU LOGIN INFO ####
### Username: tabithapugliese@yahoo.com
### Password: Octane3245!

@app.get("/auth")
def auth(user_id: str):
    # Create the Flow instance
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive'],
        redirect_uri='https://leadership-initiatives-0c372bea22f2.herokuapp.com/callback' 
    )

    # Set the state for CSRF protection
    flow.state = secrets.token_hex(16)

    # Get the authorization URL for the consent screen
    authorization_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    # Save the user_id and Flow instance for later
    tokens[0] = {"user_id": user_id, "flow": flow}
    print(f"Auth endpoint: State is {flow.state}")
    print(f"Auth endpoint: Tokens are {tokens}")
    # Return the authorization URL in the response
    return {"authorization_url": authorization_url}


@app.get("/callback")
async def callback(code: str, state: str):
    try:
        print(f"Callback endpoint: State is {state}")
        print(f"Callback endpoint: Tokens are {tokens}")
        flow = tokens[0]["flow"]
        flow.fetch_token(code=code)

        credentials = flow.credentials
        tokens[0]["token"] = credentials.token
        tokens[0]["creds"] = credentials
        return "Authentication successful. Please close this window and click 'Finalize Google Authentication'"
    except Exception as e:
        # Raise an HTTPException with a 500 status code and a custom error message
        raise HTTPException(status_code=500, detail=f"Experiencing network issues, please refresh the page.")

@app.get("/token/{user_id}")
async def get_token(user_id: str):
    # Retrieve token using user_id
    return {"creds": tokens[0]["creds"]}
