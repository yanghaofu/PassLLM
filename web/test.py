import os

# 替换成你的证书和密钥文件路径
cert_path = 'E:\大三\信安作品赛\代码\pass\cert.pem'
key_path = 'E:\大三\信安作品赛\代码\pass\key.pem'

def check_file_exists(filepath):
    if os.path.isfile(filepath):
        print(f"File '{filepath}' exists.")
    else:
        print(f"File '{filepath}' does NOT exist.")

def main():
    check_file_exists(cert_path)
    check_file_exists(key_path)

if __name__ == '__main__':
    main()
