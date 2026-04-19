from fastapi import FastAPI

app = FastAPI(title="math-agent")


@app.get("/health")
def health():
    return {"status": "ok"}
