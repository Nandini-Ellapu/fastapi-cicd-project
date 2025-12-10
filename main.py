from fastapi import FastAPI

app = FastAPI(title="CI/CD Demo App")

@app.get("/")
def home():
    return {"message": "CI/CD Pipeline Working Successfully!"}
