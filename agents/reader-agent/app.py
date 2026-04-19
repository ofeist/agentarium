from fastapi import FastAPI

app = FastAPI(title="reader-agent")


@app.get("/health")
def health():
    return {"status": "ok"}
