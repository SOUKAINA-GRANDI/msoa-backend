import os, httpx
from dataclasses import dataclass
from fastapi import HTTPException

ORDERS_URL = os.getenv("ORDERS_URL", "http://localhost:8084")

@dataclass
class OrderView:
    id: str
    total: float
    status: str

class OrdersClient:
    def __init__(self, base_url: str = ORDERS_URL, timeout: float = 5.0):
        self.base_url, self.timeout = base_url, timeout

    def get_order(self, order_id: str):
        try:
            r = httpx.get(f"{self.base_url}/api/orders/{order_id}", timeout=self.timeout)
        except httpx.RequestError:
            raise HTTPException(503, "Orders service unavailable.")
        if r.status_code == 404:
            return None
        if r.status_code >= 400:
            raise HTTPException(503, "Orders service error.")
        d = r.json()
        return OrderView(id=d["id"], total=float(d["total"]), status=d["status"])

    def mark_paid(self, order_id: str):
        try:
            r = httpx.patch(f"{self.base_url}/api/orders/{order_id}/status",
                            json={"status": "PAID"}, timeout=self.timeout)
            r.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError):
            raise HTTPException(503, "Could not update order status.")