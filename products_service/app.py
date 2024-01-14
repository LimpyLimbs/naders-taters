from fastapi import FastAPI, Body
from schemas import UpdateInventorySchema
from starlette import status

app = FastAPI()

PRODUCTS = {
    'classic': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 364,
            'medium': 362,
            'large': 125
        }
    },
    'barbeque': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 834,
            'medium': 732,
            'large': 15
        }
    },
    'sour_cream_and_onion': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 1364,
            'medium': 3462,
            'large': 1472
        }
    },
    'salt_and_vinegar': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 7864,
            'medium': 9362,
            'large': 645
        }
    },
    'cheddar': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 5834,
            'medium': 7325,
            'large': 1455
        }
    },
    'pizza': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 386,
            'medium': 7322,
            'large': 162
        }
    },
    'jalapano': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 8264,
            'medium': 3612,
            'large': 1415
        }
    },
    'kettle_cooked': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
        },
        'inventory': {
            'small': 7836,
            'medium': 7762,
            'large': 3125
        }
    },
    'dill_pickle': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
            },
        'inventory': {
            'small': 2834,
            'medium': 9736,
            'large': 5125
        }
    },
    'salt_and_pepper': {
        'prices': {
            'small': 1.99,
            'medium': 2.99,
            'large': 3.99
        },
        'inventory': {
            'small': 3564,
            'medium': 7562,
            'large': 1455
        }
    }
}

@app.get('/products')
def get_all():
    return PRODUCTS

@app.get('/products/prices')
def get_prices():
    prices = {}
    for product_name, product_details in PRODUCTS.items():
        prices[product_name] = product_details['prices']
    return prices

@app.get('/products/inventory')
def get_inventory():
    inventory = {}
    for product_name, product_details in PRODUCTS.items():
        inventory[product_name] = product_details['inventory']
    return inventory

@app.put('/products/inventory', status_code=status.HTTP_201_CREATED)
def update_inventory(inventory_changes: UpdateInventorySchema):
    inventory_changes_dict = inventory_changes.model_dump()
    for product_name, product_details in PRODUCTS.items():
        for object in inventory_changes_dict['items']:
            if product_name == object['flavor']:
                old_inventory = product_details['inventory'][object['size']]
                new_inventory = old_inventory + object['quantity']
                product_details['inventory'][object['size']] = new_inventory
                return {"old_inventory": old_inventory, "new_inventory": new_inventory}
            
                
                
'''
products service is responsible for maintaining a list of products and their details
'''
# products service = 172.31.8.169
# orders service = 172.31.5.34