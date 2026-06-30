import requests
import pandas as pd
# connection to Oracle Apex REST API

BASE_URL = "https://apex.oracle.com/ords/project_finshare/finshare"

def fetch(endpoint):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(f"{BASE_URL}/{endpoint}/", timeout=10, headers=headers)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data["items"])
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return pd.DataFrame()

def get_users():
    return fetch("users")

def get_balances():
    return fetch("balances")

def get_loans():
    return fetch("loans")

def get_groups():
    return fetch("groups")