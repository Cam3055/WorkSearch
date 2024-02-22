import zenoh
from json import dumps
import json
def listener(data):
    # json_data = dumps(data.payload)
    data=data.payload
    data=data.decode('utf-8')
    data = json.loads(data)
    print('update_table', {'data': data[0]})



session = zenoh.open()
key = "vm1/answer"
sub = session.declare_subscriber(key,listener)
while True:
    pass