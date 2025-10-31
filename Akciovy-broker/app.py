from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

clients = {}
orders = {}
matches = {}

def now_iso():
    return datetime.utcnow().isoformat() + 'Z'

def auth_required(fn):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
        else:
            token = ''
        if not token or token not in clients:
            return jsonify({"code": "UNAUTHORIZED", "message": "Missing or invalid token"}), 401
        request.client_id = token
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@app.route('/')
def home():
    return "Akciovy broker demo API"

@app.route('/api')
def swagger_ui():
    return send_from_directory('.', 'index.html')

@app.route('/openapi.yaml')
def openapi_yaml():
    return send_from_directory('.', 'openapi.yaml')

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json() or {}
    nickname = data.get('nickname')
    address = data.get('address', '')
    if not nickname or len(nickname.strip()) < 2:
        return jsonify({"code": "VALIDATION_ERROR", "message": "nickname is required (min 2 chars)"}), 400
    client_id = str(uuid.uuid4())
    client = {
        "id": client_id,
        "nickname": nickname,
        "address": address,
        "createdAt": now_iso()
    }
    clients[client_id] = client
    return jsonify({"client": client, "token": client_id}), 201

@app.route('/orders/sell', methods=['POST'])
@auth_required
def create_sell():
    data = request.get_json() or {}
    stock = data.get('stock')
    amount = data.get('amount')
    address = data.get('address')
    if not stock or not isinstance(amount, int) or amount < 1 or not address:
        return jsonify({"code": "VALIDATION_ERROR", "message": "stock, amount (int>0) and address are required"}), 400
    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "stock": stock,
        "amount": amount,
        "clientId": request.client_id,
        "createdAt": now_iso(),
        "status": "open",
        "type": "sell",
        "address": address
    }
    orders[order_id] = order
    return jsonify(order), 201

@app.route('/orders/buy', methods=['POST'])
@auth_required
def create_buy():
    data = request.get_json() or {}
    stock = data.get('stock')
    amount = data.get('amount')
    if not stock or not isinstance(amount, int) or amount < 1:
        return jsonify({"code": "VALIDATION_ERROR", "message": "stock and amount (int>0) are required"}), 400
    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "stock": stock,
        "amount": amount,
        "clientId": request.client_id,
        "createdAt": now_iso(),
        "status": "open",
        "type": "buy"
    }
    orders[order_id] = order
    return jsonify(order), 201

@app.route('/orders/sells', methods=['GET'])
def list_sells():
    page = max(1, int(request.args.get('page', 1)))
    pageSize = min(100, max(1, int(request.args.get('pageSize', 20))))
    stock_filter = request.args.get('stock')
    items = [o for o in orders.values() if o['type'] == 'sell']
    if stock_filter:
        items = [o for o in items if o['stock'] == stock_filter]
    total = len(items)
    start = (page-1)*pageSize
    end = start + pageSize
    return jsonify({"items": items[start:end], "total": total}), 200

@app.route('/orders/buys', methods=['GET'])
def list_buys():
    page = max(1, int(request.args.get('page', 1)))
    pageSize = min(100, max(1, int(request.args.get('pageSize', 20))))
    stock_filter = request.args.get('stock')
    items = [o for o in orders.values() if o['type'] == 'buy']
    if stock_filter:
        items = [o for o in items if o['stock'] == stock_filter]
    total = len(items)
    start = (page-1)*pageSize
    end = start + pageSize
    return jsonify({"items": items[start:end], "total": total}), 200

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"code": "NOT_FOUND", "message": "Order not found"}), 404
    return jsonify(order), 200

@app.route('/orders/<order_id>', methods=['DELETE'])
@auth_required
def delete_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"code": "NOT_FOUND", "message": "Order not found"}), 404
    if order['clientId'] != request.client_id:
        return jsonify({"code": "FORBIDDEN", "message": "Not owner"}), 403
    del orders[order_id]
    return '', 204

@app.route('/simulate/match', methods=['POST'])
@auth_required
def simulate_match():
    data = request.get_json() or {}
    sell_id = data.get('sellOrderId')
    buy_id = data.get('buyOrderId')
    if not sell_id or not buy_id:
        return jsonify({"code": "VALIDATION_ERROR", "message": "sellOrderId and buyOrderId required"}), 400
    sell = orders.get(sell_id)
    buy = orders.get(buy_id)
    if not sell or not buy:
        return jsonify({"code": "NOT_FOUND", "message": "Order not found"}), 404
    if sell['type'] != 'sell' or buy['type'] != 'buy':
        return jsonify({"code": "INVALID", "message": "Order types mismatch"}), 400
    sell['status'] = 'matched'
    buy['status'] = 'matched'
    match_id = str(uuid.uuid4())
    match = {
        "id": match_id,
        "sellOrderId": sell_id,
        "buyOrderId": buy_id,
        "sellerAddress": sell.get('address', ''),
        "createdAt": now_iso()
    }
    matches[match_id] = match
    return jsonify(match), 201

@app.route('/matches/<order_id>', methods=['GET'])
def get_matches_for_order(order_id):
    results = [m for m in matches.values() if m['sellOrderId'] == order_id or m['buyOrderId'] == order_id]
    if not results:
        return jsonify({"code": "NOT_FOUND", "message": "No matches found for given order"}), 404
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
x