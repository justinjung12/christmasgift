from flask import Flask,render_template,request,redirect
from flask_cors import CORS
from datetime import datetime
import random
#마지막 해야할일:크리스마스때만 열리게하기,cors설정,localstorage에 이름 저장하는거 암호화
app = Flask(__name__)
CORS(app)

users = [{'id':'w','pw':'w'}] #유저의 id,pw저장
gifts = [ {'id':'w','givegift':['1','2','3','4','5','6'],'receivedgift':[{'giveusername':'wj','giftrate':1,'content':'hi','gift':''}]} ] #유저의 받은 선물의 딕셔너리,줄 용도의 선물의 등급의 list 저장
opengift = []
def givegiftgrade():
    global giftgrade
    giftgrade = []
    for x in range(0,random.randint(3,6)):
        n = random.randint(0,100)
        if(n in range(0,5)):
            giftgrade.append('1')
        elif(n in range(5,15)):
            giftgrade.append('2')
        elif(n in range(15,30)):
            giftgrade.append('3')
        elif(n in range(30,50)):
            giftgrade.append('4')
        elif(n in range(50,75)):
            giftgrade.append('5')
        elif(n in range(75,100)):
            giftgrade.append('6')

price = 0
def choosegift(grade):
    rn1 = random.randint(0,grade+1)
    rn2 = random.randint(0,grade)
    global price
    if(rn1 == rn2):
        g1n = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,31,32,33]
        g2n = [21,22,23,24,25,26,27,28,29,30]
        g3n = [34,35,36,37,38,39,40]
        g4n = [41,42,43,44,45]
        g5n = [46,47,48,49]
        g6n = [50]

        rn3 = random.randint(0,50)

        if(rn3 in g1n):
            price += 300
            return '츄팝춥스'
        elif(rn3 in g2n):
            price += 1000
            return '비타 500'
        elif(rn3 in g3n):
            price += 1000
            return '다이소상품권1000'
        elif(rn3 in g4n):
            price += 1800
            return '바나나우유'
        elif(rn3 in g5n):
            price += 3000
            return 'cu모바일상품권'
        elif(rn3 in g6n):
            price += 3900
            return '싱글레귤러'
    else:
        return '꽝'




@app.route('/',methods=['GET','POST']) #처음 들어왔을때
def index():
    if request.method == 'GET': #링크를 치고 들어왔을때
        return render_template('signup.html')
    elif request.method == 'POST': #POST로 요청이 들어올때
        if(request.form['button'] == 'signup'):#회원가입이면
            return render_template('signup.html')


@app.route('/mypage') #mypage로 들어왔을때
def mypage():
    return render_template('mypage.html')



# @app.route('/login',methods=['GET','POST']) #로그인
# def login():
    
#     if request.method == 'POST': #POST로 요청이 들어왔을때
#         user_id = request.form['id']
#         user_pw = request.form['pw']
#         print(user_id,user_pw)
#         for index,value in enumerate(users): 
#             if(users[index]['id'] == str(user_id) and users[index]['pw'] == str(user_pw)): #id,비번이 users안에 들어있으면
#                 return redirect('/mypage')
#             else:
#                 return redirect('/')
#         return 'error'
@app.route('/signup',methods=['GET','POST']) #회원가입
def signup():
    if request.method == 'POST': #POST로 요청이 들어왔을때
        #먼저 signupinfo,gift에 값 저장후 최종 리스트에 저장
        signupinfo = {}
        gift = {}

        givegiftgrade()
        #users에 값 추가
        print(request)
        signupinfo['id'] = request.form['id']
        signupinfo['pw'] = request.form['pw']
        users.append(signupinfo)
        #gifts값 처음 지정하기
        gift['id'] = request.form['id']
        gift['givegift'] = giftgrade
        gift['receivedgift'] = []
        gifts.append(gift)
        return redirect('/mypage')

