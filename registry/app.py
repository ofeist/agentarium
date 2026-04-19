from fastapi import FastAPI

app = FastAPI(title="agentarium-registry")


@app.get("/health")
def health():
    return {"status": "ok"}
