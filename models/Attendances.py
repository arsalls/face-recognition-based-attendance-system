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
      if user_id:
        conditions.append(f"`user_id` = '{user_id}'")
      if participant_id:
        if len(participant_id) > 0:
          conditions.append(f"`participant_id` = '{participant_id}'")
      if start_datetime:
        conditions.append(f"`mark_datetime` >= '{start_datetime}'")
      if end_datetime:
        conditions.append(f"`mark_datetime` <= '{end_datetime}'")

      where_clause = f" WHERE {' AND '.join(conditions)}" if len(conditions) > 0 else ""
      query = f"""SELECT att.*, part.* FROM `attendance` att join `participants` part {where_clause};"""
      cursor.execute(query)
      rows = cursor.fetchall()
      return rows
    except Exception as error:
      return error
    

