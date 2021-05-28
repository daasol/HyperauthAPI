# HyperauthAPI
Hyperauth API (user delete)


# Hperauth user delete 가이드 

Hyperauth의 API를 사용하여 사용자를 삭제하려면 삭제하려는 사용자의 token이 있어야한다. 
이 token을 얻는 방법에는 두가지 방법이 있다. 
  1. Admin 또는 view-users 권한으로 token을 얻어와 삭제
  2. User 자신의 권한으로 token을 얻어와 삭제


### 삭제 하기 전 알아야 할 용어 세가지

1. Realm : authentication resource의 그룹
   ex)tmax 또는 master 
2. client : 인증 기능을 사용할 응용프로그램이 사용하는 auth의 group
   ex) wapl-jmeter, wapl-spec, demo 등등…
3. token : 사용자 정보를 update하거나 delete 할 때 세션 만료 전까지 갖는 값

## User delete

### 첫번째 방법 (Admin, view-users 권한)
  *주의* ! 
    해당 방법은 auth 설정마다 될 때도 있고 안 될 때도 있어서 두번째 방법을 권장함

순서 
1. Admin 또는 view-users권한으로 token 을 얻어온다.
2. 얻어온 token으로 특정 client의 유저 리스트를 얻어온다 .
3. 유저 리스트를 얻어올 때 유저의 고유 token을 함께 가져올 수 있다. 
4. 이후, 유저 delete는 두번째 방법의 delete와 같다.


### 두번째 방법 (사용자 자신의 권한으로 token얻어오기)
   *주의* ! 
    사용자가 자신의 권한으로 token을 얻어와서 delete, update하기 때문에 password를 알고 있어야함
    유저가 속한 클라이언트의 realm이 무엇인지 알아야함

순서 
1. auth에 유저가 등록된 client_id로 username과 password를 Body에 넣어 POST
2. POST결과로 얻을 수 있는 access_token을 user_name과함께 DELETE

        realm, client info => realms : tmax, client_id : hyperspace
        user info => user_name : abcdefg2@tmax.co.kr, password : qwer1234!


        POST : https://{auth_ip:port}/auth/realms/tmax/protocol/openid-connect/token
            Headers => Content-Type : application/x-www-form-urlencoded
            Body 
            grant_type :  password	
            username : abcdefg2@tmax.co.kr
            password : qwer1234!
            client_id  : wapl-jmter (삭제할 유저가 속한 client name)
      
access_token을 얻을 수 있음

      DELETE https://{auth_ip:port}/auth/realms/tmax/user/{user_name}
          QueryParam => token : {Access Token}  (해당 토큰은 앞서 POST로 사용자 자신의 권한으로 받아온 token)
       
3. 결과 : User [abcdefg2@tmax.co.kr] Delete Success 


Realm이 tmax가 아닌 master라면 URL을 다음과 같이 입력한다.
https://{}/auth/realms/master/protocol/openid-connect/token
