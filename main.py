import re
import os
import yaml
import requests

# ========== 初始化程序 ==========

def init():
    os.system("mkdir log")
    os.system("mkdir result")
    global request, config, debug, UserID, prob
    request = requests.Session()
    request.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'})
    print(request.headers)
    config  = yaml.load(open('config.yml', 'r+', encoding = 'utf8'))
    debug   = config['debug']
    prob = {}
    try:
        UserID = config['UserID'].split(', ')
    except:
        UserID = [config['UserID']]
    if config['hasStatisticsed']:
        try:
            prob = yaml.load(open('result/problem.yml', 'r+', encoding = 'utf8'))
        except:
            pass

# ========== 定义全局函数 ==========

# ---------- 正则表达式截取一段内容 ----------

def strFind(before, after, old):
    return re.findall(r'{}[\s\S]*?{}'.format(before, after), old)[0]\
        .replace(before, '').replace(after, '')

# ---------- 输出内容到文件 ----------

def writeFile(path, mode, content):
    file = open(path, mode)
    file.write(content)
    file.close()

# ---------- 把一些上千数据转换为正常数值 ----------

def isThousand(old): # 顺便吐槽一下某些大佬的AC数太多了
    if 'K' in old or 'k' in old:
        old = old.replace('K', '').replace('k', '')
        old = int(float(old) * 1000 // 1)
    return str(old)


# ---------- 获取一道题目的难度 ----------

def getProblem(probID):

    global prob

    if not probID in prob:

        print('Statisticsing {}'.format(probID))

        try:
            probWeb = 'https://www.luogu.org/problemnew/show/{}'.format(probID)

            req  = request.get(probWeb)
            html = req.text
            base = req.content

            if debug:
                writeFile('log/prob.html', 'wb+', base)

            dify = re.findall(r'<li><strong>难度</strong>[\s\S]*?</span>', html)[0]
            dify = re.sub(r'<li[\s\S]*">', '', dify)
            dify = dify.replace('</span>', '')

            prob[probID] = dify 
            return dify

        except:
            print('Met a problem at {}'.format(probID))
            dify = '难度未知'

            prob[probID] = dify 
            return dify

    else:
        return prob[probID]

# ========== 获取个人信息页面 ==========

def getUser(UserID):

    if config['hasStatisticsed'] == False:
        UserWeb = 'https://www.luogu.org/space/show?uid={}'.format(UserID)
        req  = request.get(UserWeb)
        html = req.text
        base = req.content
        writeFile('log/U{}.html'.format(UserID), 'wb+', base)
        return html

    else:
        file = open('log/U{}.html'.format(UserID), 'r+', encoding='utf8')
        content = file.read()
        file.close()
        return content

# ========== 列出已经AC的题目 ==========

def listAC(UserID):

    print('List AC problems of U{}'.format(UserID))

    html = getUser(UserID)
    html = re.findall(r'<div class="lg-article am-hide-sm">[\s\S]*?</div>', html)[0]
    html = html.replace('<div class="lg-article am-hide-sm">\n', '')
    html = html.replace('<h2>通过题目</h2>\n', '')
    html = html.replace('\n</div>', '')
    html = re.sub(r'\[<a data-pjax href="/problem/show\?pid=[\s\S]*?">', '', html)
    html = re.sub(r'</a>\]', '', html)
    prob = re.split(r'\n', html)

    writeFile('log/AC.txt', 'w+', ", ".join(str(it) for it in prob))

    return prob

# ========== 按题号统计题目难度 ==========

def statistics(prob):

    ans = []
    for probID in prob:
        ans.append(getProblem(probID))

    out = ", ".join(str(it) for it in ans)
    writeFile('log/ans.txt', 'w+', out)

    return ans

# ========== 统计输出结果 ==========

def modify(set, content):
    result = content
    for it in re.findall(r'{\|[\s\S]*?\|}', content):
        try:
            # print('Modify "{}"'.format(it[2:-2]))
            result = result.replace(it, set[it[2:-2]])
        except:
            result = result.replace(it, '0')
    return result

def modifyFile(oldPath, newPath, set):
    file = open(oldPath, 'r+', encoding='utf8')
    content = file.read()
    file.close()
    content = modify(set, content)
    file = open(newPath, 'w+', encoding='utf8')
    file.write(content)
    file.close()

def result(UserID, ans):

    set  = {}
    html = getUser(UserID)

    set['UserID']     = str(UserID)
    set['UserWeb']    = 'https://www.luogu.org/space/show?uid={}'.format(UserID)
    set['UserName']   = strFind('<h1>U{} '.format(UserID), '</h1>', html)
    set['Submit']     = re.sub(r'<[\s\S]*?>', '', strFind('<span class="lg-bignum-num">', '</span><span class="lg-bignum-text">提交</span>', html))
    set['SubmitReal'] = isThousand(set['Submit'])
    set['Accept']     = re.sub(r'<[\s\S]*?>', '', strFind('</span></li><li><span class="lg-bignum-num">', '</span><span class="lg-bignum-text">通过</span>', html))
    set['AcceptReal'] = isThousand(set['Accept'])
    set['ACpercent']  = str(int(set['AcceptReal']) / int(set['SubmitReal']))
    set['ACpercent%'] = str(int(set['AcceptReal']) * 100 // int(set['SubmitReal']))

    for it in ans:
        set[it] = 0
    for it in ans:
        set[it] += 1
    for it in ans:
        set[it] = str(set[it])

    print('Finish listing, now this it the information of U{}'.format(UserID), set)

    modifyFile('theme/count.txt', 'result/U{} - {}.txt'.format(UserID, set['UserName']), set)

# ========== 结束程序 ==========

def finish():
    global prob
    content = ''
    for first, second in prob.items():
        content += '{}: {}\n'.format(first, second)
    file = open('result/problem.yml', 'w+', encoding='utf8')
    file.write(content)
    file.close()
    print('Finish.')

# ========== 主程序部分 ==========

init()

for it in UserID:
    result(it, statistics(listAC(int(it))))

finish()
