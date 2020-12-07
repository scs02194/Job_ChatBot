from telepot.loop import MessageLoop
import requests, time, telegram,os,webbrowser,threading,time,telepot
from win10toast import ToastNotifier
from bs4 import BeautifulSoup
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from concurrent.futures import ThreadPoolExecutor
Clients = []
Client_IDs = []
lock = threading.Lock()
TOKEN_MAIN = '1426305686:AAG6IVScYx78khVSnHT4w3myF6ORwTwJskc'
class Client:
    def __init__(self,argu_chat_ID):
        self.chat_ID = argu_chat_ID
        self.Stop_Flag = 1
        self.Main_Thread = threading.Thread(target=self.both_Run,args=(self.chat_ID,))
        self.want_normal_jobcode = []
        self.want_normal_company_type = []
        self.want_normal_region_Code = []
        self.want_normal_career_Code = []
        self.want_open_company_type = []
        self.normal_jobcode_name = []
        self.normal_regionCode_Name = []
        self.normal_Company_Type_Name = []
        self.normal_Career_Name = []
        self.open_Company_Type_Name = []
        self.want_open_career_Code=[]
        self.Msg_IDs = []
        self.target_alarm = "일반/공채 모두 알람"

    normal_Company_Type_Dic = {'01':'대기업','03':'벤처기업','04':'공공기관','05':'외국계기업','09':'청년친화강소기업'}
    open_Company_Type_Dic = {'10':'대기업','20':'공기업','30':'공공기관','40':'중견기업','50':'외국계기업'}
    def open_Stringappend(self,title,companyname,closedate,wantedtype,url):

        appendedstring = "[공개채용알림]" + '\n' + '<' + title +'>'+'~'+closedate +"까지"+'\n' + "회사명 : " + companyname + '\n' + "채용 형태 : " + wantedtype + '\n' + url

        return appendedstring
    def sendTelegramMessage(self,t_ID,Message):
        tele_toekn = "1426305686:AAG6IVScYx78khVSnHT4w3myF6ORwTwJskc"
        bot =  telegram.Bot(token = tele_toekn)
        #updates = bot.get_updates()
        telegram_id = t_ID
        bot.sendMessage(telegram_id, Message)
    def open_Chaeyong_Run(self,t_ID) :
        while self.Stop_Flag == 1:
            beforeurl = "http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=1&coClcd="
            for value in self.want_open_company_type:
                beforeurl = beforeurl + value + '|'

            beforeurl += "&empWantedCareerCd="

            for value in self.want_open_career_Code:
                beforeurl = beforeurl + value +'|'
            print('before url :',beforeurl)
            r = requests.get(beforeurl)
            html = r.text
            soup = BeautifulSoup(html,'html.parser')
            values = soup.find_all('dhsopenempinfo')
            if len(values)>0:
                before_top_wanted = values[0].select("empwantedtitle")[0].get_text()
                #toaster = ToastNotifier()
                while self.Stop_Flag == 1:
                    print()
                    print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ채용 알리미 봇ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
                    print('알림설정된 기업(공개채용) : ',self.open_Company_Type_Name)
                    print('신입/경력 (공개채용) : ',self.normal_Career_Name)
                    print('chat_ID : ',t_ID)
                    
                    nowurl = "http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=50&coClcd="
                    for value in self.want_open_company_type:
                        nowurl = nowurl + value + '|'

                    nowurl += "&empWantedCareerCd="
                    for value in self.want_open_career_Code:
                        nowurl = nowurl +value+'|'
                    r = requests.get(nowurl)
                    html = r.text
                    soup = BeautifulSoup(html,'html.parser')
                    values = soup.find_all('dhsopenempinfo')
                    print('nowurl : ',nowurl)
                    if len(values)>0:
                        for value in values:
                            now_top_wanted = value.select("empwantedtitle")[0].get_text()
                            if now_top_wanted != before_top_wanted:
                                companyname = value.select("empbusinm")[0].get_text()
                                title = value.select("empwantedtitle")[0].get_text()
                                closedate = value.select("empwantedendt")[0].get_text()
                                url = value.select("empwantedhomepgdetail")[0].get_text()
                                wantedtype = value.select("empwantedtypenm")[0].get_text()
                                #iconurl = ''
                                #if len(value.select("reglogimgnm"))>0:
                                #    iconurl = value.select("reglogimgnm")[0].get_text()
                                appendedstring = self.open_Stringappend(title,companyname,closedate,wantedtype,url)
                                print('공개채용 공지 게시 <',title,'>',',',companyname)
                                self.sendTelegramMessage(t_ID,appendedstring)
                                print('텔레그램 전송 완료.')
                                #toaster.show_toast('[공개채용]'+companyname,now_top_wanted,duration=10,callback_on_click=lambda: self.open_Browser(url),icon_path=iconurl)
                            else :
                                print('새로운 공개채용정보가 없습니다.')
                                break
                            if self.Stop_Flag != 1 :
                                break
                        before_top_wanted = values[0].select("empwantedtitle")[0].get_text()
                    print('가장 최신 공지 :',before_top_wanted)
                    print('새로운 공개채용정보 요청중')
                    for i in range(5):
                        if self.Stop_Flag == 1:
                            time.sleep(1)   
            else :
                print('새로운 공개채용정보가 없습니다.')
                for i in range(5):
                    if self.Stop_Flag == 1:
                        time.sleep(1)   
            print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')    
    def all_chaeyong_Run(self,t_ID):

        while self.Stop_Flag == 1 :
            beforeurl = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=1&occupation="

            for value in self.want_normal_jobcode:
                beforeurl = beforeurl + value + '|'

            beforeurl = beforeurl + '&coTp='

            for value in self.want_normal_company_type:
                beforeurl = beforeurl + value + '|'

            beforeurl = beforeurl + '&region='

            for value in self.want_normal_region_Code:
                beforeurl = beforeurl + value + '|'
            
            if len(self.want_normal_career_Code) > 0 :
                    
                beforeurl = beforeurl + '&career='
                if self.want_normal_career_Code[0] == 'N':
                    beforeurl = beforeurl + 'N|Z'
                elif self.want_normal_career_Code[0] == 'E':
                    beforeurl = beforeurl + 'E&minCareerM=0'


            print('before url :',beforeurl)
            r = requests.get(beforeurl)
            html = r.text
            soup = BeautifulSoup(html,'html.parser')
            values = soup.find_all('wanted')
            if len(values)>0:    #채용정보가 한 개 이상일 경우
                before_top_wanted = values[0].select("title")[0].get_text()
                #toaster = ToastNotifier()
                while self.Stop_Flag == 1:
                    print()
                    print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ알림설정항목ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
                    if len(self.normal_jobcode_name) == 0 :
                        print('                                     알림설정된 직무(일반채용) : 모든 직무 알람')
                    else:
                        print('                                     알림설정된 직무(일반채용) : ',self.normal_jobcode_name)
                    if len(self.normal_regionCode_Name) == 0 :
                        print('                                     알림설정된 근무지(일반채용) : 모든 지역 알람')
                    else:
                        print('                                     알림설정된 근무지(일반채용) : ',self.normal_regionCode_Name)
                    if len(self.normal_Company_Type_Name) == 0 :
                        print('                                     알림설정된 기업분류(일반채용) : 모든 분류 알람')
                    else:
                        print('                                     알림설정된 기업분류(일반채용) : ',self.normal_Company_Type_Name)
                    if len(self.normal_Career_Name) == 0 :
                        print('                                     신입/경력 (일반채용) : 상관없음')
                    else:
                        print('                                     신입/경력 (일반채용) : ',self.normal_Career_Name)
                    print('                             chat_ID : ',t_ID)
                    
                    nowurl = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=50&occupation="

                    for value in self.want_normal_jobcode:
                            nowurl = nowurl + value + '|'

                    nowurl = nowurl + '&coTp='

                    for value in self.want_normal_company_type:
                        nowurl = nowurl + value + '|'

                    nowurl = nowurl + '&region='

                    for value in self.want_normal_region_Code:
                        nowurl = nowurl + value + '|'
                    
                    if len(self.want_normal_career_Code) > 0 :
                        nowurl = nowurl + '&career='
                        if self.want_normal_career_Code[0] == 'N':
                            nowurl = nowurl + 'N|Z'
                        elif self.want_normal_career_Code[0] == 'E':
                            nowurl = nowurl + 'E&minCareerM=0'
                            
                    print('nowurl : ',nowurl)
                    r = requests.get(nowurl)
                    html = r.text
                    soup = BeautifulSoup(html,'html.parser')
                    values = soup.find_all('wanted')
                    if len(values)>0:
                        for value in values:
                            now_top_wanted = value.select("title")[0].get_text()
                            if now_top_wanted != before_top_wanted:
                                companyname = value.select("company")[0].get_text()
                                title = value.select("title")[0].get_text()
                                salarytype = value.select("saltpnm")[0].get_text()
                                salary = value.select("sal")[0].get_text()
                                region = value.select("region")[0].get_text()
                                holiday = value.select("holidaytpnm")[0].get_text()
                                closedate = value.select("closedt")[0].get_text()
                                url = value.select("wantedmobileinfourl")[0].get_text()
                                school = value.select("minedubg")[0].get_text()
                                career = value.select("career")[0].get_text()
                                weburl = value.select("wantedinfourl")[0].get_text()
                                appendedstring = self.stringappend(companyname,title,salarytype,salary,region,holiday,closedate,url,school,career)
                                print('일반채용 공지 게시 <',title,'>',',',companyname)
                                self.sendTelegramMessage(t_ID,appendedstring)
                                print('텔레그램 알림 완료')
                                #toaster.show_toast('[일반채용]'+companyname,now_top_wanted,duration=10,callback_on_click=lambda: open_Browser(weburl))
                            else :
                                print('새로운 일반채용정보가 없습니다.')
                                print()
                                break
                            if self.Stop_Flag != 1:
                                break
                        before_top_wanted = values[0].select("title")[0].get_text()
                    print('가장 최신 공지 : ',before_top_wanted)
                    print()
                    print('새로운 일반채용정보 요청중')
                    print()
                    for i in range(5):
                        if self.Stop_Flag == 1:
                            time.sleep(1)   
            else : 
                print('새로운 채용정보를 찾을 수 없습니다.')
                for i in range(5):
                    if self.Stop_Flag == 1:
                        time.sleep(1)
            print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')      
    def stringappend(self,companyname,title,salarytype,salary,region,holiday,closedate,Url,school,career):
        appendedstring = "[일반채용알림]" + '\n' + '<' + title +'>'+'~'+closedate +"까지"+'\n' + "회사명 : " + companyname + '\n' +"경력 : "+career+'\n' +"임금 : " + salarytype + "," + salary + '\n' + "근무지 : " + region + '\n' + "학력 : " + school + '\n' + "근무 형태 : " +holiday+ '\n' + Url
        return appendedstring
    def both_Run(self,t_ID):
        #toaster = ToastNotifier()
        beforeurl = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=1&occupation="
        for value in self.want_normal_jobcode:
            beforeurl = beforeurl + value + '|'

        beforeurl = beforeurl + '&coTp='
        for value in self.want_normal_company_type:
            beforeurl = beforeurl + value + '|'

        beforeurl = beforeurl + '&region='

        for value in self.want_normal_region_Code:
            beforeurl = beforeurl + value + '|'

        beforeurl = beforeurl + '&career='
        if len(self.want_normal_career_Code)>0:
            if self.want_normal_career_Code[0] == 'N':
                beforeurl = beforeurl + 'N|Z'
            elif self.want_normal_career_Code[0] == 'E':
                beforeurl = beforeurl + 'E&minCareerM=0'

        print('일반채용 before url :',beforeurl)        
        r = requests.get(beforeurl)
        html = r.text
        soup = BeautifulSoup(html,'html.parser')
        values = soup.find_all('wanted')
        before_top_wanted = ''
        if len(values)>0:
            before_top_wanted = values[0].select("title")[0].get_text()


        beforeurl1 = "http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=1&coClcd="
        for value in self.want_open_company_type:
            beforeurl1 = beforeurl1 + value + '|'
        
        beforeurl1 += "&empWantedCareerCd="

        for value in self.want_open_career_Code:
                beforeurl1 += value +'|'
        print('공개채용 before url :',beforeurl1)  
        r1 = requests.get(beforeurl1)
        html = r1.text
        soup1 = BeautifulSoup(html,'html.parser')
        values1 = soup1.find_all('dhsopenempinfo')
        before_top_wanted1 = ''
        if len(values1)>0:
            before_top_wanted1 = values1[0].select("empwantedtitle")[0].get_text()


        while self.Stop_Flag == 1:
            print()
            print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ알림설정항목ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
            if len(self.normal_jobcode_name) == 0 :
                print('                                     알림설정된 직무(일반채용) : 모든 직무 알람')
            else:
                print('                                     알림설정된 직무(일반채용) : ',self.normal_jobcode_name)
            if len(self.normal_regionCode_Name) == 0 :
                print('                                     알림설정된 근무지(일반채용) : 모든 지역 알람')
            else:
                print('                                     알림설정된 근무지(일반채용) : ',self.normal_regionCode_Name)
            if len(self.normal_Company_Type_Name) == 0 :
                print('                                     알림설정된 기업분류(일반채용) : 모든 분류 알람')
            else:
                print('                                     알림설정된 기업분류(일반채용) : ',self.normal_Company_Type_Name)
            if len(self.normal_Career_Name) == 0 :
                print('                                     신입/경력 (일반채용) : 상관없음')
            else:
                print('                                     신입/경력 (일반채용) : ',self.normal_Career_Name)
            if len(self.open_Company_Type_Name) == 0 :
                print('                                     알림설정된 기업분류(공개채용) : 상관없음')
            else:
                print('                                     알림설정된 기업분류(공개채용) : ',self.open_Company_Type_Name)
            print('chat_ID : ',t_ID)

            nowurl = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=50&occupation="
            for value in self.want_normal_jobcode:
                nowurl = nowurl + value + '|'
            nowurl = nowurl + '&coTp='

            for value in self.want_normal_company_type:
                nowurl = nowurl + value + '|'
            
            nowurl = nowurl + '&region='

            for value in self.want_normal_region_Code:
                nowurl = nowurl + value + '|'
                
            if len(self.want_normal_career_Code) > 0 :
                nowurl = nowurl + '&career='
                if self.want_normal_career_Code[0] == 'N':
                    nowurl = nowurl + 'N|Z'
                elif self.want_normal_career_Code[0] == 'E':
                    nowurl = nowurl + 'E&minCareerM=0' 

            print('일반채용 nowurl :',nowurl)
            r = requests.get(nowurl)
            html = r.text
            soup = BeautifulSoup(html,'html.parser')
            values = soup.find_all('wanted')
            if len(values)>0:
                for value in values:
                    now_top_wanted = value.select("title")[0].get_text()
                    if now_top_wanted != before_top_wanted:
                        companyname = value.select("company")[0].get_text()
                        title = value.select("title")[0].get_text()
                        salarytype = value.select("saltpnm")[0].get_text()
                        salary = value.select("sal")[0].get_text()
                        region = value.select("region")[0].get_text()
                        holiday = value.select("holidaytpnm")[0].get_text()
                        closedate = value.select("closedt")[0].get_text()
                        url = value.select("wantedmobileinfourl")[0].get_text()
                        school = value.select("minedubg")[0].get_text()
                        career = value.select("career")[0].get_text()
                        weburl = value.select("wantedinfourl")[0].get_text()
                        appendedstring = self.stringappend(companyname,title,salarytype,salary,region,holiday,closedate,url,school,career)
                        print('일반채용 공지 게시 <',title,'>',',',companyname)
                        print('텔레그램 전송 완료')
                        self.sendTelegramMessage(t_ID,appendedstring)
                        #toaster.show_toast('[일반채용]'+companyname,now_top_wanted,duration=10,callback_on_click=lambda: open_Browser(weburl))
                        if before_top_wanted == '':#채용정보가 0개였다가 새로 들어온 경우.
                            before_top_wanted = values[0].select("title")[0].get_text()
                    else :
                        print('새로운 일반채용정보가 없습니다.')
                        before_top_wanted = values[0].select("title")[0].get_text()
                        break
                    if self.Stop_Flag != 1 :
                        break
                print('가장 최신 일반채용 :',before_top_wanted)
            else:
                print('새로운 일반채용정보가 없습니다.')
                
                    
            nowurl = "http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&callTp=L&returnType=XML&startPage=1&display=50&coClcd="
            for value in self.want_open_company_type:
                nowurl = nowurl + value + '|'

                    
            nowurl += "&empWantedCareerCd="

            for value in self.want_open_career_Code:
                nowurl = nowurl+ value +'|'
            print('공개채용 nowurl :',nowurl)
            r = requests.get(nowurl)
            html = r.text
            soup = BeautifulSoup(html,'html.parser')

            values = soup.find_all('dhsopenempinfo')

            if len(values)>0:
                for value in values:
                    now_top_wanted = value.select("empwantedtitle")[0].get_text()
                    if now_top_wanted != before_top_wanted1:
                        companyname = value.select("empbusinm")[0].get_text()
                        title = value.select("empwantedtitle")[0].get_text()
                        closedate = value.select("empwantedendt")[0].get_text()
                        url = value.select("empwantedhomepgdetail")[0].get_text()
                        wantedtype = value.select("empwantedtypenm")[0].get_text()
                        appendedstring = self.open_Stringappend(title,companyname,closedate,wantedtype,url)
                        iconurl = ''
                        if len(value.select("reglogimgnm"))>0:
                            iconurl = value.select("reglogimgnm")[0].get_text()
                        print('공개채용 공지 게시 <',title,'>',',',companyname)
                        print('텔레그램 전송 완료')
                        self.sendTelegramMessage(t_ID,appendedstring)
                        #toaster.show_toast('[공개채용]'+companyname,now_top_wanted,duration=10,callback_on_click=lambda: open_Browser(url),icon_path=iconurl)
                        if before_top_wanted1 == '':
                            before_top_wanted1 = values[0].select("empwantedtitle")[0].get_text()
                    else :
                        before_top_wanted1 = values[0].select("empwantedtitle")[0].get_text()
                        print('새로운 공개채용정보가 없습니다.')
                        break
                    if self.Stop_Flag != 1:
                        break
                print('가장 최신 공개채용 :',before_top_wanted1)
                print('새로운 채용정보 요청중') 
            else :
                print('새로운 공개채용정보가 없습니다.')

            for i in range(5):
                if self.Stop_Flag == 1:
                    time.sleep(1)
            print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')   
