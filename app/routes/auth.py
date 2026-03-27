from flask import Blueprint, request, jsonify

bp = Blueprint('auth', __name__, url_prefix='/api')

# Mock 用户数据
MOCK_USERS = [
    {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
    {'username': 'user', 'password': 'user123', 'role': 'user'},
]


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'code': 400, 'msg': '请提供用户名和密码'}), 400

    username = data['username']
    password = data['password']

    user = next((u for u in MOCK_USERS if u['username'] == username and u['password'] == password), None)

    if user is None:
        return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401

    return jsonify({
        'code': 200,
        'msg': '登录成功',
        'data': {'username': user['username'], 'role': user['role'], 'token': f'mock-token-{username}'}
    })
