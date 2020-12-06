from app import db
import os
import nsq
from app.models import Results
import json

# engine = create_engine(os.environ.get('DATABASE_URL'))

def handler(message):
    new_res = Results(**json.loads(message.body))
    db.session.add(new_res)
    db.session.commit()
    # print(f'came in handler {message.body}')
    return True

r = nsq.Reader(message_handler=handler,
        lookupd_http_addresses=[os.environ.get('HTTP_ADDRESSES')],
        topic=os.environ.get('TOPIC'), channel='default', lookupd_poll_interval=5)
nsq.run()
