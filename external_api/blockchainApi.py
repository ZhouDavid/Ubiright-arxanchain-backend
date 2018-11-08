import os
import constant
import json
import ast
import time
import base64
import pandas as pd

user_data_path = './user_data/'
asset_data_path = './asset_data/'
user2asset_path = './user2asset/'
def __handleResponse__(username,register_info):
	'''
	:param username: string, self-defined 
	:param register_info: unicode json, info get from user_register 
	:return: string, user_id get from arxan official blockchain server
	'''
	data = json.loads(str(register_info['Payload']))
	data['username'] = username
	with open(user_data_path+data['id']+'.json','w') as file:
		json.dump(data,file)
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
	_,info = constant.walletClient.register(header,body)
	if info['Payload']==None:
		return str(info)
	return __handleResponse__(username,info)

def create_poe(user_id,assetName):
	'''
	:param user_id: string, user_id got from arxahin official blockchain server
	:param assetName: string, article name created by user
	:return: 
	'''
	user_data = None
	if not os.path.exists(user_data_path+user_id+'.json'):  # judge whether user_id is valid
		return '400'
	with open(user_data_path+user_id+'.json','r') as file:
		user_data = file.read()  # open pre_stored user data named with user_id
	user_data = ast.literal_eval(user_data)
	metadata = base64.b64encode(str({'count':0,'coins_earned':0,'modified_time':[]}))  # initial number of read and coins eared should both be zero
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
	header = {"Bc-Invoke-Mode": "sync"}
	_, response = constant.walletClient.create_poe(header, payload, params)
	if response['Payload']==None:
		return '-1'
	assetData = json.loads(str(response['Payload']))
	assetData['creator'] = constant.ent_sign_param['creator']
	assetData['owner'] = wallet_id
	assetData['name'] = assetName
	assetData['metadata'] = metadata
	assetData['privateB64'] = private_key_base64
	assetData['created'] = created_time
	with open(asset_data_path+assetData['id']+'.json','w') as file:    # wirte asset data to json file name wit asset_id
		json.dump(assetData,file)
	with open(user2asset_path+user_id+'.csv','a') as file:
		record = ",".join([user_id,assetData['id'],'-1','-1'])+'\n'
		file.write(record)

	return assetData['id']

def update_poe(asset_id,updated_metadata):
	data = {}
	status_code = 200
	try:
		with open(asset_data_path+asset_id+'.json','r') as file:
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
	header = {"Bc-Invoke-Mode": "sync"}
	time,res = constant.walletClient.query_poe(header,asset_id)
	res = json.loads(str(res['Payload']))
	res['metadata'] = base64.b64decode(res['metadata'])
	return res

def issue_token(asset_id,amount):
	data = {}
	status_code = 200
	token_id = -1
	try:
		with open(asset_data_path+asset_id+'.json','r') as file:
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

def transfer_token(from_id,to_id,tokens):
	with open(user_data_path+from_id+'.json','r') as file:
		data = json.load(file)
		privateB64 = data['key_pair']['private_key']
		try:
			payload = {
				'from':from_id,
				'to':to_id,
				'asset_id':"",
				'tokens':tokens
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
 	_,balance_info = constant.walletClient.query_wallet_balance(header,wallet_id)
 	balance_info = json.loads(str(balance_info['Payload']))
	balance_info = balance_info['colored_tokens']
	balance = 0
	for k,v in balance_info.items():
		balance+=v['amount']
 	return balance
			
def issue_coins(user_id,amount):
	filename = user2asset_path+user_id+'.csv'
	aid = '400'
	token_id = '-1'
	if not os.path.isfile(filename):
		aid = create_poe(user_id,'issue token')
		if aid.startswith('did'):
			f = open(filename,'w')
			f.write(','.join(['user_id','asset_id','token_id','amount'])+'\n')
			f.write(','.join([user_id,aid,'-1','-1'])+'\n')
			f.close()
		else:
			return '-1'

	df = pd.read_csv(filename)
	for i in range(df.shape[0]):
		if df.iloc[i,2]=='-1':
			aid = df.iloc[i,1]
			status,token_id = issue_token(aid,amount)
			df.iloc[i,2]=str(token_id)
			df.iloc[i,3]=float(amount)
			df.to_csv(filename,index=False)
			return token_id

	aid = create_poe(user_id,'issue token')
	status,token_id = issue_token(aid,amount)
	df.loc[df.shape[0]]=[user_id,aid,token_id,amount]
	df.to_csv(filename,index=False)
	
	return token_id

def transfer_coins(from_id,to_id,amount):
	header = {"Bc-Invoke-Mode": "sync"}
	_,balance_info = constant.walletClient.query_wallet_balance(header,from_id)
	balance_info = json.loads(str(balance_info['Payload']))
	balance_info = balance_info['colored_tokens']
	balance = 0
	for k,v in balance_info.items():
		balance+=v['amount']
	if balance<amount:
		return 'insufficient balance'
	tokens = list()
	for k,v in balance_info.items():
		if v['amount']<=amount:
			tokens.append({'token_id':k,'amount':v['amount']})
			amount-=v['amount']
		else:
			if amount!=0:
				tokens.append({'token_id':k,'amount':amount})
			break
	info = transfer_token(from_id,to_id,tokens)
	return info

if __name__ == '__main__':
	####### register a new user############
	# user_name = 'David Zhou'
	# password = 'Zhoujy123'
	# utype="Person"
	# user_id1 = user_register(user_name,password,utype)
	# print(user_name+' registered successfully, id:{}'.format(user_id1))

	# user_name = 'Bob Tian'
	# password = 'Tianz123'
	# user_id2 = user_register(user_name,password,utype)
	# print(user_name+' registered successfully, id:{}'.format(user_id2))
	

	# print('user_id1:{}'.format(user_id1))
	# print('user_id2:{}'.format(user_id2))


	##### issue coins ###############
	# amount = 200
	# token_id = issue_coins(user_id1,amount)

	user_id1 = 'did:axn:922a1f92-b6f2-4280-a6e4-15683d81d00b'
	user_id2 = 'did:axn:67f9ee8a-46cc-4928-80ba-dcdfa43642c5'
	# ##### query blalance#############
	# info = query_wallet_balance(user_id1)
	# print('-----------user_id1 balance--------------')
	# print(info)
	# info = query_wallet_balance(user_id2)
	# print('-----------user_id2 balance--------------')
	# print(info)

	##### transfer coins ############
	amount = 8
	info = transfer_coins(user_id1,user_id2,amount)
	print('----------transfer info---------------')
	print(info)

	info = query_wallet_balance(user_id1)
	print('-----------user_id1 balance--------------')
	print(info)
	info = query_wallet_balance(user_id2)
	print('-----------user_id2 balance--------------')
	print(info)
