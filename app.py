from datetime import datetime
from uuid import uuid4, UUID
from fastapi import FastAPI
from starlette import status
from schemas import CreateOrderSchema, GetOrderSchema, Flavor, Size
import boto3
import json

app = FastAPI()

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
dynamodb_table_name = 'naders_taters_orders_service'
dynamodb_table = dynamodb.Table(dynamodb_table_name)

@app.get('/orders')
def get_order_ids():
    response = dynamodb_table.scan()
    order_ids = [item['order_id'] for item in response.get('Items', [])]
    return order_ids

@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def create_order(items: CreateOrderSchema):
    order = items.model_dump()
    order['order_id'] = uuid4()
    order['created'] = datetime.utcnow()
    import_order_to_dynamodb(order)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id_request: UUID):
    response = dynamodb_table.scan()
    order_id_list = [item['order_id'] for item in response.get('Items', [])] # figure out how this works
    for order_id in order_id_list:
        if order_id == order_id_list:
            # get the contents of that entry
            # return contents
        # return 404 if not found

def import_order_to_dynamodb(order_data: GetOrderSchema):
    order_id = str(order_data['order_id'])
    created = str(order_data['created'])
    items = json.dumps(order_data['items'])
    dynamodb_item = {
        'order_id': order_id,
        'created': created,
        'items': items
    }
    response = dynamodb_table.put_item(Item=dynamodb_item)
    return response['ResponseMetadata']['HTTPStatusCode']