def setting_Reset(chat_ID):
    global Clients
    global Client_IDs
    
    for client in Clients:
        if client.chat_ID == chat_ID:
            if client.Main_Thread.is_alive():
                My_Bot.sendMessage(chat_ID, '알람이 이미 실행 중입니다. 알람을 먼저 중지해주세요.')
            else:
                client.want_normal_jobcode = []
                client.want_normal_company_type = []
                client.want_normal_region_Code = []
                client.want_normal_career_Code = []
                client.want_open_company_type = []

                client.normal_jobcode_name = []
                client.normal_regionCode_Name = []
                client.normal_Company_Type_Name = []
                client.normal_Career_Name = []
                client.open_Company_Type_Name = []
                client.Main_Thread = threading.Thread(target=client.both_Run,args=(chat_ID,))
                client.target_alarm = "일반/공채 모두 알람"
                msg = My_Bot.sendMessage(chat_ID, '초기화되었습니다.')
                add_Msg_ID(chat_ID,msg["message_id"])
                show_Setting(chat_ID)
                start_Route(chat_ID,'home')
            break
    
def deleteKeyboard(chat_ID):
    
    global Clients
    for client in Clients:
        if client.chat_ID == chat_ID:
            for msgid in client.Msg_IDs:
                try:
                    My_Bot.deleteMessage((chat_ID,msgid))
                except:
                    print('삭제할메세지발견못함')
            del client.Msg_IDs[:]
    
