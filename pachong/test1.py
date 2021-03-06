from bs4 import BeautifulSoup
import requests
import time
# 保持会话
# 新建一个session对象
sess = requests.session()

# 添加headers（header为自己登录的企查查网址，输入账号密码登录之后所显示的header，此代码的上方介绍了获取方法）
afterLogin_headers = {'User-Agent': '此代码上方介绍了获取的方法'}

# post请求(代表着登录行为，登录一次即可保存，方便后面执行查询指令)
login = {'user':'自己注册的账号','password':'密码'}
sess.post('https://www.qcc.com',data=login,headers=afterLogin_headers)

def get_company_message(company):
    # 获取查询到的网页内容（全部）
    search = sess.get('https://www.qcc.com/search?key={}'.format(company),headers=afterLogin_headers,timeout=10)
    search.raise_for_status()
    search.encoding = 'utf-8' #linux utf-8
    soup = BeautifulSoup(search.text,features="html.parser")
    href = soup.find_all('a',{'class': 'title'})[0].get('href')
    time.sleep(4)
    # 获取查询到的网页内容（全部）
    details = sess.get(href,headers=afterLogin_headers,timeout=10)
    details.raise_for_status()
    details.encoding = 'utf-8' #linux utf-8
    details_soup = BeautifulSoup(details.text,features="html.parser")
    message = details_soup.text
    time.sleep(2)
    return message

import pandas as pd

def message_to_df(message,company):
    list_companys = []
    Registration_status = []
    Date_of_Establishment = []
    registered_capital = []
    contributed_capital = []
    Approved_date = []
    Unified_social_credit_code = []
    Organization_Code = []
    companyNo = []
    Taxpayer_Identification_Number = []
    sub_Industry = []
    enterprise_type = []
    Business_Term = []
    Registration_Authority = []
    staff_size = []
    Number_of_participants = []
    sub_area = []
    company_adress = []
    Business_Scope = []




    list_companys.append(company)
    Registration_status.append(message.split('登记状态')[1].split('\n')[1].split('成立日期')[0].replace(' ',''))
    Date_of_Establishment.append(message.split('成立日期')[1].split('\n')[1].replace(' ',''))
    registered_capital.append(message.split('注册资本')[1].split('人民币')[0].replace(' ',''))
    contributed_capital.append(message.split('实缴资本')[1].split('人民币')[0].replace(' ',''))
    Approved_date.append(message.split('核准日期')[1].split('\n')[1].replace(' ',''))
    try:
        credit = message.split('统一社会信用代码')[1].split('\n')[1].replace(' ','')
        Unified_social_credit_code.append(credit)
    except:
        credit = message.split('统一社会信用代码')[3].split('\n')[1].replace(' ','')
        Unified_social_credit_code.append(credit)
    Organization_Code.append(message.split('组织机构代码')[1].split('\n')[1].replace(' ',''))
    companyNo.append(message.split('工商注册号')[1].split('\n')[1].replace(' ',''))
    Taxpayer_Identification_Number.append(message.split('纳税人识别号')[1].split('\n')[1].replace(' ',''))
    try:
        sub = message.split('所属行业')[1].split('\n')[1].replace(' ','')
        sub_Industry.append(sub)
    except:
        sub = message.split('所属行业')[1].split('为')[1].split('，')[0]
        sub_Industry.append(sub)
    enterprise_type.append(message.split('企业类型')[1].split('\n')[1].replace(' ',''))
    Business_Term.append(message.split('营业期限')[1].split('登记机关')[0].split('\n')[-1].replace(' ',''))
    Registration_Authority.append(message.split('登记机关')[1].split('\n')[1].replace(' ',''))
    staff_size.append(message.split('人员规模')[1].split('人')[0].split('\n')[-1].replace(' ',''))
    Number_of_participants.append(message.split('参保人数')[1].split('所属地区')[0].replace(' ','').split('\n')[2])
    sub_area.append(message.split('所属地区')[1].split('\n')[1].replace(' ',''))
    try:
        adress = message.split('经营范围')[0].split('企业地址')[1].split('查看地图')[0].split('\n')[2].replace(' ','')
        company_adress.append(adress)
    except:
        adress = message.split('经营范围')[1].split('企业地址')[1].split()[0]
        company_adress.append(adress)
    Business_Scope.append(message.split('经营范围')[1].split('\n')[1].replace(' ',''))
    df = pd.DataFrame({'公司':company,\
                      '登记状态':Registration_status,\
                      '成立日期':Date_of_Establishment,\
                      '注册资本':registered_capital,\
                      '实缴资本':contributed_capital,\
                      '核准日期':Approved_date,\
                      '统一社会信用代码':Unified_social_credit_code,\
                      '组织机构代码':Organization_Code,\
                      '工商注册号':companyNo,\
                      '纳税人识别号':Taxpayer_Identification_Number,\
                      '所属行业':sub_Industry,\
                      '企业类型':enterprise_type,\
                      '营业期限':Business_Term,\
                      '登记机关':Registration_Authority,\
                      '人员规模':staff_size,\
                      '参保人数':Number_of_participants,\
                      '所属地区':sub_area,\
                      '企业地址':company_adress,\
                      '经营范围':Business_Scope})

    return df

# 测试所用
companys = ['深圳市腾讯计算机系统有限公司','阿里巴巴（中国）有限公司']

# 实际所用
# df_companys = pd.read_csv('自己目录的绝对路径/某某.csv')
# companys = df_companys['公司名称'].tolist()

for company in companys:
    try:
        messages = get_company_message(company)
    except:
        pass
    else:
        df = message_to_df(messages,company)
        if(company==companys[0]):
            df.to_csv('自己目录的绝对路径/某某.csv',index=False,header=True)
        else:
            df.to_csv('自己目录的绝对路径/某某.csv',mode='a+',index=False,header=False)
    time.sleep(1)