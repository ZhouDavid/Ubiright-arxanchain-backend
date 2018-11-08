from flask import Flask, request, jsonify
from external_api.blockchainApi import *
app = Flask(__name__)

@app.route("/user_register",methods=['POST'])
def _register_():
	data = request.json
	username = data['username']
	password = data['password']
	usertype = data['usertype']
	userid = user_register(username,password,usertype)
	return userid

@app.route('/create_asset',methods=['POST'])
def _create_asset_():
	data = request.json
	userid = data['userid']
	assetname = data['assetname']
	assetid = create_poe(userid,assetname)
	return assetid


@app.route('/query_asset',methods=['GET'])
def _query_asset_():
	assetid = request.args.get('assetid')
	info = query_poe(assetid)
	return jsonify(info)

@app.route('/transfer_coins',methods=['POST'])
def _transfer_coins_():
	data = request.json
	from_id = data['from_id']
	to_id = data['to_id']
	amount = data['amount']
	info = transfer_coins(from_id,to_id,amount)
	return jsonify(info)

@app.route('/issue_coins',methods=['POST'])
def _issue_coins_():
	data = request.json
	user_id = data['user_id']
	amount = data['amount']
	info = issue_coins(user_id,amount)
	return jsonify(info)

@app.route('/query_balance',methods=['GET'])
def _query_balance_():
	user_id = request.args.get('user_id')
	info = query_wallet_balance(user_id)
	return jsonify(info)

app.run(host='0.0.0.0', port=5000)