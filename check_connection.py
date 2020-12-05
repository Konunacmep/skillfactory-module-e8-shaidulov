from sqlalchemy import create_engine
import sys
import os
engine = create_engine(os.environ.get('DATABASE_URL'))

try:
    with engine.connect() as connection:
        with connection.begin():
            r1 = connection.execute("select 1")
            sys.exit(0)
except Exception as e:
    sys.exit(1)