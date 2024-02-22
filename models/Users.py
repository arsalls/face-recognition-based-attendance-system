import uuid
from utilities.helpers import get_db_connection


class Users:

  @classmethod
  def insert_user(cls, name, email, password):
    try:
      connection, cursor = get_db_connection()

      id = str(uuid.uuid4().hex)
      cursor.execute(f"""INSERT INTO `users` (`id`,`name`,`email`,`password`)
                          VALUES(%s,%s,%s,%s);""", (id, name, email, password))
      connection.commit()
      return id
    except Exception as error:
      return error


  @classmethod
  def get_users(cls, id=None, name=None, email=None, password=None):
    try:
      connection, cursor = get_db_connection()

      conditions = []
      if id: conditions.append(f"`id` = '{id}'")
      if name: conditions.append(f"`name` LIKE '%{name}%'")
      if email: conditions.append(f"`email` = '{email}'")
      if password: conditions.append(f"`password` = '{password}'")

      where_clause = f" WHERE {' AND '.join(conditions)}" if len(conditions) > 0 else ""

      cursor.execute(f"""SELECT * FROM `users`{where_clause};""")
      rows = cursor.fetchall()
      return rows[0] if id or name or email or password else rows
    except Exception as error:
      return error


  @classmethod
  def check_user(cls, email):
    try:
      connection, cursor = get_db_connection()

      cursor.execute(f"""SELECT * FROM `users` WHERE `email`=%s;""", (email,))
      row = cursor.fetchone()
      return True if row else False
    except Exception as error:
      return error
    

