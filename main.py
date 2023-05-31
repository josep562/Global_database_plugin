import json
import requests
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.post("/search")
async def search():
    request_data = await quart.request.get_json(force=True)
    name = request_data.get("name")
    country_code = request_data.get("country_code")
    page = request_data.get("page", 1)
    
    payload = {
        "name": name,
        "country_code": country_code,
        "page": page
    }
    
    headers = {
        "Authorization": "Token YOUR_AUTH_TOKEN"  # Replace with your actual authorization token
    }
    
    response = requests.post("https://api.globaldatabase.com/v2/overview", json=payload, headers=headers)
    
    if response.status_code == 200:
        search_results = response.json().get("data")
        return quart.Response(response=json.dumps(search_results), status=200)
    else:
        return quart.Response(response='Search failed', status=response.status_code)

@app.get("/company/<string:id>")
async def get_company(id):
    headers = {
        "Authorization": "Token YOUR_AUTH_TOKEN"  # Replace with your actual authorization token
    }
    
    response = requests.get(f"https://api.globaldatabase.com/v2/companies/{id}", headers=headers)
    
    if response.status_code == 200:
        company_data = response.json()
        return quart.Response(response=json.dumps(company_data), status=200)
    else:
        return quart.Response(response='Company not found', status=response.status_code)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
