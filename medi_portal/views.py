from flask import jsonify, request, Response
from . import medi_bp
from .controllers import get_intake_data
import urllib
import urllib.parse
from APIException import APIException

@medi_bp.route('/intake', methods=['GET'])
@medi_bp.route('/intake/', methods=['GET'])
def intake_data():
	# print(request.path)
    parsed_url = urllib.parse.urlparse(request.url)
    if request.args.get("sid"):
        # Clone of Medication List : Submission ID of form '223604174814150'
        sid = urllib.parse.parse_qs(parsed_url.query).get('sid')[0]
        data = get_intake_data(sid)
        return jsonify(data)
    else:
    	raise APIException('Invalid request - Query parameter sid is missing', status_code=400)
