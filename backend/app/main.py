from fastapi import FastAPI

app = FastAPI(title="Learnify AI API")

@app.get("/health")
def health():
    return {"status": "ok"}
