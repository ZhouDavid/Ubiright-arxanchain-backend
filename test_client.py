import requests
ip = 'http://ec2-34-212-135-27.us-west-2.compute.amazonaws.com'
############# register a new user ##################
data = {'username':'pigeon3','password':'Ubiright2018','usertype':'Person'}
r = requests.post(ip+':5000/user_register',json=data)
print(r.text) # responsed user_id, store it locally for future query

############# create a new asset ###################
# data = {'userid':'did:axn:983c0a6a-82d0-4ed9-ae80-d362140a4758','assetname':"David's Winter"}
# r = requests.post(ip+':5000/create_asset',json=data)
# print(r.text) # responsed asset_id, store it locally for future_query

# ############ query asset info ######################
# payload = {'assetid':'did:axn:93d0151e-8e98-4890-845f-86f65858d514'}
# r = requests.get(ip+':5000/query_asset',params=payload)
# print(r.text) # a json object that contains all basic info for this asset


