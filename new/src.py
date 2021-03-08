import time
import os
import json #parse
import requests #json from url
import re #prettify
from json2html import * #table
import webbrowser #result
import colorterminal #prettier for new terminal users

#TODO: directly read json from requests module. i ran into encoding error, write + read in utf8 fixes it

print("")
if os.path.exists("temp.json"): #quiz data
  os.remove("temp.json")
  print(colorterminal.ColorText.YELLOW + "Removed temp.json")

#how to quiz id
print(colorterminal.ColorText.GREEN + "Dont start the quiz yet! First fetch your quiz id like this : ")
print(" ")
print(colorterminal.ColorText.WHITE + "https://quizizz.com/quiz/" + colorterminal.ColorText.PURPLE + "5bebe060ee53f9001a713529" + colorterminal.ColorText.WHITE + "/start")
print("Here, "+ colorterminal.ColorText.PURPLE + "5bebe060ee53f9001a713529" + colorterminal.ColorText.WHITE +" is the quiz code")
print("")
print("Paste in your quiz code: ")
qzcode = input(" > ")
print("")

#request
url = 'https://quizizz.com/quiz/' + qzcode
r = requests.get(url, allow_redirects=True)
open('temp.json', 'wb').write(r.content)

#write then read to solve encoding error

f = open('temp.json', "r", encoding="utf8")
quizInfo = json.loads(f.read())

def deUnicode(stuff): #remove most unicode
    string = r'{}'.format(stuff)
    for letter, i in zip(string, range(len(string))):
        try:
            if letter == "\\" and string[i + 1] == "u":
                string = string[:i] + string[i + 6:]
        except:
            pass
    return string

allAns = {}
for question in quizInfo["data"]["quiz"]["info"]["questions"]: #parse through the question data
    if question["type"] == "MCQ":
        #single question
        if question["structure"]["options"][int(question["structure"]["answer"])]["text"] == "":
            #image answer
            answer = question["structure"]["options"][int(question["structure"]["answer"])]["media"][0]["url"]
        else:
            answer = question["structure"]["options"][int(question["structure"]["answer"])]["text"]
    elif question["type"] == "MSQ":
        #multiple answers
        answer = []
        for answerC in question["structure"]["answer"]:
            if question["structure"]["options"][int(answerC)]["text"] == "":
                answer.append(question["structure"]["options"][int(answerC)]["media"][0]["url"])
            else:
                answer.append(question["structure"]["options"][int(answerC)]["text"])

    questionStr = question["structure"]["query"]["text"].replace('"', '\\"')
    allAns[questionStr] = answer #ugly output

#clean
f = open("answers.json", "w")
final = json.dumps(allAns, sort_keys=True, indent=2)
clean = re.compile('<.*?>')
final = re.sub(clean, '', final)
#extra unicode
final = final.replace("&nbsp;", "")
final = final.encode("utf8").decode("unicode-escape")

os.remove("temp.json")

#prettyprint
person_dict = json.loads(final)
pp = json.dumps(person_dict, indent = 4, sort_keys=True)
page = json2html.convert(json = pp) #table
pf = open("answer.html", "w")
#table padding stylesheet 
pf.write(page + "<style>" + """
table {
  table-layout: fixed;
  width: 100%;
  border-collapse: collapse;
  border: 3px solid purple;
}
thead th:nth-child(1) {
  width: 30%;
}
thead th:nth-child(2) {
  width: 20%;
}
thead th:nth-child(3) {
  width: 15%;
}
thead th:nth-child(4) {
  width: 35%;
}
th, td {
  padding: 20px;
}
""" + "</style>")
pf.close()

webbrowser.open("answer.html", new=2)#new tab
os.remove("answers.json")
time.sleep(3)
print("")
print("")
print("")
print("Quiting...")
print("If this application doesn't quit please do CTRL+C or close this window !") #sometimes browsers wierd
quit()