def add_Msg_ID(chat_ID,msg_num):
    
    global Clients
    for client in Clients:
        if client.chat_ID == chat_ID:
            client.Msg_IDs.append(msg_num)
            break
    
def show_Setting(chat_ID):
    global Clients
    global Client_IDs
    
    if chat_ID not in Client_IDs:
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
        Client_IDs.append(chat_ID)
    deleteKeyboard(chat_ID)
    for client in Clients:
        if client.chat_ID == chat_ID:
            msg = "현재알람설정" +'\n'
            msg += "[공통]" + '\n'
            msg += " 받는 알람 : " + client.target_alarm + '\n'

            if len(client.normal_Career_Name) == 0:
                msg += " 신입/경력 : " + "신입/경력 모두" + '\n'
            else:
                msg += " 신입/경력 : " + str(client.normal_Career_Name) + '\n'

            msg += "[일반채용]" + '\n'
            if len(client.normal_regionCode_Name) == 0:
                msg += " 일반채용 지역 : " + "모든 지역" + '\n'
            else:
                msg += " 일반채용 지역 : " + str(client.normal_regionCode_Name) + '\n'

            if len(client.normal_jobcode_name) == 0:
                msg += " 일반채용 직종 : " + "모든 직종" + '\n'
            else:
                msg += " 일반채용 직종 : " + str(client.normal_jobcode_name) + '\n'            

            if len(client.normal_Company_Type_Name) == 0:
                msg += " 일반채용 기업분류 : " + "기업분류 구분 없음" + '\n'
            else:
                msg += " 일반채용 기업분류 : " + str(client.normal_Company_Type_Name) + '\n'

            msg += "[공개채용]" + '\n'
            if len(client.open_Company_Type_Name) == 0:
                msg += " 공개채용 기업분류 : " + "기업분류 구분 없음" + '\n'
            else:
                 msg += " 공개채용 기업분류 : " + str(client.open_Company_Type_Name)
           

            msg = My_Bot.sendMessage(chat_ID, msg)
            add_Msg_ID(chat_ID,msg["message_id"])
            break
    
