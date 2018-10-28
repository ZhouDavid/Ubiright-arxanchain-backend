# Ubiright-arxanchain-backend
This is a temporary blockchain-backend repo of Ubiright for the First Blockchain Competition of Chinese University 
## Sample Usage
```python
import requests
############# register a new user ##################
data = {'username':'ubiright_david','password':'Ubiright2018','usertype':'Person'}
r = requests.post('http://10.155.236.124:5000/user_register',json=data)
print(r.text) # responsed user_id, store it locally for future query

############# create a new asset ###################
data = {'userid':'did:axn:282c31d1-26c6-444e-8d78-79968818f4e8','assetname':"Bob's spring"}
r = requests.post('http://10.155.236.124:5000/create_asset',json=data)
print(r.text) # responsed asset_id, store it locally for future_query

############ query asset info ######################
payload = {'assetid':'did:axn:cd1a2d9e-faa0-4951-9fef-392dcec158a9'}
r = requests.get('http://10.155.236.124:5000/query_asset',params=payload)
print(r.json()) # a json object that contains all basic info for this asset
```
