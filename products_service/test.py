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

inventory_changes = {
  "items": [
    {
      "flavor": "barbeque",
      "size": "small",
      "quantity": 2
    },
    {
      "flavor": "class",
      "size": "medium",
      "quantity": 2
    }
  ]
}

def update_inventory(inventory_changes):
    for product_name, product_details in PRODUCTS.items():
        for object in inventory_changes['items']:
            # print(product_name + ' ' + object['flavor'])
            if product_name == object['flavor']:
                print(product_name)
                new_inventory = product_details['inventory'][object['size']]
                new_inventory = new_inventory + object['quantity']
                
update_inventory(inventory_changes)