def show_JobType_Code(chat_ID):
    code = ""
    url = "http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&dtlGb=2"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    onedepths = soup.find_all('onedepth')
    for onedepth in onedepths:
        now_Code = ""
        jobCd = onedepth.find('jobscd').get_text()
        jobsname = onedepth.find('jobsnm').get_text()
        now_Code = jobCd +" "+jobsname+"\n"
        if len(code)+len(now_Code)>4090 :
            My_Bot.sendMessage(chat_ID, code)
            code = now_Code
        else : 
            code = code + now_Code
        twodepths = onedepth.find_all('twodepth')
        for twodepth in twodepths:
            jobCd = twodepth.find('jobscd').get_text()
            jobsname = twodepth.find('jobsnm').get_text()
            now_Code = jobCd +" "+jobsname+"\n"
            if len(code)+len(now_Code)>4090 :
                My_Bot.sendMessage(chat_ID, code)
                code = now_Code
            else : 
                code = code + now_Code
            '''threedepths = twodepth.find_all('threedepth')
            for threedepth in threedepths:
                jobCd = threedepth.find('jobscd').get_text()
                jobsname = threedepth.find('jobsnm').get_text()
                now_Code = jobCd +" "+jobsname+"\n"
                if len(code)+len(now_Code)>4090 :
                    My_Bot.sendMessage(chat_ID, code)
                    code = now_Code
                else : 
                    code = code + now_Code'''
    msg = My_Bot.sendMessage(chat_ID, code)
    add_Msg_ID(chat_ID,msg["message_id"])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')]])
    msg = My_Bot.sendMessage(chat_ID,'알람받고 싶은 직종코드 /직종 이라고 입력후  ,로 구분하여 입력해주세요\n ex) /직종 024,115' ,reply_markup=keyboard)
    add_Msg_ID(chat_ID,msg["message_id"])
def show_Region_Code(chat_ID):
    code = ""
    url = "http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&dtlGb=1"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    onedepths = soup.find_all('onedepth')
    for onedepth in onedepths:
        regionCd = onedepth.find('regioncd').get_text()
        regionNm = onedepth.find('regionnm').get_text()
        code += regionCd + " " + regionNm + '\n'
        '''
        twodepths = onedepth.find_all('twodepth')
        for twodepth in twodepths:
            regionCd = twodepth.find('regioncd').get_text()
            regionNm = twodepth.find('regionnm').get_text()
            code += regionCd + " " + regionNm + '\n'
        '''
    msg = My_Bot.sendMessage(chat_ID, code)
    add_Msg_ID(chat_ID,msg["message_id"])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')]])
    msg = My_Bot.sendMessage(chat_ID,'알람받고 싶은 직종코드를 "/지역" 이라고 입력후  ,로 구분하여 입력해주세요\n ex) /지역 11000,41000' ,reply_markup=keyboard)
    add_Msg_ID(chat_ID,msg["message_id"])
def start_Route(chat_ID,location):
    global Clients
    global Client_IDs
    global Msg_IDs
    
    if chat_ID not in Client_IDs:
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
        Client_IDs.append(chat_ID)
    
    if location == 'home':
        #deleteKeyboard(chat_ID)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='알람 켜기', callback_data='알람켜기')],
        [InlineKeyboardButton(text='알람 중지', callback_data='알람중지')],
        [InlineKeyboardButton(text='알람 설정하기', callback_data='설정코드')],
        [InlineKeyboardButton(text='현재 알림설정 확인', callback_data='현재알림설정확인')],
        [InlineKeyboardButton(text='설정 초기화', callback_data='설정초기화')],
            ])
        msg = My_Bot.sendMessage(chat_ID, '원하는 서비스를 선택해주세요', reply_markup=keyboard)
        add_Msg_ID(chat_ID,msg["message_id"])

    elif location == 'secondmenu':
        #deleteKeyboard(chat_ID)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='일반/공채 설정', callback_data='일반/공채')],
        [InlineKeyboardButton(text='근무지역 설정(일반채용)', callback_data='근무지 코드')],
        [InlineKeyboardButton(text='직종 설정(일반채용)', callback_data='직종 코드')],
        [InlineKeyboardButton(text='기업분류(일반채용)', callback_data='기업분류(일반채용)')],
        [InlineKeyboardButton(text='기업분류(공개채용)', callback_data='기업분류(공개채용)')],
        [InlineKeyboardButton(text='신입/경력', callback_data='신입/경력')],
        [InlineKeyboardButton(text='뒤로가기', callback_data='뒤로가기(delete)')],
            ])
        msg = My_Bot.sendMessage(chat_ID, '변경하길 원하는 설정을 선택해주세요.', reply_markup=keyboard)
        add_Msg_ID(chat_ID,msg["message_id"])
    elif location == 'alarming':
        if check_Thread_is_Running(chat_ID) == True :
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='알람중지', callback_data='알람중지')],
                    #[InlineKeyboardButton(text='현재알림설정확인', callback_data='현재알림설정확인')],
                ])
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행중입니다. 알람중지를 원할경우, 알람중지를 터치하시거나 /stop을 입력해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
def start_Route_home_delete(chat_ID):
    global Clients
    global Client_IDs
    global Msg_IDs
    
    if chat_ID not in Client_IDs:
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
        Client_IDs.append(chat_ID)   
    
    deleteKeyboard(chat_ID)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='알람 켜기', callback_data='알람켜기')],
    [InlineKeyboardButton(text='알람 중지', callback_data='알람중지')],
    [InlineKeyboardButton(text='알람 설정하기', callback_data='설정코드')],
    [InlineKeyboardButton(text='현재 알림설정 확인', callback_data='현재알림설정확인')],
    [InlineKeyboardButton(text='설정 초기화', callback_data='설정초기화')],
        ])
    msg = My_Bot.sendMessage(chat_ID, '원하는 서비스를 선택해주세요', reply_markup=keyboard)
    add_Msg_ID(chat_ID,msg["message_id"])   

