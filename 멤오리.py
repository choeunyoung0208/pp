import socket                                          # Python과 Arduino간의 소켓 통신을 위해 socket 모듈 사용

# 소켓 객체를 생성
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '192.168.43.237'                                # 서버의 주소 (아두이노쪽의 주소)
PORT = 12345                                           # 서버에서 (우리가 임의로) 지정해 놓은 포트 번호

client_socket.connect((HOST, PORT))                    # 지정한 HOST와 PORT를 사용하여 서버에 접속

prov_list = [ {'name':'Daegu','city_id':'1835329'} ]

import requests                                        # 웹 데이터 파싱(웹에서 데이터를 받아온다고 생각하면 됨!)을 하기 위해 requests 모듈 사용

url = 'http://api.openweathermap.org/data/2.5/weather' # 데이터를 받아올 웹 주소(현재 날씨 데이터를 받아올 수 있는 openweathermap 사이트 사용)

weather_info_list = []

for i in range(len(prov_list)):                       # prov_list 라는 리스트에 저장된 요소의 개수만큼 반복
    city_id = prov_list[i]['city_id']
    city_name = prov_list[i]['name']
    params = dict(                                   
        id=city_id,
        APPID='f1a51f91206c5673b65a1854d89949b8',     # 위의 url에서 날씨 데이터를 불러오기 위해 필요한 API key. 직접 발급 받음.
                                                      # API(Application Programming Interface) : 어떤 응용 프로그램에서 데이터를 주고 받기 위한 규칙들
    )
    resp = requests.get(url=url, params=params)       # 해당 url에 접속하면 열리는 html의 소스코드에서 원하는 데이터를 resp에 저장
    data = resp.json()                                # .json()을 활용해 딕셔너리 형태로 데이터 저장
    
    if(data['cod'] == 429):                           # blocking error code
        break
    data_main = data['main']
    data_zero = data['weather']
    data_id = data_zero[0]
    info = [
        city_id,
        city_name,
        data_id['id']]
    weather_info_list.append(info)                  # weather_info_list에 info에 저장된 데이터들을 추가한다

import pandas as pd                                 # weather_info_list에 저장된 데이터를 보기좋게 정리하기 위해 pandas 라이브러리 사용

# weather_info_list에 저장된 데이터를 city_id, city_name, id 라는 세 개의 열을 가지는 2차원 배열로 만듦(표 형태로 구성하려고 사용함)
df = pd.DataFrame(weather_info_list, columns=['city_id', 'city_name','id'])

print(df) 
# print(df) 결과 출력되는 것
# 1행 : city_id  city_name  id
# 2행 : 1835329    Daegu  현재 대구의 날씨를 알 수 있는 id 값

a = df['id']                                       # 현재 대구의 날씨를 알 수 있는 id 값이 포함되어 있는 부분을 추출
b = str(a[0])                                      # a의 첫번째 요소에 현재 대구의 날씨를 알 수 있는 id 값이 저장되어 있어 a[0]을 문자열로 형변환

client_socket.sendall(b.encode())                  # 문자열로 b에 저장되어있는 데이터 송신. 서버(수신단)에서 이 값을 받고 정수형으로 다시 변환 할 예정.

# 소켓을 닫음
client_socket.close()