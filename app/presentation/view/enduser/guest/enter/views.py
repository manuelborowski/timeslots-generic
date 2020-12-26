from flask import redirect, render_template, request, url_for, jsonify, session, copy_current_request_context
import json
from . import enter
from app import log, socketio
from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from app.application import enduser as menduser

# @guest.route('/guest/<string:code>/<string:name>/<string:time>', methods=['POST', 'GET'])
@enter.route('/guest/enter', methods=['POST', 'GET'])
def show():
    print(request.args)
    code = request.args['code']
    guest = menduser.get_end_user(code, set_timestamp=True)

    config = {
        'check_server_endpoint': 'guest.enter.server_ajax_endpoint',
        'intro_video': "https://www.youtube.com/embed/YrLk4vdY28Q",
        'code': 'abcde',
        'first_name': 'manuel',
        'last_name': 'borowski',
        'email': 'emmanuel.borowski@gmail.com'
    }
    return render_template('guest/enter/enter.html', config=config, async_mode=socketio.async_mode)



@enter.route('/guest/enter/action/<string:jds>', methods=['GET', 'POST'])
def server_ajax_endpoint(jds):
    try:
        jd = json.loads(jds)
        if jd['action'] == 'get-timeout-1':
            return jsonify({"status": True})
    except Exception as e:
        log.error(f'execute action: {jd}')
        return jsonify({"status": False})

    return jsonify({"status": True})