'''개별적으로 사용할때
def start_all_chaeyoung(chat_ID):
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
        Client_IDs.append(chat_ID)
    for client in Clients:
        if client.chat_ID == chat_ID:
            if client.Main_Thread.is_alive() :
                My_Bot.sendMessage(chat_ID, '알람이 이미 실행중입니다. /stop으로 알람을 먼저 중지해주세요.')
            else :
                My_Bot.sendMessage(chat_ID, '일반채용 알람이 커졌습니다.\n알람중지는 /stop을 입력해주세요')
                client.Stop_Flag = 1
                client.Main_Thread = threading.Thread(target=client.all_chaeyong_Run,args=(chat_ID,))
                client.Main_Thread.start()
                show_Setting(chat_ID)
            break
'''
'''개별적으로 사용할때
def start_open_chaeyong(chat_ID):
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
        Client_IDs.append(chat_ID)
    for client in Clients:
        if client.chat_ID == chat_ID:
            if client.Main_Thread.is_alive() :
                My_Bot.sendMessage(chat_ID, '알람이 이미 실행중입니다. /stop으로 알람을 먼저 중지해주세요.')
            else :
                My_Bot.sendMessage(chat_ID, '공개채용 알람이 커졌습니다.\n알람중지는 /stop을 입력해주세요')
                client.Stop_Flag = 1
                client.Main_Thread = threading.Thread(target=client.open_Chaeyong_Run,args=(chat_ID,))
                client.Main_Thread.start()
                show_Setting(chat_ID)
            break
'''
'''개별적으로 사용할때
def start_both_chaeyong(chat_ID):
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
        Client_IDs.append(chat_ID)
    for client in Clients:
        if client.chat_ID == chat_ID:
            if client.Main_Thread.is_alive() :
                My_Bot.sendMessage(chat_ID, '알람이 이미 실행중입니다. /stop으로 알람을 먼저 중지해주세요.')
            else :
                My_Bot.sendMessage(chat_ID, '공개/일반채용 알람이 커졌습니다.\n알람중지는 /stop을 입력해주세요')
                client.Stop_Flag = 1
                client.Main_Thread = threading.Thread(target=client.both_Run,args=(chat_ID,))
                client.Main_Thread.start()
                show_Setting(chat_ID)
            break
'''
def Stop_Alarm(chat_ID,ismessage):
    global Clients
    global Client_IDs
    deleteKeyboard(chat_ID)
    
    for client in Clients:
        if client.chat_ID == chat_ID:
            client.Stop_Flag = 2
            if client.Main_Thread.is_alive():    
                client.Main_Thread.join()
                if ismessage == True:
                    msg = My_Bot.sendMessage(chat_ID, '알람이 중지되었습니다.')
                    add_Msg_ID(chat_ID,msg["message_id"])
                start_Route(chat_ID,'home')
            else:
                msg = My_Bot.sendMessage(chat_ID, '알람이 실행중이지 않습니다.')
                add_Msg_ID(chat_ID,msg["message_id"])
                start_Route(chat_ID,'home')
            break
    
def start_alarm(chat_ID):
    global Clients
    global Client_IDs
    
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    for client in Clients:
        if client.chat_ID == chat_ID:
            if client.Main_Thread.is_alive():
                My_Bot.sendMessage(chat_ID,'알람이 이미 실행 중입니다. 중지하고 다시 시도해주세요.') 
            else :
                client.Stop_Flag = 1
                show_Setting(chat_ID)
                if client.target_alarm == "일반채용 알람만":
                    new_thread = threading.Thread(target=client.all_chaeyong_Run,args=(chat_ID,))
                    client.Main_Thread = new_thread
                    new_thread.start()
                    client.target_alarm = "일반채용 알람만"
                elif client.target_alarm == "공개채용 알람만":
                    new_thread = threading.Thread(target=client.open_Chaeyong_Run,args=(chat_ID,))
                    client.Main_Thread = new_thread
                    client.target_alarm = "공개채용 알람만"
                    new_thread.start()
                elif client.target_alarm == "일반/공채 모두 알람":
                    new_thread = threading.Thread(target=client.both_Run,args=(chat_ID,))
                    client.Main_Thread = new_thread
                    client.target_alarm = "일반/공채 모두 알람"
                    new_thread.start()
            break
         
def alarm_Type_setting(chat_ID,alarm_type):
    
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    
    for client in Clients:
        if client.chat_ID == chat_ID:
            if alarm_type == "일반채용만":
                client.Main_Thread = threading.Thread(target=client.all_chaeyong_Run,args=(chat_ID,))
                client.target_alarm = "일반채용 알람만"
            if alarm_type == "공개채용만":
                client.Main_Thread = threading.Thread(target=client.open_Chaeyong_Run,args=(chat_ID,))
                client.target_alarm = "공개채용 알람만"
            if alarm_type == "모두알람":
                client.Main_Thread = threading.Thread(target=client.both_Run,args=(chat_ID,))
                client.target_alarm = "일반/공채 모두 알람"
            break
