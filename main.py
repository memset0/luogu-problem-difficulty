import re
import yaml
import requests

# 读取配置文件

config = yaml.load(open('config.yml', 'r+', encoding = 'utf8'))
# print(config['UserID'])

# 定义全局变量

UserID = config['UserID']
UserWeb = 'https://www.luogu.org/space/show?uid={}'.format(UserID)

limitCount = config['limitCount']

# 定义全局函数

def writeFile(path, mode, content):
    file = open(path, mode)
    file.write(content)
    file.close()

# 定义 Session

request = requests.Session()

# 列出已经AC的题目

def listAC():

    req  = request.get(UserWeb)
    html = req.text
    base = req.content

    writeFile('log/user.html', 'wb+', base)

    html = re.findall(r'<div class="lg-article am-hide-sm">[\s\S]*?</div>', html)[0]
    html = html.replace('<div class="lg-article am-hide-sm">\n', '')
    html = html.replace('<h2>通过题目</h2>\n', '')
    html = html.replace('\n</div>', '')
    html = re.sub(r'\[<a data-pjax href="/problem/show\?pid=[\s\S]*?">', '', html)
    html = re.sub(r'</a>\]', '', html)
    prob = re.split(r'\n', html)

    writeFile('log/AC.txt', 'w+', ", ".join(str(it) for it in prob))

    return prob

# 按题号统计题目难度

def statistics(prob):

    global limitCount
    ans = []

    for probID in prob:

        print('Statisticsing {}'.format(probID))

        try:
            probWeb = 'https://www.luogu.org/problemnew/show/{}'.format(probID)

            req  = request.get(probWeb)
            html = req.text
            base = req.content

            writeFile('log/prob.html', 'wb+', base)

            dify = re.findall(r'<li><strong>难度</strong>[\s\S]*?</span>', html)[0]
            dify = re.sub(r'<li[\s\S]*">', '', dify)
            dify = dify.replace('</span>', '')

            ans.append(dify)

            limitCount -= 1
            if limitCount == 0:
                break

        except:
            print('Met a problem at {}'.format(probID))

    return ans

# 统计输出结果

def result(ans):
    pass

# 主程序部分

if config['hasStatisticsed'] == False:
    ans = statistics(listAC())
    out = ", ".join(str(it) for it in ans)
    writeFile('log/ans.txt', 'w+', out)
    print(ans)
else:
    ans = open('log/ans.txt', 'r+').read().split(', ')

result(ans)

print('Finish')