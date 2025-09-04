from fastapi import FastAPI
from services import*

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/orders/ingest", response_model=OrdersResponse)
def ingest_orders(request: OrdersRequest):
    return process_orders(request.orders)