def on_callback_query(msg):
    global Msg_IDs
    query_id, chat_ID, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_ID, query_data)
    if query_data == '설정코드':
        deleteKeyboard(chat_ID)
        show_Setting(chat_ID)
        if check_Thread_is_Running(chat_ID) == False :
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='일반/공채 설정', callback_data='일반/공채')],
                    [InlineKeyboardButton(text='근무지역 설정(일반채용)', callback_data='근무지 코드')],
                    [InlineKeyboardButton(text='직종 설정(일반채용)', callback_data='직종 코드')],
                    [InlineKeyboardButton(text='기업분류(일반채용)', callback_data='기업분류(일반채용)')],
                    [InlineKeyboardButton(text='기업분류(공개채용)', callback_data='기업분류(공개채용)')],
                    [InlineKeyboardButton(text='신입/경력', callback_data='신입/경력')],
                    [InlineKeyboardButton(text='뒤로가기', callback_data='뒤로가기(delete)')],
                ])
            msg = My_Bot.sendMessage(chat_ID, '변경하길 원하는 설정을 선택해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else :
            My_Bot.sendMessage(chat_ID, '알람이 이미 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
    elif query_data == '두번째메뉴로':
        deleteKeyboard(chat_ID)
        show_Setting(chat_ID)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='일반/공채 설정', callback_data='일반/공채')],
        [InlineKeyboardButton(text='근무지역 설정(일반채용)', callback_data='근무지 코드')],
        [InlineKeyboardButton(text='직종 설정(일반채용)', callback_data='직종 코드')],
        [InlineKeyboardButton(text='기업분류(일반채용)', callback_data='기업분류(일반채용)')],
        [InlineKeyboardButton(text='기업분류(공개채용)', callback_data='기업분류(공개채용)')],
        [InlineKeyboardButton(text='신입/경력', callback_data='신입/경력')],
        [InlineKeyboardButton(text='뒤로가기', callback_data='뒤로가기(delete)')],
            ])
        msg = My_Bot.sendMessage(chat_ID, '변경하길 원하는 설정을 선택해주세요.', reply_markup=keyboard)
        add_Msg_ID(chat_ID,msg["message_id"])
    elif query_data == '알람켜기':
        deleteKeyboard(chat_ID)
        start_alarm(chat_ID)
        if check_Thread_is_Running(chat_ID) == True :
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='알람중지', callback_data='알람중지')],
                    #[InlineKeyboardButton(text='현재알림설정확인', callback_data='현재알림설정확인(알람ON)')],
                ])
            msg = My_Bot.sendMessage(chat_ID, '알람이 시작되었습니다. 알람중지를 원할경우, 알람중지를 터치하시거나 /stop을 입력해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else:
            msg = My_Bot.sendMessage(chat_ID,'알람시작을 실패했습니다.')
            add_Msg_ID(chat_ID,msg["message_id"])
    elif query_data == '직종 코드':
        if check_Thread_is_Running(chat_ID) == False :
            deleteKeyboard(chat_ID) 
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='키워드로 직종코드 찾기', callback_data='직종키워드검색')],
                    [InlineKeyboardButton(text='전체 직종코드 보기', callback_data='전체 직종코드 보기')],
                    [InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')],
                ])
            msg = My_Bot.sendMessage(chat_ID, '키워드로 직종코드를 찾아보거나, 전체 직종코드를 확인하여 알람설정을 할 수 있습니다.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else:
            deleteKeyboard(chat_ID)
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
    elif query_data == '직종키워드검색':
        if check_Thread_is_Running(chat_ID) == False:
            deleteKeyboard(chat_ID)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')],
                ])
            msg = My_Bot.sendMessage(chat_ID, '"/직종코드 키워드" 형식으로 알고 싶은 직종코드를 입력해주세요. \nex)/직종코드 간호 or /직종코드 컴퓨터', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else:
            deleteKeyboard(chat_ID)
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
    elif query_data == '전체 직종코드 보기':
        if check_Thread_is_Running(chat_ID) == False:
            deleteKeyboard(chat_ID)
            show_JobType_Code(chat_ID)
        else :
            deleteKeyboard(chat_ID)
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')   
            add_Msg_ID(chat_ID,msg["message_id"])   
    elif query_data == '근무지 코드':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            show_Region_Code(chat_ID)
        else : 
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
            start_Route(chat_ID,'secondmenu')  
    elif query_data == '뒤로가기':
        start_Route(chat_ID,'home')
    elif query_data == '뒤로가기(delete)':
        start_Route_home_delete(chat_ID)
    elif query_data == '현재알림설정확인':
        show_Setting(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            start_Route(chat_ID,'home')
        else :
            start_Route(chat_ID,'alarming')
    elif query_data == '현재알림설정확인(알람ON)':
        show_Setting(chat_ID)
        start_Route(chat_ID,'alarming')
    elif query_data == '설정초기화':
        setting_Reset(chat_ID)
    #elif query_data == '일반채용만':
        #start_all_chaeyoung(chat_ID)
    elif query_data == '알람중지':
        deleteKeyboard(chat_ID)
        Stop_Alarm(chat_ID,True)
    #elif query_data == '공개채용만':
        #start_open_chaeyong(chat_ID)
    #elif query_data == '모두 알람받기':
        #start_both_chaeyong(chat_ID)
    elif query_data == '기업분류(일반채용)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='대기업', callback_data='대기업(일반)')],
            [InlineKeyboardButton(text='벤처기업', callback_data='벤처기업(일반)')],
            [InlineKeyboardButton(text='공공기관', callback_data='공공기관(일반)')],
            [InlineKeyboardButton(text='외국계기업', callback_data='외국계기업(일반)')],
            [InlineKeyboardButton(text='청년친화강소기업', callback_data='청년친화강소기업(일반)')],
            [InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')],
            ])
            msg = My_Bot.sendMessage(chat_ID, '일반채용 기업형태를 선택해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
            start_Route(chat_ID,'secondmenu')    
    elif query_data == '대기업(일반)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"대기업","일반")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
            start_Route(chat_ID,'secondmenu')  
    elif query_data == '벤처기업(일반)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"벤처기업","일반")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  
    elif query_data == '공공기관(일반)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"공공기관","일반")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '외국계기업(일반)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"외국계기업","일반")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.') 
            add_Msg_ID(chat_ID,msg["message_id"]) 

    elif query_data == '청년친화강소기업(일반)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"청년친화강소기업","일반")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.') 
            add_Msg_ID(chat_ID,msg["message_id"]) 

    elif query_data == '기업분류(공개채용)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='대기업', callback_data='대기업(공개)')],
            [InlineKeyboardButton(text='공기업', callback_data='공기업(공개)')],
            [InlineKeyboardButton(text='공공기관', callback_data='공공기관(공개)')],
            [InlineKeyboardButton(text='중견기업', callback_data='중견기업(공개)')],
            [InlineKeyboardButton(text='외국계기업', callback_data='외국계기업(공개)')],
            [InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')],
            ])
            msg = My_Bot.sendMessage(chat_ID, '공개채용 기업형태를 선택해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '대기업(공개)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"대기업","공개")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '공기업(공개)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"공기업","공개")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')  
            add_Msg_ID(chat_ID,msg["message_id"])

    elif query_data == '공공기관(공개)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"공공기관","공개")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '중견기업(공개)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"중견기업","공개")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.') 
            add_Msg_ID(chat_ID,msg["message_id"])   

    elif query_data == '외국계기업(공개)':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_normal_Company_Type(chat_ID,"외국계기업","공개")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')  
            add_Msg_ID(chat_ID,msg["message_id"]) 

    elif query_data == '신입/경력':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='신입', callback_data='신입')],
            [InlineKeyboardButton(text='경력', callback_data='경력')],
            [InlineKeyboardButton(text='상관없음', callback_data='상관없음')],
            [InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')],
            ])
            msg = My_Bot.sendMessage(chat_ID, '신입/경력을 선택해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '신입':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_Career(chat_ID,"신입")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '경력':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_Career(chat_ID,"경력")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.') 
            add_Msg_ID(chat_ID,msg["message_id"]) 

    elif query_data == '상관없음':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False:
            Add_Career(chat_ID,"상관없음")
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')  
            add_Msg_ID(chat_ID,msg["message_id"])

    elif query_data == '일반/공채':
        deleteKeyboard(chat_ID)
        if check_Thread_is_Running(chat_ID) == False :
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='일반채용 소식만 알람받기', callback_data='일반공채만')],
            [InlineKeyboardButton(text='공개채용 소식만 알람받기', callback_data='공개채용만')],
            [InlineKeyboardButton(text='둘다 알람받기', callback_data='둘다')],
            [InlineKeyboardButton(text='뒤로가기', callback_data='두번째메뉴로')],
            ])
            msg = My_Bot.sendMessage(chat_ID, '받고싶은 알람을 선택해주세요.', reply_markup=keyboard)
            add_Msg_ID(chat_ID,msg["message_id"])
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])
    elif query_data == '일반공채만':
        if check_Thread_is_Running(chat_ID) == False:
            alarm_Type_setting(chat_ID,'일반채용만')
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            msg = My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')
            add_Msg_ID(chat_ID,msg["message_id"])  

    elif query_data == '공개채용만':
        if check_Thread_is_Running(chat_ID) == False:
            alarm_Type_setting(chat_ID,'공개채용만')
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')  

    elif query_data == '둘다':
        if check_Thread_is_Running(chat_ID) == False:
            alarm_Type_setting(chat_ID,'모두알람')
            show_Setting(chat_ID)
            start_Route(chat_ID,'secondmenu')
        else :
            My_Bot.sendMessage(chat_ID, '알람이 실행 중입니다. 알람을 먼저 중지해주세요.')  


