import requests
ip = 'http://ec2-34-212-135-27.us-west-2.compute.amazonaws.com'
port = '5000'

# ############# register a new user ##################
data = {'username':'gix_ubiright','password':'Ubiright2018','usertype':'Person'} # password must contain at least one lower case, upper case letter and digits with minimum length of 9
r = requests.post(ip+':'+port+'/user_register',json=data)
print(r.text) # responsed user_id, store it locally for future query

# # ############# create a new asset ###################
data = {'user_id':'did:axn:983c0a6a-82d0-4ed9-ae80-d362140a4758','assetname':"David's Winter"}
r = requests.post(ip+':'+port+'/create_asset',json=data)
print(r.text) # responsed asset_id, store it locally for future_query



# ############## query asset info ######################
payload = {'asset_id':'did:axn:93d0151e-8e98-4890-845f-86f65858d514'}
r = requests.get(ip+':'+port+'/query_asset',params=payload)
print(r.text) # a json object that contains all basic info for this asset



# # ############## issue coins ###########################
user_id = 'did:axn:67f9ee8a-46cc-4928-80ba-dcdfa43642c5'
data = {'user_id':user_id,'amount':100} # amount must be non-negative integer
r = requests.post(ip+':'+port+'/issue_coins',json=data)
print(r.text) # valid token_id if succeeded or -1 if failed



# ############## transfer coins ########################

from_id = 'did:axn:922a1f92-b6f2-4280-a6e4-15683d81d00b'
to_id = 'did:axn:67f9ee8a-46cc-4928-80ba-dcdfa43642c5'

data = {'from_id':from_id,'to_id':to_id,'amount':100} # amount must be non-negative integer
r = requests.post(ip+':'+port+'/transfer_coins',json=data)
print(r.text) # transaction info



############## query wallet balance ##################
payload = {'user_id':'did:axn:67f9ee8a-46cc-4928-80ba-dcdfa43642c5'}
r = requests.get(ip+':'+port+'/query_balance',params=payload)
print(r.text) # integer




