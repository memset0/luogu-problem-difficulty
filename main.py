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

def strFind(before, after, old):
    return re.findall(r'{}[\s\S]*?{}'.format(before, after), old)[0]\
        .replace(before, '').replace(after, '')

def writeFile(path, mode, content):
    file = open(path, mode)
    file.write(content)
    file.close()

# 定义 Session

request = requests.Session()

# 获取个人信息页面

def getUser():

    if config['hasStatisticsed'] == False:
        global UserWeb
        req  = request.get(UserWeb)
        html = req.text
        base = req.content
        writeFile('log/user.html', 'wb+', base)
        return html

    else:
        file = open('log/user.html', 'r+', encoding='utf8')
        content = file.read()
        file.close()
        return content

# 列出已经AC的题目

def listAC():

    html = getUser()

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

def modify(set, content):
    result = content
    for it in re.findall(r'{\|[\s\S]*?\|}', content):
        # print('Modify "{}"'.format(it[2:-2]))
        result = result.replace(it, set[it[2:-2]])
    return result

def modifyFile(oldPath, newPath, set):
    file = open(oldPath, 'r+', encoding='utf8')
    content = file.read()
    file.close()
    content = modify(set, content)
    file = open(newPath, 'w+', encoding='utf8')
    file.write(content)
    file.close()

def result(ans):

    # 初始化
    set = {}

    # 从全局变量中引入
    global UserID, UserWeb
    set['UserID'] = str(UserID)
    set['UserWeb'] = UserWeb

    # 从网页（个人简介页面）中引入
    html = getUser()

    set['UserName'] = strFind('<h1>U{} '.format(UserID), '</h1>', html)
    set['Submit'] = strFind('<span class="lg-bignum-num">', '</span><span class="lg-bignum-text">提交</span>', html)
    set['Accept'] = strFind('</span></li><li><span class="lg-bignum-num">', '</span><span class="lg-bignum-text">通过</span>', html)
    set['ACpercent'] = str(int(set['Accept']) / int(set['Submit']))
    set['ACpercent%'] = str(int(set['Accept']) * 100 // int(set['Submit']))

    # 从统计数据中引入
    for it in ans:
        set[it] = 0
    for it in ans:
        set[it] += 1
    for it in ans:
        set[it] = str(set[it])

    print(set)

    modifyFile('theme/index.html', 'result.html', set)
    modifyFile('theme/count.txt', 'result.txt', set)
    


# 主程序部分

if config['hasStatisticsed'] == False:
    ans = statistics(listAC())
    out = ", ".join(str(it) for it in ans)
    writeFile('log/ans.txt', 'w+', out)
else:
    ans = open('log/ans.txt', 'r+').read().split(', ')

result(ans)

print('Finish')