# API

## Instalación
### Crear y activar un entorno virtual
```bash
python3 -m venv ambiente
```
```bash
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```
### Instalar dependencias
```bash
pip install -r requirements.txt
```
## Levantar servidor
Usando shell script
```bash
bash shells/main.sh
```
## Pruebas automatizadas
```bash
bash shells/run_tests.sh
```
## Endpoints disponibles

### GET /healthz
Prueba rápida del servidor para verificar que está funcionando.

**Ejemplo de uso con `curl`:**
```bash
curl http://localhost:8000/healthz
```
Respuesta esperada:
```bash
{"status":"ok"}
```
### POST /orders/ingest
Envía un JSON con pedidos:
**Ejemplo de uso con `curl`:**
```bash
curl -X POST "http://localhost:8000/orders/ingest" \
-H "Content-Type: application/json" \
-d '{
  "orders": [
    {
      "id": "o1",
      "customer_id": 123,
      "created_at": "2025-08-20T10:00:00Z",
      "currency": "EUR",
      "items": [
        { "sku": "A", "quantity": 2, "unit_price": 10.0 }
      ]
    },
    {
      "id": "o2",
      "customer_id": 2,
      "created_at": "2025-08-20T11:00:00Z",
      "currency": "USD",
      "items": [
        { "sku": "B", "quantity": 1, "unit_price": 30.0 },
        { "sku": "C", "quantity": 3, "unit_price": 5.0 }
      ]
    }
  ]
}'
```
Respuesta esperada:
```bash
{
    "processed_orders": [
        {
            "id": "o1",
            "total_eur": 20.0,
            "flags": []
        },
        {
            "id": "o2",
            "total_eur": 40.5,
            "flags": []
        }
    ],
    "summary": {
        "orders_received": 2,
        "orders_valid": 2,
        "orders_invalid": 0,
        "duplicates_dropped": 0,
        "total_revenue_eur": 60.5,
        "avg_ticket_eur": 30.25,
        "top_skus_by_quantity": [
            {
                "sku": "C",
                "quantity": 3
            },
            {
                "sku": "A",
                "quantity": 2
            },
            {
                "sku": "B",
                "quantity": 1
            }
        ]
    },
    "duplicates": []
}
```

