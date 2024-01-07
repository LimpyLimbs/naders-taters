from enum import Enum
import json

class Size(str, Enum):
    small = 'small value'
    medium = 'medium value'
    large = 'large value'
    
    # def __str__(self):
    #     return self.value

item = Size.small
json_string = json.dumps(item)
print(json_string)