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
routes_bp.route("/attendance", methods=['GET'])(attendance)


# authentication routes
routes_bp.route("/register", methods=['POST'])(register_user)
routes_bp.route("/login", methods=['POST'])(login)


# participants routes
routes_bp.route("/action-participant", methods=['POST'])(action_participant)
routes_bp.route("/del-participants", methods=['POST'])(del_participant)
routes_bp.route("/get-participants", methods=['GET'])(get_participants)


# attendances routes
routes_bp.route("/mark-attendance", methods=['POST'])(mark_attendance)
routes_bp.route("/get_attendances", methods=['POST'])(get_attendances)
routes_bp.route("/generate-attendance", methods=['GET'])(generate_attendance)
