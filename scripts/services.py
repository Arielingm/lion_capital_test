from typing import List, Dict
from futils import convert_to_eur, Order, OrdersResponse, ProcessedOrder, Summary, OrdersRequest

def process_orders(orders: List[Order]) -> OrdersResponse:
    orders_received = len(orders)
    processed = []
    duplicates = []
    invalid_count = 0

    # Deduplicar por id (mantener más reciente)
    unique_orders = {}
    for order in orders:
        if order.id not in unique_orders or order.created_at > unique_orders[order.id].created_at:
            unique_orders[order.id] = order
    duplicates_dropped = orders_received - len(unique_orders)
    duplicates = [o.id for o in orders if o.id not in unique_orders]

    total_revenue = 0
    valid_orders = 0
    sku_counter: Dict[str, int] = {}

    for order in unique_orders.values():
        flags = []
        valid = True

        # Validación negativa
        for item in order.items:
            if item.quantity <= 0 or item.unit_price <= 0:
                flags.append("NEGATIVE_VALUE")
                valid = False
                break

        if valid:
            total = sum(item.quantity * item.unit_price for item in order.items)
            total_eur = convert_to_eur(total, order.currency)
            total_eur = round(total_eur, 2)
            total_revenue += total_eur
            valid_orders += 1

            # Contar SKUs
            for item in order.items:
                sku_counter[item.sku] = sku_counter.get(item.sku, 0) + item.quantity

            processed.append(ProcessedOrder(id=order.id, total_eur=total_eur, flags=flags))
        else:
            invalid_count += 1
            processed.append(ProcessedOrder(id=order.id, total_eur=0, flags=flags))

    avg_ticket = round(total_revenue / valid_orders, 2) if valid_orders > 0 else 0

    top_skus = sorted(sku_counter.items(), key=lambda x: x[1], reverse=True)[:5]
    top_skus = [{"sku": k, "quantity": v} for k, v in top_skus]

    summary = Summary(
        orders_received=orders_received,
        orders_valid=valid_orders,
        orders_invalid=invalid_count,
        duplicates_dropped=duplicates_dropped,
        total_revenue_eur=round(total_revenue, 2),
        avg_ticket_eur=avg_ticket,
        top_skus_by_quantity=top_skus
    )

    return OrdersResponse(processed_orders=processed, summary=summary, duplicates=duplicates)
