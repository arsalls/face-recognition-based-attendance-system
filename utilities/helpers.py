import os
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from functools import wraps
from flask import redirect, url_for, request, session
import pymysql
from flask import jsonify, g

rds_host = os.getenv('DB_SERVER')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')


# SUCCESS RESPONSE
def success(data=None, status_code=200):
  resp = jsonify({
    "message": "success",
    "status": status_code,
    "data": data
  })
  resp.status_code = status_code
  resp.headers['Content-Type'] = 'application/json'
  resp.headers['Access-Control-Allow-Origin'] = '*'
  resp.headers['Access-Control-Allow-Headers'] = '*'
  resp.headers['Access-Control-Allow-Methods'] = '*'
  return resp


def fail(data=None, status_code=500):
  resp = jsonify({
    "message": "fail",
    "status": status_code,
    "data": data
  })
  resp.status_code = status_code
  resp.headers['Content-Type'] = 'application/json'
  resp.headers['Access-Control-Allow-Origin'] = '*'
  resp.headers['Access-Control-Allow-Headers'] = '*'
  resp.headers['Access-Control-Allow-Methods'] = '*'
  return resp


def open_db_connection():
  try:
    connection = pymysql.connect(host=rds_host, user=username, passwd=password, db=database_name)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor
  except Exception as e:
    return e


def get_db_connection():
  try:
    if "connection" not in g or "cursor" not in g:
      g.connection, g.cursor = open_db_connection()
    return g.connection, g.cursor
  except Exception as e:
    return e


def destroy_db_connection():
  try:
    connection = g.pop("connection", None)
    if connection is not None:
      if connection.open:
          connection.close()
  except Exception as e:
    return e


def encrypt(data):
  data = bytes(data, 'utf-8')
  encrypted = b64e(zlib.compress(data, 9))
  return encrypted.decode("utf-8")


def decrypt(data):
  decrypted = zlib.decompress(b64d(data))
  return decrypted.decode("utf-8")


def convert_to_camel_case(input_dict):
  snake_to_camel = lambda key: key.split('_')[0] + ''.join(word.title() for word in key.split('_')[1:])
  camel_case_dict = {snake_to_camel(key): value for key, value in input_dict.items()}
  return camel_case_dict


def login_required(f):

  @wraps(f)
  def decorated_function(*args, **kwargs):
    request_user = request.cookies.get('user')
    if not request_user:
      return redirect('/signin')

    if 'user' in session:
      session_user = session['user']
      if request_user != session_user:
        return redirect('/signin')
    else:
      return redirect('/signin')

    return f(*args, **kwargs)

  return decorated_function

def remove_folder_and_files(folder_path):
  try:
    for file_name in os.listdir(folder_path):
      file_path = os.path.join(folder_path, file_name)
      if os.path.isfile(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        remove_folder_and_files(file_path)

      os.rmdir(folder_path)
      print(f"Folder {folder_path} removed successfully.")
  except Exception as e:
    return e