from flask import Blueprint

from controllers.AttendancesController import *
from controllers.NavigationController import *
from controllers.AuthController import *
from controllers.ParticipantsController import *

routes_bp = Blueprint("routes_bp", __name__)

# navigation routes
routes_bp.route("/", methods=['GET'])(index)
routes_bp.route("/signin", methods=['GET'])(sign_in)
routes_bp.route("/signup", methods=['GET'])(sign_up)


# authentication routes
routes_bp.route("/register", methods=['POST'])(register_user)
routes_bp.route("/login", methods=['POST'])(login)


# participants routes
routes_bp.route("/add-participants", methods=['POST'])(add_participant)


# attendances routes
routes_bp.route("/mark-attendance", methods=['POST'])(mark_attendance)
routes_bp.route("/get_attendances", methods=['GET'])(get_attendances)
