# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

HTML_FORM = """
<html>
  <body>
    <h2>Test Deployment Trigger</h2>
    <form method="post">
      <label>GitHub Repo URL:</label><br>
      <input type="text" name="repo_url" value="alexwambu/GBTNetwork-network-update-render" size="60"><br><br>
      <label>Domain:</label><br>
      <input type="text" name="domain" value="GBTNetwork"><br><br>
      <label>Logo Hash:</label><br>
      <input type="text" name="logo" value="fded6dc4-a90e-4089-877a-bb8a1cc15bc8.png"><br><br>
      <button type="submit">Trigger Deployment</button>
    </form>
    <br>{response}
  </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def form():
    return HTML_FORM.format(response="")

@app.post("/", response_class=HTMLResponse)
async def trigger_deployment(request: Request):
    form = await request.form()
    payload = {
        "repo_url": form["repo_url"],
        "domain": form["domain"],
        "logo": form["logo"]
    }

    try:
        r = requests.post("https://gbt-advance-9-1.onrender.com/deploy", json=payload)
        response_text = f"<h3>Response from backend:</h3><pre>{r.json()}</pre>"
    except Exception as e:
        response_text = f"<p style='color:red'>Error contacting backend: {e}</p>"

    return HTML_FORM.format(response=response_text)
