from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

def convert_to_eur(monto: float, currency: str) -> float:
    tasas = {"EUR": 1.0, "USD": 0.90, "GBP": 1.15}
    return monto * tasas.get(currency, 1.0)



class Item(BaseModel):
    sku: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

class Order(BaseModel):
    id: str
    customer_id: int
    created_at: datetime
    currency: str
    items: List[Item]

class OrdersRequest(BaseModel):
    orders: List[Order]

class ProcessedOrder(BaseModel):
    id: str
    total_eur: float
    flags: List[str]

class Summary(BaseModel):
    orders_received: int
    orders_valid: int
    orders_invalid: int
    duplicates_dropped: int
    total_revenue_eur: float
    avg_ticket_eur: float
    top_skus_by_quantity: List[dict]

class OrdersResponse(BaseModel):
    processed_orders: List[ProcessedOrder]
    summary: Summary
    duplicates: List[str]