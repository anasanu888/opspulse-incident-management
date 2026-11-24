import os, time, redis, pymysql

def rdb():
    return redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=int(os.getenv("REDIS_PORT","6379")), decode_responses=True)

def db():
    return pymysql.connect(host=os.getenv("MYSQL_HOST","mysql"), port=int(os.getenv("MYSQL_PORT","3306")),
      user=os.getenv("MYSQL_USER","opspulse"), password=os.getenv("MYSQL_PASSWORD","change_this_app_password"),
      database=os.getenv("MYSQL_DATABASE","opspulse"), cursorclass=pymysql.cursors.DictCursor, autocommit=True)

def wait_redis():
    c=rdb()
    for _ in range(30):
        try: c.ping(); return c
        except Exception: time.sleep(2)
    raise RuntimeError("Redis unavailable")

def wait_db():
    for _ in range(40):
        try:
            c=db(); c.close(); return
        except Exception: time.sleep(2)
    raise RuntimeError("MySQL unavailable")
