from flask import jsonify, request, Response
from . import oclab_bp
from .controllers import get_oclab_data, get_oclab_order_data, get_oclab_order_request_hook, get_provider_register_data
import urllib
import urllib.parse
from APIException import APIException

@oclab_bp.route('/collection', methods=['GET'])
@oclab_bp.route('/collection/', methods=['GET'])
def order_collection_data():
	# print(request.path)
    parsed_url = urllib.parse.urlparse(request.url)
    if request.args.get("sid"):
        # OC Lab Request Form : Submission ID of form '5601513206446536954'
        sid = urllib.parse.parse_qs(parsed_url.query).get('sid')[0]
        data = get_oclab_data(sid)
        return jsonify(data)
    else:
    	raise APIException('Invalid request - Query parameter sid is missing', status_code=400)

@oclab_bp.route('/order_request', methods=['GET'])
@oclab_bp.route('/order_request/', methods=['GET'])
def order_request_data():
	# print(request.path)
    parsed_url = urllib.parse.urlparse(request.url)
    if request.args.get("sid"):
        # OC Lab Request Form : Submission ID of form '5601513206446536954'
        sid = urllib.parse.parse_qs(parsed_url.query).get('sid')[0]
        data = get_oclab_order_data(sid)
        return jsonify(data)
    else:
    	raise APIException('Invalid request - Query parameter sid is missing', status_code=400)

@oclab_bp.route('/order_request_hooks', methods=['GET'])
@oclab_bp.route('/order_request_hooks/', methods=['GET'])
def order_request_hook():
    parsed_url = urllib.parse.urlparse(request.url)
    if parsed_url:
        data = get_oclab_order_request_hook(parsed_url)
        return data
    else:
    	raise APIException('Invalid request', status_code=400)

@oclab_bp.route('/check_provider_register', methods=['GET'])
@oclab_bp.route('/check_provider_register/', methods=['GET'])
def check_provider_register():
    # print(request.path)
    parsed_url = urllib.parse.urlparse(request.url)
    if request.args.get("nfcid"):
        # OC Lab Request Form : Submission ID of form '5601513206446536954'
        nfcid = urllib.parse.parse_qs(parsed_url.query).get('nfcid')[0]
        data = get_provider_register_data(nfcid)
        return jsonify(data)
    else:
        raise APIException('Invalid request - Query parameter nfcid is missing', status_code=400)