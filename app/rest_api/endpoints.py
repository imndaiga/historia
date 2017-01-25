from . import api
from flask import jsonify, abort, make_response
from flask_httpauth import HTTPBasicAuth

http_auth = HTTPBasicAuth()


@http_auth.get_password
def get_password(username):
    if username == 'wasch':
        return 'cheers'
    return None


@api.route('/user/settings', methods=['GET'])
@http_auth.login_required
def get_settings_view():
    abort(404)


@api.route('/user/relationships', methods=['GET'])
@http_auth.login_required
def get_relationships_view():
    relationships_view = [
        {
            'sub_menu_present': True,
            'panels_present': False,
            'window_present': False,
            'sub_menu_items': {
                'List': 'info_button',
                'Add': 'primary_button',
                'Edit': 'warning_button'
            },
            'default_pane': 'List'
        }
    ]
    return jsonify({'view': relationships_view})


@api.route('/user/overview', methods=['GET'])
@http_auth.login_required
def get_overview_view():
    overview_view = [
        {
            'sub_menu_present': False,
            'panels_present': True,
            'window_present': False,
            'panel_items': {
                'Connections': 'green_pane',
                'Recommendations': 'blue_pane',
                'Leaderboard': 'orange_pane'
            }
        }
    ]
    return jsonify({'view': overview_view})


@api.route('/user/share', methods=['GET'])
@http_auth.login_required
def get_share_view():
    share_view = [
        {
            'sub_menu_present': False,
            'panels_present': True,
            'window_present': False,
            'panel_items': {
                'Facebook': 'fb_pane',
                'Twitter': 'tw_pane',
                'Gmail': 'gm_pane'
            }
        }
    ]
    return jsonify({'view': share_view})


@api.route('/user/visualisation', methods=['GET'])
@http_auth.login_required
def get_visualisation_view():
    visualisation_view = [
        {
            'sub_menu_present': False,
            'panels_present': False,
            'window_present': True,
            'window_attr': {
                'width': 'auto',
                'height': 'auto'
            }
        }
    ]
    return jsonify({'view': visualisation_view})


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@http_auth.error_handler
def unauthorised():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
