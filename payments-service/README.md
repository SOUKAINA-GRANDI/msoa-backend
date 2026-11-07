# Payment Service (port 8085)

Run: `uvicorn app.main:app --port 8085 --reload`  |  Docs: http://localhost:8085/docs

| Method | URL | Description |
|---|---|---|
| GET | /api/payments | list payments |
| GET | /api/payments/order/{orderId} | payment of an order (404 if none) |
| POST | /api/payments | body `{orderId, method}` |
| GET | /health | health check |

Test methods: `TEST_DECLINE` (402), `TEST_TIMEOUT` (503). Amount > 50000 is declined.
Env: `ORDERS_URL` (default http://localhost:8084).
