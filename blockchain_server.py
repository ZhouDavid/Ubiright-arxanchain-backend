from flask import Flask, request, jsonify
from external_api.blockchainApi import *
app = Flask(__name__)

@app.route("/user_register",methods=['POST'])
def register():
	data = request.json
	username = data['username']
	password = data['password']
	usertype = data['usertype']
	userid = user_register(username,password,usertype)
	return userid

@app.route('/create_asset',methods=['POST'])
def create_asset():
	data = request.json
	userid = data['userid']
	assetname = data['assetname']
	assetid = create_poe(userid,assetname)
	return assetid


@app.route('/query_asset',methods=['GET'])
def query_timestamp():
	assetid = request.args.get('assetid')
	info = query_poe(assetid)
	return jsonify(info)

@app.route()
# @app.route("/")
# def hello():
#     return "POST images to /mnistify"

# @app.route("/mnistify", methods=['POST'])
# def add_two_numbers():
#     data = request.json['data']
#     result = classify_image(spicynet, data)
#     return jsonify({'result': result})

app.run(host='0.0.0.0', port=5000)