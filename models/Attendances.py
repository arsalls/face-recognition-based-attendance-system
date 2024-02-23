from utilities.helpers import get_db_connection


class Attendances:

  @classmethod
  def mark_attendance(cls, user_id, participant_id):
    try:
      connection, cursor = get_db_connection()

      cursor.execute(f"""INSERT INTO `attendance` (`user_id`,`participant_id`) 
                          VALUES(%s,%s);""", (user_id, participant_id))
      connection.commit()
      return True
    except Exception as error:
      return error

  @classmethod
  def get_attendances(cls, user_id=None, participant_id=None, start_datetime=None, end_datetime=None):
    try:
      connection, cursor = get_db_connection()

      conditions = []
      data = []
      if user_id:
        conditions.append(f"`user_id` = %s")
        data.append(user_id)
      if participant_id:
        conditions.append(f"`participant_id` = %s")
        data.append(participant_id)
      if start_datetime:
        conditions.append(f"`mark_datetime` >= %s")
        data.append(start_datetime)
      if end_datetime:
        conditions.append(f"`mark_datetime` <= %s")
        data.append(end_datetime)

      where_clause = f" WHERE {' AND '.join(conditions)}" if len(conditions) > 0 else ""

      cursor.execute(f"""SELECT * FROM `attendance`{where_clause};""")
      rows = cursor.fetchall()
      return True
    except Exception as error:
      return error
    

