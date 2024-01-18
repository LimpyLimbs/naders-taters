from fastapi import FastAPI, Body
from schemas import UpdateInventorySchema
from starlette import status

app = FastAPI()

PRODUCTS = {
    'classic': {
        'prices': {
            'small': 1.73,
            'medium': 2.31,
            'large': 3.42
            },
        'inventory': {
            'small': 364,
            'medium': 362,
            'large': 125
        }
    },
    'barbeque': {
        'prices': {
            'small': 1.21,
            'medium': 2.31,
            'large': 3.73
            },
        'inventory': {
            'small': 834,
            'medium': 732,
            'large': 15
        }
    },
    'sour_cream_and_onion': {
        'prices': {
            'small': 1.22,
            'medium': 2.20,
            'large': 3.39
            },
        'inventory': {
            'small': 1364,
            'medium': 3462,
            'large': 1472
        }
    },
    'salt_and_vinegar': {
        'prices': {
            'small': 1.63,
            'medium': 2.31,
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
            'small': 1.44,
            'medium': 2.83,
            'large': 3.09
            },
        'inventory': {
            'small': 5834,
            'medium': 7325,
            'large': 1455
        }
    },
    'pizza': {
        'prices': {
            'small': 1.77,
            'medium': 2.84,
            'large': 3.33
            },
        'inventory': {
            'small': 386,
            'medium': 7322,
            'large': 162
        }
    },
    'jalapano': {
        'prices': {
            'small': 1.13,
            'medium': 2.37,
            'large': 3.73
            },
        'inventory': {
            'small': 8264,
            'medium': 3612,
            'large': 1415
        }
    },
    'kettle_cooked': {
        'prices': {
            'small': 1.54,
            'medium': 2.28,
            'large': 3.07
        },
        'inventory': {
            'small': 7836,
            'medium': 7762,
            'large': 3125
        }
    },
    'dill_pickle': {
        'prices': {
            'small': 1.11,
            'medium': 2.53,
            'large': 3.59
            },
        'inventory': {
            'small': 2834,
            'medium': 9736,
            'large': 5125
        }
    },
    'salt_and_pepper': {
        'prices': {
            'small': 1.34,
            'medium': 2.42,
            'large': 3.94
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