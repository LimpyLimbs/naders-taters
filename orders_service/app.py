from datetime import datetime
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from starlette import status
from schemas import CreateOrderSchema, GetOrderSchema

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