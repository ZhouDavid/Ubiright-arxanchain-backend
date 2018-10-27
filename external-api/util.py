import requests
import constant
import time
import json

def query_poe(asset_id):
	"""
	return a result dict,query the balance of poe
	"""
	headers = {'API-Key':constant.apikey,"Bc-Invoke-Mode": "sync"}
	res  = constant.walletClient.query_poe(headers,asset_id)
	return json.loads(str(res[1]['Payload']))
	
def coinsQuery(wallet_id):
	"""
	query balance of coins
	"""
	res = constant.walletClient.query_wallet_balance({},wallet_id)
	return res

def poeTransfer(account,from_id,to_id,asset_ids):
	payloads = {
	   "callback_url": "http://url-to-notify",
	   "from":from_Id,
	   "to": to_id,
	   "assets": asset_ids
	}
	res = constant.walletClient.transfer_assets({},payloads)
	return res[1]

def coinsTransfer(from_id,to_id,asset_id,tokens,amount):
	payload = {
		"from":from_id,
		"to":to_id,
		"asset_id":asset_id,
		"tokens":tokens,
		"fee":{
			amount:amount
		}
	}
	params = {
		"creator":constant.ent_sign_param['creator'],
		"created":str(int(time.time())),
		"nonce":"nonce",
		"privateB64":constant.ent_sign_param['privateB64'],
		"payload":payload
	}
	_,resp = constant.walletClient.transfer_colored_tokens({},payload,params)
	return resp

def queryTransactionLog(wallet_id,num,page):
	_, resp = constant.walletClient.get_tx_logs({}, wallet_id, tx_type, num, page)
	return resp


# if __name__ == '__main__':
	# assetId = 'did:axn:a2ec21c0-c6d7-45b9-8503-2df640a80ac5'
	# url = constant.ip_addr+"/wallet-ng/v1/poe?id={}".format('did:axn:a2ec21c0-c6d7-45b9-8503-2df640a80ac5')
	# headers = {'API-Key':constant.apikey,"Bc-Invoke-Mode": "sync"}
	# # res = requests.get(url,headers=headers)
	# res = constant.walletClient.query_poe(headers,assetId)
	# print type(res[1])

	# wallet_id = 'did:axn:bcaad1cb-e1f2-415b-b110-1fb4da5a08a2'
	# res = coinsQuery(wallet_id)
	# print res