def handle_main(msg):
    global Clients
    global Client_IDs
    msg_type, chat_type, chat_ID, msg_data, msg_id = telepot.glance(msg, long=True)
    print(msg)

    if msg_type == 'text':
        if msg['text'] == '/stop':
            Stop_Alarm(chat_ID,True)
        elif msg['text'] == '/menu':
            start_Route(chat_ID,'home')
        elif msg['text'] == '/start':
            My_Bot.sendMessage(chat_ID,'모두의 채용 알리미봇에 오신 것을 환영합니다!\n광운대학교 비전공자 SW전시회 출품을 목적으로 제작하였습니다. \n개발언어 - 파이썬 \n채용데이터 - 한국고용정보원 워크넷 API\n만든 이 - 광운대학교 정책법학대학 법학부 정지웅(팀 참가상약탈자)')
            start_Route(chat_ID,'home')
        elif msg['text'][:5] == '/직종코드':
            for c in Clients:
                if c.chat_ID == chat_ID:
                    deleteKeyboard(chat_ID)
                    if c.Main_Thread.is_alive():
                        msg = My_Bot.sendMessage(chat_ID,'알람을 먼저 중지해주세요.')
                        add_Msg_ID(chat_ID,msg["message_id"])
                    else:
                        keyward = msg['text'][6:]
                        jobCode_Query(chat_ID,keyward)
                    break
            
            
        elif msg['text'][:3] == '/직종':
            for c in Clients:
                if c.chat_ID == chat_ID:
                    if c.Main_Thread.is_alive():
                        deleteKeyboard(chat_ID)
                        msg = My_Bot.sendMessage(chat_ID,'알람을 먼저 중지해주세요.')
                        add_Msg_ID(chat_ID,msg["message_id"])
                    else:
                        deleteKeyboard(chat_ID)
                        jobCodes = msg['text'][4:].split(',')
                        Add_JobcodeAndNames(chat_ID,jobCodes)
                    break
        elif msg['text'][:3] == '/지역':
            for c in Clients:
                if c.chat_ID == chat_ID:
                    if c.Main_Thread.is_alive():
                        msg = My_Bot.sendMessage(chat_ID,'알람을 먼저 중지해주세요.')
                        add_Msg_ID(chat_ID,msg["message_id"])
                    else:
                        regionCodes = msg['text'][4:].split(',')
                        Add_RegioncodeAndNames(chat_ID,regionCodes)
                    break
        elif msg['text'] == '/show':
            for client in Clients:
                print(client.chat_ID)
                print(client.normal_regionCode_Name)
def jobCode_Query(chat_ID,keyward):
    global Msg_IDs
    code = ""
    url = "http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&dtlGb=2"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    onedepths = soup.find_all('onedepth')
    for onedepth in onedepths:
        now_Code = ""
        jobCd = onedepth.find('jobscd').get_text()
        jobsname = onedepth.find('jobsnm').get_text()
        if keyward in jobsname:
            now_Code = jobCd +" "+jobsname+"\n"
            if len(code)+len(now_Code)>4090 :
                msg = My_Bot.sendMessage(chat_ID, code)
                add_Msg_ID(chat_ID,msg["message_id"])
                code = now_Code
            else : 
                code = code + now_Code
        twodepths = onedepth.find_all('twodepth')
        for twodepth in twodepths:
            jobCd = twodepth.find('jobscd').get_text()
            jobsname = twodepth.find('jobsnm').get_text()
            if keyward in jobsname:
                now_Code = jobCd +" "+jobsname+"\n"
                if len(code)+len(now_Code)>4090 :
                    msg = My_Bot.sendMessage(chat_ID, code)
                    add_Msg_ID(chat_ID,msg["message_id"])
                    code = now_Code
                else : 
                    code = code + now_Code
            threedepths = twodepth.find_all('threedepth')
            for threedepth in threedepths:
                jobCd = threedepth.find('jobscd').get_text()
                jobsname = threedepth.find('jobsnm').get_text()
                if keyward in jobsname:
                    now_Code = jobCd +" "+jobsname+"\n"
                    if len(code)+len(now_Code)>4090 :
                        msg = My_Bot.sendMessage(chat_ID, code)
                        add_Msg_ID(chat_ID,msg["message_id"])
                        code = now_Code
                    else : 
                        code = code + now_Code
    if len(code) == 0 :
        msg = My_Bot.sendMessage(chat_ID, '검색결과를 찾을 수 없습니다.')
        add_Msg_ID(chat_ID,msg["message_id"])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='뒤로가기', callback_data='뒤로가기(delete)')],
            ])
        msg = My_Bot.sendMessage(chat_ID, '"/직종코드 키워드" 형식으로 알고 싶은 직종코드를 입력해주세요.\nex)/직종코드 간호 or /직종코드 컴퓨터', reply_markup=keyboard)
        add_Msg_ID(chat_ID,msg["message_id"])
    else:    
        msg = My_Bot.sendMessage(chat_ID, code)
        add_Msg_ID(chat_ID,msg["message_id"])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='뒤로가기', callback_data='뒤로가기(delete)')],
            ])
        msg = My_Bot.sendMessage(chat_ID, '직종코드를 다시 검색하거나 알림받기 원하는 직종코드를 /직종 입력 후 입력해주세요.\n ex)/직종코드 간호 or /직종코드 컴퓨터 \n/직종 023,024', reply_markup=keyboard)
        add_Msg_ID(chat_ID,msg["message_id"])
