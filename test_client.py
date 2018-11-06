import requests
ip = 'http://ec2-34-212-135-27.us-west-2.compute.amazonaws.com'
############# register a new user ##################
# data = {'username':'davidhehe','password':'Ubiright2018','usertype':'Person'}
# r = requests.post(ip+':5000/user_register',json=data)
# print(r.text) # responsed user_id, store it locally for future query

############# create a new asset ###################
data = {'userid':'did:axn:282c31d1-26c6-444e-8d78-79968818f4e8','assetname':"Bob's spring"}
r = requests.post(ip+':5000/create_asset',json=data)
print(r.text) # responsed asset_id, store it locally for future_query

# ############ query asset info ######################
# payload = {'assetid':'did:axn:cd1a2d9e-faa0-4951-9fef-392dcec158a9'}
# r = requests.get(ip+':5000/query_asset',params=payload)
# print(r.text) # a json object that contains all basic info for this asset