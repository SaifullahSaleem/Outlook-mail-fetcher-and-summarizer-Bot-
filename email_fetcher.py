import msal
import requests
from datetime import datetime, timedelta
from config import CLIENT_ID, AUTHORITY

# Scopes required for delegated access
SCOPES = ["User.Read", "Mail.Read"]

def get_user_token():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to create device flow")
    print(flow["message"]) 
    result = app.acquire_token_by_device_flow(flow)
    return result["access_token"]

def fetch_emails_for_day(date_str):
    access_token = get_user_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    date_start = datetime.strptime(date_str, "%Y-%m-%d")
    date_end = date_start + timedelta(days=1)

    endpoint = "https://graph.microsoft.com/v1.0/me/messages"
    params = {
        "$top": 5  # Fetch the latest 5 emails (adjust as needed)
    }

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    messages = response.json().get("value", [])

    emails = []
    for msg in messages:
        received_str = msg.get("receivedDateTime")
        if received_str:
            received_date = datetime.fromisoformat(received_str.rstrip("Z"))
            if date_start <= received_date < date_end:
                emails.append({
                    "subject": msg.get("subject", ""),
                    "sender": msg.get("from", {}).get("emailAddress", {}).get("address", ""),
                    "body": msg.get("body", {}).get("content", "")
                })
    return emails
