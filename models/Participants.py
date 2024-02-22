import json
import uuid
from utilities.helpers import get_db_connection


class Participants:

  @classmethod
  def insert_participant(cls, id, name, user_id, group):
    try:
      connection, cursor = get_db_connection()

      part_id = id if id else str(uuid.uuid4().hex)
      cursor.execute(f"""INSERT INTO `participants` (`id`,`name`,`user_id`,`group`)
                          VALUES(%s,%s,%s,%s);""", (part_id, name, user_id, group))
      connection.commit()
      return part_id
    except Exception as error:
      return error

  @classmethod
  def update_participant_face(cls, id, face_data):
    try:
      connection, cursor = get_db_connection()

      face_data = json.dumps(face_data)
      cursor.execute(f"""UPDATE `participants` SET `face_data` = %s WHERE `id` = %s;""", (face_data, id))
      connection.commit()
      return True
    except Exception as error:
      return error


  @classmethod
  def get_participants(cls, id=None, name=None, group=None):
    try:
      connection, cursor = get_db_connection()

      conditions = []
      if id: conditions.append(f'`id` = {id}')
      if name: conditions.append(f'`name` LIKE "%{name}%"')
      if name: conditions.append(f'`group` = "{group}"')

      where_clause = f" WHERE {' AND '.join(conditions)}" if len(conditions) > 0 else ""

      cursor.execute(f"""SELECT * FROM `participants`{where_clause};""")
      rows = cursor.fetchall()
      return rows[0] if id or name else rows
    except Exception as error:
      return error
    

