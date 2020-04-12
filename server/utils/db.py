import psycopg2

def db_connection():
  host = ""
  db_user = ""
  db_password = ""
  db_name = ""  

  return psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=host
  )
