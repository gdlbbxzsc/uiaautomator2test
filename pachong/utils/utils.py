from pathlib import Path
#创建目录
img_path = Path("D:\\python\\demo\\电脑壁纸\\img")
img_path.mkdir(parents=True,exist_ok=True)
# 拼接
path = img_path / '{}.jpg'.format("test_name")


# 替换该义字符
def change_title(title):
    pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")  # '/ \ : * ? " < > |'
    new_title = re.sub(pattern, "_", title)  # 替换为下划线
    return new_title


fake_useragent 随机agent




#(.*?)'.'匹配\n(换行符)以外的任何字符
#(.*?)'*'前面的字符出现0次或以上
#(.*?)'?'非贪婪模式
 re.findall('<span class="bjh-p">(.*?)</span></p><p>',data )


 #快速为 “：” 前后字符串加上单引号 需要find replace功能
(.*?): (.*)
'$1': '$2',