def Add_JobcodeAndNames(chat_ID,jobcodes):
    
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    
    for jobcode in jobcodes:
        for client in Clients :
            if client.chat_ID == chat_ID:
                url = "http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&dtlGb=2"
                r = requests.get(url)
                html = r.text
                soup = BeautifulSoup(html,'html.parser')
                onedepths = soup.find_all('onedepth')
                for onedepth in onedepths:
                    jobCd = onedepth.find('jobscd').get_text()
                    jobsname = onedepth.find('jobsnm').get_text()
                    if jobcode.strip() == jobCd:
                        if jobsname not in str(client.normal_jobcode_name):
                            client.normal_jobcode_name.append(jobsname)
                            client.want_normal_jobcode.append(jobCd)
                            break
                    twodepths = onedepth.find_all('twodepth')
                    for twodepth in twodepths:
                        jobCd = twodepth.find('jobscd').get_text()
                        jobsname = twodepth.find('jobsnm').get_text()
                        if jobcode.strip() == jobCd:
                            if jobsname not in str(client.normal_jobcode_name):
                                client.normal_jobcode_name.append(jobsname)
                                client.want_normal_jobcode.append(jobCd)
                                break
                        threedepths = twodepth.find_all('threedepth')
                        for threedepth in threedepths:
                            jobCd = threedepth.find('jobscd').get_text()
                            jobsname = threedepth.find('jobsnm').get_text()
                            if jobcode.strip() == jobCd:
                                if jobsname not in str(client.normal_jobcode_name):
                                    client.normal_jobcode_name.append(jobsname)
                                    client.want_normal_jobcode.append(jobCd)
                                    break
                break
    show_Setting(chat_ID)
    start_Route(chat_ID,'secondmenu')
def Add_RegioncodeAndNames(chat_ID,regionCodes):
    
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    for regioncode in regionCodes:
        for client in Clients:
            if client.chat_ID == chat_ID:
                url = "http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKH4G5OGQXCJZICYQ5DN2VR1HK&dtlGb=1"
                r = requests.get(url)
                html = r.text
                soup = BeautifulSoup(html,'html.parser')
                onedepths = soup.find_all('onedepth')
                for onedepth in onedepths:
                    regionCd = onedepth.find('regioncd').get_text()
                    regionNm = onedepth.find('regionnm').get_text()
                    if regionCd == regioncode.strip():
                        if regionNm not in str(client.normal_regionCode_Name):
                            client.want_normal_region_Code.append(regionCd)
                            client.normal_regionCode_Name.append(regionNm)
                            break
                    twodepths = onedepth.find_all('twodepth')
                    for twodepth in twodepths:
                        regionCd = twodepth.find('regioncd').get_text()
                        regionNm = twodepth.find('regionnm').get_text()
                        if regionCd == regioncode.strip(): 
                            if regionNm not in str(client.normal_regionCode_Name):
                                client.want_normal_region_Code.append(regionCd)
                                client.normal_regionCode_Name.append(regionNm)
                                break
                break
     
    show_Setting(chat_ID)
    start_Route(chat_ID,'secondmenu')
def Add_normal_Company_Type(chat_ID,company,setting_type):
    
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    for client in Clients:
        if chat_ID == client.chat_ID:
            if setting_type == "일반":
                if company == "대기업":
                    if company not in client.normal_Company_Type_Name:
                        client.want_normal_company_type.append('01')
                        client.normal_Company_Type_Name.append('대기업')
                if company == "벤처기업":
                    if company not in client.normal_Company_Type_Name:
                        client.want_normal_company_type.append('03')
                        client.normal_Company_Type_Name.append('벤처기업')
                if company == "공공기관":
                    if company not in client.normal_Company_Type_Name:
                        client.want_normal_company_type.append('04')
                        client.normal_Company_Type_Name.append('공공기관')
                if company == "외국계기업":
                    if company not in client.normal_Company_Type_Name:
                        client.want_normal_company_type.append('05')
                        client.normal_Company_Type_Name.append('외국계기업')
                if company == "청년친화강소기업":
                    if company not in client.normal_Company_Type_Name:
                        client.want_normal_company_type.append('09')
                        client.normal_Company_Type_Name.append('청년친화강소기업')
            elif setting_type == "공개":
                if company == "대기업":
                    if company not in client.open_Company_Type_Name:
                        client.want_open_company_type.append('10')
                        client.open_Company_Type_Name.append('대기업')
                if company == "공기업":
                    if company not in client.open_Company_Type_Name:
                        client.want_open_company_type.append('20')
                        client.open_Company_Type_Name.append('공기업')
                if company == "공공기관":
                    if company not in client.open_Company_Type_Name:
                        client.want_open_company_type.append('30')
                        client.open_Company_Type_Name.append('공공기관')
                if company == "중견기업":
                    if company not in client.open_Company_Type_Name:
                        client.want_open_company_type.append('40')
                        client.open_Company_Type_Name.append('중견기업')
                if company == "외국계기업":
                    if company not in client.open_Company_Type_Name:
                        client.want_open_company_type.append('50')
                        client.open_Company_Type_Name.append('외국계기업')   


            break
    
def Add_Career(chat_ID,career):
    global Clients
    global Client_IDs
    
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    for client in Clients:
        if client.chat_ID == chat_ID:
            if career == "신입":
                if career not in client.normal_Career_Name:
                    client.want_normal_career_Code.append('N')
                    client.normal_Career_Name.append('신입')
                    client.want_open_career_Code.append('10')
                    client.want_open_career_Code.append('30')
                    client.want_open_career_Code.append('40')
                    break
            elif career == "경력":
                if career not in client.normal_Career_Name:
                    client.want_normal_career_Code.append('E')
                    client.normal_Career_Name.append('경력')
                    client.want_open_career_Code.append('20')
                    break
            elif career == "상관없음":
                if career not in client.normal_Career_Name:
                    client.want_normal_career_Code = []
                    client.normal_Career_Name = []
                    client.want_open_career_Code = []
                    client.normal_Career_Name.append("상관없음")
                    break
    
def check_Thread_is_Running(chat_ID):   
    
    global Clients
    global Client_IDs
    if chat_ID not in Client_IDs:
        Client_IDs.append(chat_ID)
        now_Client = Client(chat_ID)
        Clients.append(now_Client)
    for client in Clients:
        if client.chat_ID == chat_ID:
            if client.Main_Thread.is_alive():
                
                return True
            else:
                
                return False
    

My_Bot = telepot.Bot(TOKEN_MAIN)
MessageLoop(My_Bot, {'chat': handle_main,'callback_query': on_callback_query}).run_as_thread()
while True:
    time.sleep(5) 
