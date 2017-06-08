#coding=utf-8
import requests
from bs4 import BeautifulSoup
from os.path import dirname
import os
import sys
import getpass

OUTPUT_DICTIONARY = os.path.dirname(os.path.realpath(__file__)) + "\\AC" #相對目錄AC
# 輸入
print("============= Login =============")
Username = raw_input("Zerojudge Username: ")
# Password mask.
Password = getpass.getpass("Zerojudge Password: ")

LOGIN_URL = "https://zerojudge.tw/Login"
BASE_URL = "https://zerojudge.tw/Submissions?&account=" + Username + "&status=AC"
RELATE_URL = "./Submissions?account=" + Username + "&status=AC"
INFO_URL = "https://zerojudge.tw/UserStatistic"
LOGOUT_URL = "https://zerojudge.tw/Logout"

loginSession = requests.session();
headers = {"User-Agent":"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
           "Content-Type":"application/x-www-form-urlencoded",
           "Connection":"Keep-Alive"}
res = loginSession.get(LOGIN_URL, headers=headers)
soup = BeautifulSoup(res.text,"html5lib")
token = soup.find("input", {"name":"token"})['value']
try:
	post={"token":token,"account":Username,"passwd":Password, "returnPage":"/UserStatistic"}
	res = loginSession.post(LOGIN_URL, headers=headers, data=post)
	if(res.url != LOGIN_URL):
		res = loginSession.get(INFO_URL, headers=headers)
		soup = BeautifulSoup(res.text,"html5lib")
		AC_count = soup.find("a", {"href" : RELATE_URL}).text
		print(u"AC數: " + AC_count)
		PageCount = 1;
		FileCount = 0;
		while(True):
			Url = BASE_URL + "&page=" + str(PageCount)
			res = loginSession.get(Url, headers=headers)
			soup = BeautifulSoup(res.text,"html5lib")
			noData = True
			for codeParent in soup.findAll("div", { "class" : "SolutionCode" }):
				noData = False
				solutionId = codeParent["solutionid"]
				qustionInfo = soup.find("tr", {"solutionid":solutionId}).findAll("a")[1]
				questionId = qustionInfo["href"].split("=")[1]
				questionName = qustionInfo.text
				
				code = codeParent.find("textarea", {"name": "code"}).text
				codeType = codeParent.find("a", {"class": "showcode"}).text
				if not os.path.exists(OUTPUT_DICTIONARY):# 先確認資料夾是否存在
					os.makedirs(OUTPUT_DICTIONARY)
				# 刪除windows保留字
				questionName = questionName.replace("\\","").replace(".","").replace("?","").replace("*","").replace("/","").replace("|","").replace(":","").replace(">","").replace("<","").replace("\"","")
				fileName = questionId + " " + questionName + "." + codeType.lower()
				# 解決Console預設編碼不是utf-8時產生的問題
				print(str(FileCount) + ". " + fileName.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
				# 解決OUTPUT_DICTIONARY為str物件無法與unicode物件append的問題
				filePath = OUTPUT_DICTIONARY.decode(sys.stdin.encoding) + "\\" + fileName
				if(os.path.exists(filePath)):
					# 重複檔名改為(1)
					repeatTimes = 1
					repeatFilePath = filePath
					while(os.path.exists(repeatFilePath)):
						repeatFilePath =  OUTPUT_DICTIONARY.decode(sys.stdin.encoding) + "\\" + questionId + " " + questionName + "(" + str(repeatTimes) + ")" + "." + codeType.lower()
						repeatTimes += 1
					f = open(repeatFilePath, 'wb')
				else:
					f = open(filePath, 'wb')
				f.write(code.encode("utf-8"))
				f.close()
				FileCount += 1
			# 如果沒資料了就跳出
			if(noData):
				break
			# 下一頁
			PageCount += 1
		# Output infomation.
		print(u"輸出成功，共 " + str(FileCount) + u" 個檔案位於" + OUTPUT_DICTIONARY.decode(sys.stdin.encoding))
	else :
		print(u"帳密錯誤或登入次數過多")
except Exception as inst:
	print(inst)
finally:
	loginSession.get(LOGOUT_URL, headers = headers) #登出防止重複登入被卡死
# End of program.
raw_input("Press enter any key to exit... ")