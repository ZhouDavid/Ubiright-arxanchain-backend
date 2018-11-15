# Ubiright-arxanchain-backend
This is a temporary blockchain-backend repo of Ubiright for the First Blockchain Competition of Chinese University 
## Sample Usage
```python
import requests
ip = 'http://ec2-34-212-135-27.us-west-2.compute.amazonaws.com'
port = '5000'

############# register a new user ##################
data = {'username':'gix_ubiright3','password':'Ubiright2018','usertype':'Person'} # password must contain at least one lower case, upper case letter and digits with minimum length of 9
r = requests.post(ip+':'+port+'/user_register',json=data)
print(r.text) # responsed user_id, store it locally for future query

user_id1 = str(r.text)
data = {'username':'gix_ubiright4','password':'Ubiright2018','usertype':'Person'} # password must contain at least one lower case, upper case letter and digits with minimum length of 9
r = requests.post(ip+':'+port+'/user_register',json=data)
print(r.text) # responsed user_id, store it locally for future query
user_id2 = str(r.text)
user_id1 = 'did:axn:3fdd8d2b-13bf-467a-a021-120f139adec9'
user_id2 = 'did:axn:8ab48979-ca29-441b-9063-c10515d367da'


############# create a new asset ###################
data = {'user_id':user_id2,'asset_name':"David's Winter"}
r = requests.post(ip+':'+port+'/create_asset',json=data)
print(r.text) # responsed asset_id, store it locally for future_query
asset_id1_1 = str(r.text)


# ############## query asset info ######################
payload = {'asset_id':asset_id1_1}
r = requests.get(ip+':'+port+'/query_asset',params=payload)
print(r.text) # a json object that contains all basic info for this asset



############## issue coins ###########################
user_id = user_id1
data = {'user_id':user_id,'amount':200} # amount must be non-negative integer
r = requests.post(ip+':'+port+'/issue_coins',json=data)
print(r.text) # valid token_id if succeeded or -1 if failed



# ############## transfer coins ########################

from_id = user_id1
to_id = user_id2

data = {'from_id':from_id,'to_id':to_id,'amount':43} # amount must be non-negative integer
r = requests.post(ip+':'+port+'/transfer_coins',json=data)
print(r.text) # transaction info



############## query wallet balance ##################
payload = {'user_id':to_id}
r = requests.get(ip+':'+port+'/query_balance',params=payload)
print(r.text) # integer




