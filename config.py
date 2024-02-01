import os
from dotenv import load_dotenv
load_dotenv()

mysql_pass = os.environ.get('ENV_MY_SQL_PASS')
rmq_user = os.environ.get('ENV_RMQ_USER')
rmq_pass = os.environ.get('ENV_RMQ_PASS')
# DB_URL = "mysql+pymysql://root:@localhost:3306/mw_db"
# DB_URL = f"mysql+pymysql://root:{mysql_pass}@localhost:3306/mw_db"
# if not working in docker, use the below DB_URL
DB_URL = f"mysql+pymysql://root:{mysql_pass}@db/mw_db"
# RMQ_URL = "amqp://guest:guest@localhost:5672//"
RMQ_URL = f"amqp://{rmq_user}:{rmq_pass}@rabbitmq:5672//"
