from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


WINDOW_SIZE = 10
test_server_urls = {
    "p": "http://20.244.56.144/test/primes",
    "f": "http://20.244.56.144/test/fibo",
    "e": "http://20.244.56.144/test/even",
    "r": "http://20.244.56.144/test/rand"
}


window = []
access_token = None

def fetch_numbers(numberid):
    # Fetch numbers from the test server with authorization header
    url = test_server_urls.get(numberid)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=0.5)
        if response.status_code == 200:
            return response.json().get("numbers", [])

        elif response.json().get("message") == "Invalid authorization token":
            # Handle expired token
            refresh_access_token()  
            # Retry the request with the new token
            #print(access_token)
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.get(url, headers=headers, timeout=0.5)
            if response.status_code == 200:
                return response.json().get("numbers", [])
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return []

def refresh_access_token():
    global access_token
    # Prepare data for POST request
    auth_data = {
        "companyName": "Solvers",
        "clientID": "ed48dd31-c7ee-4be6-a676-446254415d0d",
        "clientSecret": "NeAKzIbMmkmitrXD",
        "ownerName": "Srishti",
        "ownerEmail": "2003srishti1@gmail.com",
        "rollNo": "se21ucse219"
    }
    auth_url = "http://20.244.56.144/test/auth"

    try:
        #print("trying")
        response = requests.post(auth_url, json=auth_data)
        if response.status_code in [200, 201]:
            #print("done")
            access_token = response.json().get("access_token")
        else:
            print(f"Failed to refresh access token. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Token refresh request failed: {e}")

@app.route("/numbers/<numberid>", methods=["GET"])
def get_numbers(numberid):
    if numberid not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400
    
    # Ensure access token is available
    if access_token is None:
        refresh_access_token()

    # Fetch numbers from the third-party server
    fetched_numbers = fetch_numbers(numberid)
    
    # Ensure unique numbers and update window
    prev_state = list(window)
    for number in fetched_numbers:
        if number not in window:
            if len(window) >= WINDOW_SIZE:
                window.pop(0)
            window.append(number)
    curr_state = list(window)
    
    # Calculate average
    if len(window) > 0:
        avg = sum(window) / len(window)
    else:
        avg = 0.0

    # Prepare response
    response = {
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": fetched_numbers,
        "avg": round(avg, 2)
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, threaded=False)
