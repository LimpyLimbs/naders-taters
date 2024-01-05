from fastapi import FastAPI, Body
from starlette import status

app = FastAPI()

ORDERS = [
    {'orderID': 'order1', 'items': ['chips', 'soda', 'burger']},
    {'orderID': 'order2', 'items': ['chips', 'soda', 'hot dog']}
]

@app.get('/orders')
def get_orders():
    return ORDERS

@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(new_order=Body()):
    ORDERS.append(new_order)
    return 'order has been created'