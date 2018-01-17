import logging
import re
import MySQLdb
from database_login_info import *

def write_json_to_mysql(data):
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Start of write json to MySQL function..')
    conn = MySQLdb.connect(
        host = host,
        user = user,
        passwd = password,
        db = db,
    )

    c = conn.cursor()
    
    c.execute("INSERT INTO json_test (jdoc,) VALUES CAST(%s as JSON)", (data))
    conn.commit()
    logging.debug('End of write json to MySQL function.')