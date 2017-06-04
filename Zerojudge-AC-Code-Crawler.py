# coding=UTF-8
import requests
from bs4 import BeautifulSoup
from os.path import dirname
import os
# 設定參數
Username = ""
Password = ""
OUTPUT_DICTIONARY = dirname(__file__) + "/AC" + "" #程式所在資料夾的AC資料夾

LOGIN_URL = "https://zerojudge.tw/Login"
BASE_URL = "https://zerojudge.tw/Submissions?&account=" + Username + "&status=AC"
RELATE_URL = "./Submissions?account=" + Username + "&status=AC"
INFO_URL = "https://zerojudge.tw/UserStatistic"
LOGOUT_URL = "https://zerojudge.tw/Logout"

loginSession = requests.session();
headers = {"User-Agent":"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
           "Content-Type":"application/x-www-form-urlencoded"}
res = loginSession.get(LOGIN_URL, headers=headers)
soup = BeautifulSoup(res.text,"html.parser")
token = soup.find("input", {"name":"token"})['value']
try:
	post={"token":token,"account":Username,"passwd":Password, "returnPage":"/UserStatistic"}
	res = loginSession.post(LOGIN_URL, headers=headers, data=post)
	if(res.url != LOGIN_URL):
		res = loginSession.get(INFO_URL, headers=headers)
		soup = BeautifulSoup(res.text,"html.parser")
		AC_count = soup.find("a", {"href" : RELATE_URL}).text
		print("AC數: " + AC_count)
		PageCount = int(int(AC_count) / 20) + 1;
		for i in range(PageCount):
			Url = BASE_URL + "&page=" + str(i+1)
			res = loginSession.get(Url, headers=headers)
			soup = BeautifulSoup(res.text,"html.parser")
			for codeParent in soup.findAll("div", { "class" : "SolutionCode" }):
				solutionId = codeParent["solutionid"]
				qustionInfo = soup.find("tr", {"solutionid":solutionId}).findAll("a")[1]
				questionId = qustionInfo["href"].split("=")[1]
				questionName = qustionInfo.text
				print(questionId + " " + questionName)
				code = codeParent.find("textarea", {"name": "code"}).text
				codeType = codeParent.find("a", {"class": "showcode"}).text
				if not os.path.exists(OUTPUT_DICTIONARY):#先確認資料夾是否存在
					os.makedirs(OUTPUT_DICTIONARY)
				# 刪除windows保留字
				questionName = questionName.replace("\\","").replace(".","").replace("?","").replace("*","").replace("/","").replace("|","").replace(":","").replace(">","").replace("<","")
				f = open(OUTPUT_DICTIONARY + "/" + questionId + " " + questionName + "." + codeType.lower(), 'w', encoding = 'UTF-8')
				f.write(code)
				f.close()
	else :
		print("帳密錯誤或登入次數過多")
except Exception as inst:
	print(inst)
finally:
	loginSession.get(LOGOUT_URL, headers = headers) #登出防止重複登入被卡死