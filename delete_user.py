import json
import requests
import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #ssl 사용하지 않음 , verify=False 

## NOTI ##



#auth info
    #IP => auth domain name 
    #   ex :  "192.168.158.120:3121" or "demoauth.com" 
    #client_id => auth client name 
    #   ex : hyperspace or wapl-jmeter or demo ... 
IP=""
client_id =""

#user info
user_list_path="D:/TMAX/cnu/auth_delete/delete_user_list.txt"
password="Qwer1234!"



def read_user_list() -> list : 
    user_list = []
    file = open(user_list_path, 'r')
    while True:
        line = file.readline()
        line=line.rstrip('\n')
        user_list.append(line)
        if not line: break
    file.close()
    return user_list    


def get_mytoken(user_id:str) -> str :
    URL = "https://{}/auth/realms/tmax/protocol/openid-connect/token".format(IP)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  
    data = {"grant_type"  : "password",
            "username"  : user_id , 
            "password"  : password,  
            "client_id"  : client_id}
    
    res = requests.post(URL, headers=headers, verify=False ,data=data)
    res_json = res.json()
    
    if res.status_code == 200:
        res_json = res.json()
        if 'access_token' in res_json.keys():
            return res_json['access_token']
        return ''
    else : 
        print("no token") 
        return ''


def delete_user(user_data:list) :
    for i in range(len(user_data)) :
        ## NOTI ##
        # users_data[i][0], user_data[i][1] => user_id, user_token
        user_id=user_data[i][0]
        user_token=user_data[i][1]
        HYPERAUTH_URL = "https://{}/auth/realms/tmax/user/{}?token={}".format(IP, user_id,user_token)

        try:                           
            response = requests.delete(url=HYPERAUTH_URL, verify=False)
            if response.ok == True :
                print('delete success >> {} '.format(user_id))
        except Exception as e :
            print(e)



if __name__ == "__main__":
    users = read_user_list()   #파일로부터 user_id를 하나씩 가져와서 list 생성 
    token = "" 
    user_data = [] # [user_id : token] 형태의 list 생성
    
    for user in users : 
        token = get_mytoken(user)
        user_data.append([user, token]) # user_data = [[user1_id, user1_token],[user2_id, user2_token], ...]
        
    delete_user(user_data) #dlfr
    print("--finish--")
    