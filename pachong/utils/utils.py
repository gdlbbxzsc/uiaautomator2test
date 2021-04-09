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