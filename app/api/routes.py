from flask import Blueprint, request, jsonify, abort
from app.config.superset import create_guest_token
from utils.guest_token_payload import GuestTokenPayload

routes = Blueprint('routes', __name__)

@routes.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=str(error)), 500

@routes.errorhandler(400)
def bad_request(error):
    return jsonify(error=str(error)), 400

@routes.route('/api/guest-token-by-company', methods=['GET'])
def get_guest_token():
    """  
    Generate a guest token for a company.
    """
    try:
        company_id = request.args.get('company_id')

        if not company_id:
            abort(400, description="Missing company_id parameter.")

        parameters = {
            "company_id": company_id
        }

        payload = GuestTokenPayload()
        data = payload.get_payload_data(parameters)

        guest_token = create_guest_token(data)

        return jsonify(guestToken=guest_token)
    except Exception as e:
        abort(500, str(e))