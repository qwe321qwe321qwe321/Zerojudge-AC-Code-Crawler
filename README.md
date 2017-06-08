# Zerojudge-AC-Code-Crawler
爬zerojudge的AC code

原本用python 3.6寫，可是pyinstaller不支援python3.6，剛好電腦還有灌Python 2.7就直接改寫了。因此release的執行檔是python2.7的版本
## Dependencies
* Python 2.7/3.6
* [Requests](http://docs.python-requests.org/en/master/)
* [BeatifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [html5lib](https://github.com/html5lib/html5lib-python)
## Screenshot
![img](Screenshot.png)
## 遇到的問題
* 照之前的方法直接使用`html.parser`解析遇到`textarea`會有下面的問題，後來改用`html5lib`解析就解決了
```
<textarea>
#include<stdio.h> // BeatifulSoup會把<stdio.h>視為標籤，導致讀取出來的東西錯誤
int main(){
  return 0;
}
</textarea>
```
* windows檔名問題，懶人解決方法
```
# 刪除windows保留字
questionName = questionName.replace("\\","").replace(".","").replace("?","").replace("*","").replace("/","").replace("|","").replace(":","").replace(">","").replace("<","").replace("\"","")
```
* 後來改用Python 2.7遇到的編碼問題，因為太多了直接看coding時的[註解](Python2.7/Zerojudge-AC-Code-Crawler.py#L59)
