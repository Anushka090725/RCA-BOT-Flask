import requests

# print('gemini_query.py')

def query_gemini(prompt, api_key):
    """
    Query the Gemini API with a structured RCA prompt.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    params = {"key": api_key}

    response = requests.post(url, headers=headers, params=params, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Gemini API Error: {response.status_code}, {response.text}")

    return response.json()
