import os
import constant
import json
import ast
import time
import base64
import util


def __handleResponse__(username,register_info):
	'''
	:param username: string, self-defined 
	:param register_info: unicode json, info get from user_register 
	:return: string, user_id get from arxan official blockchain server
	'''
	data = json.loads(str(info['Payload']))
	data['username'] = username
	with open(data['id']+'.json','w') as file:
		json.dump(data,file)
	self.user_id = data['id']
	return data['id']


def user_register(username,password,utype):
	'''
	:param username: string, self-defined
	:param password: string, 8-16 characters including upper case, lower case and digits
	:param utype: string, "Organization" or "Person"
	:return: string, user_id get from arxan official blockchain server
	'''
	header = {"Bc-Invoke-Mode": "sync"}
	body = {
	    "type": utype,
	    "access": username,
	    "secret": password
	}
	try:
		_,info = constant.walletClient.register(header,body)
	except:
		print('registration failed')
		return None

	finally:
		return __handleResponse__(username,info)

def create_poe(user_id,assetName):
	'''
	:param user_id: string, user_id got from arxahin official blockchain server
	:param assetName: string, article name created by user
	:return: 
	'''
	user_data = None
	try:
		with open(user_id+'.json','r') as file:
			user_data = file.read()  # open pre_stored user data named with user_id
	except:
		print('user not found')
	finally:
		user_data = ast.literal_eval(user_data)
		metadata = base64.b64encode(str({'count':0,'coins_earned':0}))  # initial number of read and coins eared should both be zero
		wallet_id = user_data['id']   # also known as user_id
		private_key_base64 = user_data['key_pair']['private_key']
		payload = {
			"id":"",
			"name":assetName,
			"hash":"", # to te decided later
			"parent_id":"",
			"owner":wallet_id,
			"metadata":metadata #encoded metadata
		}
		created_time = str(int(time.time())) # created timestamp
		params = {
			"creator": constant.ent_sign_param['creator'],
			"created": created_time,
			"nonce": 'ubiright', # your nonce for ed25519 signture
			"privateB64": private_key_base64,
			"payload": payload
		}
		self.payload = payload
		self.params = params
		header = {"Bc-Invoke-Mode": "sync"}
		_, response = constant.walletClient.create_poe(header, payload, params)
		assetData = json.loads(str(response['Payload']))
		assetData['creator'] = constant.ent_sign_param['creator']
		assetData['owner'] = wallet_id
		assetData['name'] = assetName
		assetData['metadata'] = metadata
		assetData['privateB64'] = private_key_base64
		assetData['created'] = created_time
		with open(assetData['id']+'.json','w') as file:    # wirte asset data to json file name wit asset_id
			json.dump(assetData,file)
		return assetData['id']

def update_poe(asset_id,updated_metadata):
	data = {}
	status_code = 200
	try:
		with open(asset_id+'.json','r') as file:
			data = json.load(file)
			payload = {
				"id":data['id'],
				"name":data['name'],
				"hash":"",
				"parent_id":"",
				"owner":data['owner'],
				"metadata":base64.b64encode(str(updated_metadata))
			}
			params = {
				'creator':constant.ent_sign_param['creator'],
				'nonce':constant.ent_sign_param['nonce'],
				'privateB64':data['privateB64'],
				'created':data['created'],
				'payload':payload
			}
			header = {"Bc-Invoke-Mode": "sync"}
			try:
				_,resp = constant.walletClient.update_poe(header,payload,params)
			except:
				print('update failed')
				status_code = 400
	except:
		print('asset_id not found')
		status_code = 404
	finally:
		return status_code

def query_poe(asset_id):
	res = util.query_poe(asset_id)
	return res

def issue_token(asset_id,amount):
	data = {}
	status_code = 200
	token_id = -1
	try:
		with open(asset_id+'.json','r') as file:
			data = json.load(file)
		payload = {
			"issuer":constant.ent_sign_param['creator'],
			"owner":data['owner'],
			"asset_id":data['id'],
			"amount":amount
		}
		params = {
			'creator':constant.ent_sign_param['creator'],
			'created':str(int(time.time())),
			'nonce':constant.ent_sign_param['nonce'],
			'privateB64':data['privateB64'],
			'payload':payload
		}
		header = {"Bc-Invoke-Mode": "sync"}
		try:
			_,resp=constant.walletClient.issue_colored_token(header,payload,params)
			token_id = json.loads(str(resp['Payload']))['token_id']
		except:
			print('issue token failed')
			status_code = 400
	except:
		print('asset_id not found')
		status_code = 400
	finally:
		return (status_code,token_id)

def transfer_token(wallet_id,amount,from_id,to_id,token_id):
	with open(wallet_id+'.json','r') as file:
		data = json.load(file)
		privateB64 = data['privateB64']
		try:
			payload = {
				'from':from_id,
				'to':to_id,
				'asset_id':asset_id,
				'tokens':[
					{
						'token_id':token_id,
						'amount':amount
					}
				]
			}
			params = {
				'creator':constant.ent_sign_param['creator'],
				'created':str(int(time.time())),
				'nonce':constant.ent_sign_param['nonce'],
				'privateB64':privateB64,
				'payload':payload
			}
			header = {"Bc-Invoke-Mode": "sync"}
			_,info = constant.walletClient.transfer_colored_tokens(header, payload, params)
			return info
		except:
			return None

def query_wallet_balance(wallet_id):
	header = {"Bc-Invoke-Mode": "sync"}
 	_,resp = constant.walletClient.query_wallet_balance(header,wallet_id)
 	return resp

if __name__ == '__main__':
 	 user = User('test-ubiright16','Gixstudent2018')
 	 # asset_id = user.create_poe('hello world4')
 	 # token_id = user.issue_token(asset_id,999)
 	 user_id1 = 'did:axn:3118752e-6f67-435d-b838-9e4a0e47809f'
 	 user_id2 = 'did:axn:6c7b90a0-a1d2-496d-bb98-d9f7ea054822'
 	 token_id = '3379f130c1490ad09abf805b4670e574149d36cf9f284e944f2e395a520d6bb2'
 	 asset_id = 'did:axn:17253ed2-0712-440a-9d39-b890ab3df84b'
 	 # print('----------before transfer1-----------')
 	 # print(user.query_wallet_balance(user_id1))
 	 # print(user.query_wallet_balance(user_id2))
 	 # user.transfer_token(100,user_id1,user_id2,token_id,asset_id)
 	 # print('----------after transfer1------------')
 	 # print(user.query_wallet_balance(user_id1))
 	 # print(user.query_wallet_balance(user_id2))
 	 user.transfer_token(66,user_id2,user_id1,token_id,"")
 	 print('----------after transfer2------------')
 	 print(user.query_wallet_balance(user_id1))
 	 print(user.query_wallet_balance(user_id2))


 	 #################
 	 # transfer token#
 	 #################



 	 #################
 	 # query balance #
 	 #################

 	 # header = {"Bc-Invoke-Mode": "sync"}
 	 # _,resp = constant.walletClient.query_wallet_balance(header,'did:axn:6c7b90a0-a1d2-496d-bb98-d9f7ea054822')
 	 # print resp



			

		
