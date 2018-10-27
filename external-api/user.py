import os
import constant
import json
import ast
import time
import base64
import util

class User:
	def __init__(self,accountName,password,userType="Person"):
		self._accountName = accountName
		self._password = password
		self._type = userType

	def __handleResponse__(self,info):
		data = json.loads(str(info['Payload']))
		data['username'] = self._accountName;
		with open(self._accountName+'.json','w') as file:
			json.dump(data,file)
		self.user_id = data['id']
		return data['id']
		

	def register(self):
		header = {"Bc-Invoke-Mode": "sync"}
		body = {
		    "type": "Organization",
		    "access": self._accountName,
		    "secret": self._password  ## 8-16 characters including upper case, lower case and digits
		}
		try:
			_,info = constant.walletClient.register(header,body)
		except:
			print('registration failed')
			return

		finally:
			return self.__handleResponse__(info)

	def create_poe(self,assetName):
		file = None
		try:
			file = open(self._accountName+'.json','r')
			print self
		except:
			print('user not found')
			return
		finally:
			user_data = ast.literal_eval(file.read())
			metadata = base64.b64encode(str({'count':0,'coins_earned':0}))
			wallet_id = user_data['id']   # also known as user_id
			private_key_base64 = user_data['key_pair']['private_key']
			payload = {
				"id":"",
				"name":assetName,
				"hash":"",
				"parent_id":"",
				"owner":wallet_id,
				"metadata":metadata
			}
			created_time = str(int(time.time()))
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
			with open(assetData['id']+'.json','w') as file:
				json.dump(assetData,file)
			return assetData['id']

	def update_poe(self,asset_id,updated_metadata):
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

 	def query_poe(self,asset_id):
 		res = util.query_poe(asset_id)
 		return res

 	def issue_token(self,asset_id,amount):
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

 	def transfer_token(self,amount,from_id,to_id,token_id):
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
 	 	# data = {}
 	 	# with open(asset_id+'.json','r') as file:
 	 	# 	data = json.load(file)
		params = {
		 	'creator':constant.ent_sign_param['creator'],
		 	'created':str(int(time.time())),
		 	'nonce':constant.ent_sign_param['nonce'],
		 	'privateB64':'M3RcT8XVeeQ692vmGevnKvIjdo4UBVdSCJIXnZlnHZZUdfantXzz8aQyTi1b7KJQcbSYJYzMo6nNVssiMwx9EQ==',
		 	'payload':payload
		}
 	 	header = {"Bc-Invoke-Mode": "sync"}
 	 	constant.walletClient.transfer_colored_tokens(header, payload, params)

 	def query_wallet_balance(self,wallet_id):
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



			

		
