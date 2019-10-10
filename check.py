from bs4 import BeautifulSoup
import requests, time

def check_update(url="https://www.uukanshu.com", novel="/b/439/"):
    result = requests.get(url+novel)
    #html = result.text.encode('iso-8859-1').decode('gbk')
    c = result.text
    soup = BeautifulSoup(c, "html.parser")
    new = soup.find("div", class_="zuixin").find("a")
    #print(new.text, "https://www.uukanshu.com"+new.get('href'))


    with open("./chapter_list.txt", encoding='utf-8') as fo:
        his_chap = fo.readline()
    if (his_chap == new.text):
        print("No updated.")
        update = False
    else:
        with open("./chapter_list.txt", "w", encoding='utf-8') as fi:
            fi.write(new.text)
        update = True
        #print("New chapter ", new.text, "is updated!")
        #print("URL:", url+new.get('href'))
    return update, new.text, new.get('href')

if __name__ == "__main__":
    update, name, href = check_update()
    if (update):
        print("New chapter ", name, "is updated!")
        print("URL:", url+href)