@app.route('/signupnoreturn',methods=['POST']) #회원가입
def signupnr():
    if request.method == 'POST': #POST로 요청이 들어왔을때
        #먼저 signupinfo,gift에 값 저장후 최종 리스트에 저장
        signupinfo = {}
        gift = {}

        givegiftgrade()
        #users에 값 추가
        print(request)
        signupinfo['id'] = request.get_json()['id']
        signupinfo['pw'] = request.get_json()['pw']
        users.append(signupinfo)
        #gifts값 처음 지정하기
        gift['id'] = request.get_json()['id']
        gift['givegift'] = giftgrade
        gift['receivedgift'] = []
        gifts.append(gift)
        print("아")
        return{'statue':'Ok'} 

@app.route('/checkreceivedgifts/',methods=['GET','POST']) #받은 선물확인
def checkreceivedgifts():
    
    if request.method == 'POST': #POST요청이면
        for index,value in enumerate(gifts): #요청된 user name값이랑 gifts리스트 id에서 일치되는게 있으면 그 username에 해당되는 receivedgift값 반환
            if(gifts[index]['id'] == request.get_json()['username']):
                print(gifts[index]['receivedgift'])
                return gifts[index]['receivedgift']
            print(gifts[index]['id'],request.get_json()['username'])
    return 'error'


@app.route('/openreceivedgifts/',methods=['GET','POST']) #받은 선물을 열때
def openreceivedgifts():
    if request.method == 'POST': #만약 POST라면
        print("post")
        now = datetime.now()

        if(True): #12월 25일날 열 수 있게 하기
            gift = request.get_json()['giftindex'].split('.')#0:rate,1:giveusername
            for index,value in enumerate(gifts):
                if(gifts[index]['id'] == request.get_json()['username']): #요청된 user name값이랑 gifts리스트 id에서 일치되는게 있으면 =
                    List = gifts[index]['receivedgift']

                    for i,v in enumerate(List): #receivedgift 안 값
                        if v['giveusername'] == gift[1]: #만약 receivegift안 값이 보낸 giveusername과 같다면
                            giftn = v['gift']
                            del List[i]
                            return{'gift':giftn} 
            return'no'
        else:
            return '크리스마스가 아닙니다'
    return 'error'

@app.route('/givegifts/<receivingusername>',methods=['GET','POST']) #링크를 타고 다른사람에게 선물 보내기
def givegifts(receivingusername):
    if request.method == 'POST':
        for index,value in enumerate(gifts):
            if(gifts[index]['id'] == receivingusername): #받는 사람의 이름의 receivedgift 값 수정
                giftgive = {}
                
                giftgive['giftrate']=request.get_json()['rate']
                giftgive['giveusername'] = request.get_json()['writtenusername']
                giftgive['content'] = request.get_json()['content']
                giftgive['gift'] = choosegift(int(giftgive['giftrate']))
                gifts[index]['receivedgift'].append(giftgive)
                
                for index,value in enumerate(gifts): #준사람 givegift 값 지우기
                    if(gifts[index]['id'] == request.get_json()['username']):
                        print(request.get_json()['rate'],gifts[index]['givegift'])
                        gifts[index]['givegift'].remove(request.get_json()['rate'])
 
                return {'finish':True}

        return 'error'
    elif request.method == 'GET': #만약 링크를 타고 들어오면
        return render_template('givegift.html',receivingusername = receivingusername)




@app.route('/checkgivegifts/',methods=['GET','POST'])
def checkgivegifts():
    if request.method == 'POST':
        for index,value in enumerate(gifts):
            if(gifts[index]['id'] == request.get_json()['username']):
                print(gifts[index]['givegift'])
                return gifts[index]['givegift']
            


    return 'error'


@app.route('/admin/wj',methods=['GET','POST'])
def admin():
    print(users,gifts,opengift)
    return {'users':users,'gifts':gifts,'opengift':opengift}

@app.route('/saveopen',methods=['POST'])
def saveopen():
    print(request.get_json())
    opengift.append(request.get_json())
    return gifts

@app.route('/giveuser',methods=['POST'])
def giveuser():
    data = []
    for index,value in enumerate(gifts):
        if(gifts[index]['id'] == request.get_json()['username']):
            data.append(gifts[index]['receivedgift'])

    return data
