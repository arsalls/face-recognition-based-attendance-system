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
    

