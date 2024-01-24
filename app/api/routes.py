from flask import Blueprint, request, jsonify, abort
from app.common.superset import create_guest_token
from utils.guest_token_payload import GuestTokenPayload
import logging
from werkzeug.exceptions import HTTPException

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
        company_id = request.args.get('company_id', type=int, default=0)

        if not company_id or company_id == 0:
            abort(400, description="Missing company_id parameter.")

        parameters = {
            "company_id": company_id
        }

        payload = GuestTokenPayload()
        logging.info("Payload: " + str(payload))
        data = payload.get_payload_data(parameters)
        logging.info("Payload data: " + str(data))
        guest_token = create_guest_token(data, auto_generate_resources=False)

        return jsonify(guest_token=guest_token)
    
    except HTTPException as e:
        logging.error("Error generating guest token: " + str(e))
        abort(e.code, description=e.description)

    except Exception as e:
        logging.error("Error generating guest token: " + str(e))
        abort(500, description="Internal server error.")
