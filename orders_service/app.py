from datetime import datetime
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from starlette import status
from schemas import CreateOrderSchema, GetOrderSchema, UpdateOrderSchema
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
    order['price'] = calculate_price(order)
    ORDERS.append(order)
    order_copy = deepcopy(order)
    for item in order_copy['items']:
        item['quantity'] = item['quantity'] * -1
    update_inventory(order_copy)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['order_id'] == order_id:
            return order
        raise HTTPException(status_code=404, detail=f'order {order_id} was not found')
    
@app.put('/orders/{order_id}', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def update_order(order_id: UUID, order: UpdateOrderSchema):
    new_order = order.model_dump()
    for index, old_order in enumerate(ORDERS):
        if old_order['order_id'] == order_id:
            new_order['price'] = calculate_price(new_order)
            ORDERS[index] = new_order
            # returns the items from the old order to the /products/inventory service
            update_inventory(old_order)
            # create a copy of the new order and remove those items from the /products/inventory service
            order_copy = deepcopy(new_order)
            for item in order_copy['items']:
                item['quantity'] = item['quantity'] * -1
            update_inventory(order_copy)
            return new_order
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
    requests.put('https://c76vzjivmb.execute-api.us-west-1.amazonaws.com/dev/products/inventory', json=inventory_changes)
    
def calculate_price(order: dict):
    product_prices = requests.get('https://c76vzjivmb.execute-api.us-west-1.amazonaws.com/dev/products/prices').json()
    order_price = 0
    for item in order['items']:
        order_price = order_price + (item['quantity'] * product_prices[item['flavor']][item['size']])
    # round order price to nearest hundredth
    order_price = round(order_price, 2)
    return order_price

# products service = https://c76vzjivmb.execute-api.us-west-1.amazonaws.com/dev/products/inventory
# http://127.0.0.1:8080/products/prices
# http://127.0.0.1:8080/products/inventory
# orders service = https://c76vzjivmb.execute-api.us-west-1.amazonaws.com/dev/orders/