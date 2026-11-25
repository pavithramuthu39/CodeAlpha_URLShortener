# CodeAlpha URL Shortener

A Flask application that creates short links and redirects them to their original URLs.

## Run locally

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy to Render

The `render.yaml` Blueprint creates a web service and PostgreSQL database. Push the project to GitHub, then in Render choose **New + → Blueprint**, connect this repository, and approve the generated services. Render will build and deploy the app automatically.

The free web service may spin down while idle, and free PostgreSQL databases have provider-defined usage and retention limits. Review Render's current plan terms before relying on this deployment for persistent data.