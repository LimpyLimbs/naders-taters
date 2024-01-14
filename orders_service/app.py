from datetime import datetime
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from starlette import status
from schemas import CreateOrderSchema, GetOrderSchema
from copy import deepcopy
import requests

app = FastAPI()

ORDERS = []

@app.get('/orders')
def get_orders():
    return ORDERS

@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def create_order(items: CreateOrderSchema):
    order = items.model_dump()
    order['order_id'] = uuid4()
    order['created'] = datetime.utcnow()
    ORDERS.append(order)
    order_copy = deepcopy(order)
    update_inventory(order_copy)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['order_id'] == order_id:
            return order
        raise HTTPException(status_code=404, detail=f'order {order_id} was not found')
    
@app.put('/orders/{order_id}', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def update_order(order_id: UUID, updated_order: GetOrderSchema):
    for index, order in enumerate(ORDERS):
        if order['order_id'] == order_id:
            ORDERS[index] = updated_order.model_dump()
            return updated_order
    raise HTTPException(status_code=404, detail=f'order {order_id} was not found')

@app.delete('/orders/{order_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['order_id'] == order_id:
            ORDERS.pop(index)
            return f'Order {order_id} has been deleted'
    raise HTTPException(status_code=404, detail=f'order {order_id} was not found')

def update_inventory(order: dict):
    inventory_changes = {}
    inventory_changes['items'] = order['items']
    for item in inventory_changes['items']:
        item['quantity'] = item['quantity'] * -1
    requests.put('https://c76vzjivmb.execute-api.us-west-1.amazonaws.com/dev/products/inventory', json=inventory_changes)

# products service = 172.31.8.169
# orders service = 172.31.5.34