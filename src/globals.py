import os

from dotenv import load_dotenv

load_dotenv()

login_pwd = os.getenv("LOGIN_PWD")
admin_pwd = os.getenv("ADMIN_PWD")

cafe_table_name = os.getenv("CAFE_TABLE")
toilet_table_name = os.getenv("TOILET_TABLE")

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pwd = os.getenv("DB_PWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_connection_string = f"dbname={db_name} user={db_user} password={db_pwd} host={db_host} port={db_port}"

if (
    not login_pwd or
    not admin_pwd or
    not cafe_table_name or
    not toilet_table_name or 
    not db_name or
    not db_user or
    not db_pwd or 
    not db_host or 
    not db_port or 
    not db_connection_string
    ):
    raise ModuleNotFoundError("Unable to find one or more environment vars")
