import logging
import pymysql
#import MySQLdb

logger = logging.getLogger(__name__)

def get_record_db_cursor():
    try:
        db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="root",
            db="doctor_friende",
            charset="utf8",
    )
    except Exception as e:
        logger.error(e)
    else:
        return db.cursor()

