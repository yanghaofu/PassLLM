import base64

from flask import request, Flask, render_template, jsonify, redirect
from flask_sslify import SSLify
import sys
from openai import OpenAI
import ssl
from gmssl import sm2, sm3, sm4
from sqlalchemy import func
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# 请替换成你的OpenAI API密钥
api_key = "sk-Z6ttNnGzWksu7LYIOVVNuvXi3GqD5g6rykmK7NAn7ZcqTP7Q"

client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

# 确保使用UTF-8编码
if sys.getdefaultencoding() != 'utf-8':
    import importlib
    importlib.reload(sys)
    sys.setdefaultencoding('utf-8')

app = Flask(__name__)
sslify = SSLify(app)

# 生成 ECC 密钥对
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# 导出私钥
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# 导出公钥
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

print("Private Key PEM:", private_key_pem)
print("Public Key PEM:", public_key_pem)


# 初始化SM2加解密对象
# sm2的公私钥
SM2_PRIVATE_KEY = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
SM2_PUBLIC_KEY = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
# sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)

# sm2加密函数
def sm2_encrypt(info):
    encode_info = sm2_crypt.encrypt(info.encode(encoding="utf-8"))
    return encode_info
# sm2解密函数
def sm2_decrypt(info):
    decode_info = sm2_crypt.decrypt(info).decode(encoding="utf-8")
    return decode_info

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 强制使用HTTPS
@app.before_request
def force_https():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    password = data.get('password', '')

    if not password:
        return jsonify({"error": "Password is required"}), 400
    print(password)

    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    birthday = data.get('birthday', '')

    # 使用sm2进行加密
    encrypted_password = sm2_encrypt(password)
    if name!='':
        encrypted_name = sm2_encrypt(name)
        encrypted_email = sm2_encrypt(email)
        encrypted_phone = sm2_encrypt(phone)
        encrypted_birthday = sm2_encrypt(birthday)
    else:
        encrypted_name = ''
        encrypted_email = ''
        encrypted_phone = ''
        encrypted_birthday = ''

    print(f"Encrypted password: {encrypted_password}")
    print(f"Encrypted name: {encrypted_name}")
    print(f"Encrypted email: {encrypted_email}")
    print(f"Encrypted phone: {encrypted_phone}")
    print(f"Encrypted birthday: {encrypted_birthday}")

    # print("前端加密后的结果：",name, email, phone, birthday)


    # strength, explanation = evaluate_password_strength(password, name, email, phone, birthday)
    strength, explanation = evaluate_password_strength(
        encrypted_password, encrypted_name, encrypted_email, encrypted_phone, encrypted_birthday
    )

    response = {
        "strength": strength,
        "explanation": explanation
    }

    print(strength)

    return jsonify(response)

def evaluate_password_strength(encrypted_password, encrypted_name, encrypted_email, encrypted_phone, encrypted_birthday):
    try:
        # sm2解密
        password = sm2_decrypt(encrypted_password)
        if encrypted_name!='':
            name = sm2_decrypt(encrypted_name)
            email = sm2_decrypt(encrypted_email)
            phone = sm2_decrypt(encrypted_phone)
            birthday = sm2_decrypt(encrypted_birthday)
        else:
            name = ''
            email = ''
            phone = ''
            birthday = ''

        print(f"Decrypted password: {password}")
        print(f"Decrypted name: {name}")
        print(f"Decrypted email: {email}")
        print(f"Decrypted phone: {phone}")
        print(f"Decrypted birthday: {birthday}")


        # messages = [
        #     {
        #         "role": "system",
        #         "content": (
        #             "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。"
        #             "你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，"
        #             "种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
        #         )
        #     },
        #     {
        #         "role": "user",
        #         # "content": f"请直接给出下面密码的强度（非常强，强，中等，弱，很弱），并解释为什么它强或弱：\n\n密码: {password}"
        #         "content": f"你现在是一名口令领域的专家，你需要根据给定的口令以及可能附加的用户个人信息，从口令长度、字符种类、字符重复、语义信息、键盘模式、个人信息等多个角度分析口令的安全性。请给出口令强度评级（1-5级），并列出三条左右的评级原因。\n\n用户口令：{password}。"
        #     },
        # ]

        messages = [
            {
                "role": "system",
                "content": (
                    "你现在是一名口令领域的专家，你需要根据给定的口令以及可能附加的用户个人信息，从多个角度分析口令的安全性。"
                )
            },
            {
                "role": "user",
                "content": f"请直接给出下面密码的强度（非常强，强，中等，弱，很弱），三条左右主要的评级原因：\n\n密码: {password}"
            },
        ]

        if name or email or phone or birthday:
            additional_info = (
                f"\n\n附加信息：\n姓名: {name}\n电子邮件: {email}\n电话: {phone}\n生日: {birthday}"
            )
            messages.append({
                "role": "user",
                "content": additional_info
            })

        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.3,
        )

        analysis = completion.choices[0].message.content.strip()
        analysis = analysis.replace('*', '')  # 去除所有 * 符号
        strength = extract_strength_from_analysis(analysis)
        explanation = extract_explanation_from_analysis(analysis)
        print(explanation)
        return strength, explanation

    except Exception as e:
        print(f"Error analyzing password: {str(e)}")
        return "错误", "分析密码时出错。"
def extract_strength_from_analysis(analysis):
    # 获取分析文本的第一段
    first_paragraph = analysis.split('\n')[0]

    if "非常强" in first_paragraph:
        return 5
    elif "中等" in first_paragraph:
        return 3
    elif "很弱" in first_paragraph:
        return 1
    elif "弱" in first_paragraph:
        return 2
    else:
        return 4


def extract_explanation_from_analysis(analysis):
    return analysis

if __name__ == '__main__':
    # app.run(debug=True)
    # context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, check_hostname=False)
    app.run(debug=False, ssl_context=('newKey/cert.pem', 'newKey/key.pem'))
