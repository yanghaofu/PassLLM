import base64

import requests
from flask import request, Flask, render_template, jsonify
from flask_sslify import SSLify
import sys
from openai import OpenAI
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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    password = data.get('password', '')

    if not password:
        return jsonify({"error": "Password is required"}), 400

    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    birthday = data.get('birthday', '')

    # 对文本信息进行加密并使用 base64 编码
    encrypted_password = base64.b64encode(password.encode()).decode('utf-8')
    encrypted_name = base64.b64encode(name.encode()).decode('utf-8') if name else ''
    encrypted_email = base64.b64encode(email.encode()).decode('utf-8') if email else ''
    encrypted_phone = base64.b64encode(phone.encode()).decode('utf-8') if phone else ''
    encrypted_birthday = base64.b64encode(birthday.encode()).decode('utf-8') if birthday else ''

    print(f"Encrypted password: {encrypted_password}")
    print(f"Encrypted name: {encrypted_name}")
    print(f"Encrypted email: {encrypted_email}")
    print(f"Encrypted phone: {encrypted_phone}")
    print(f"Encrypted birthday: {encrypted_birthday}")

    strength, explanation = evaluate_password_strength(
        encrypted_password, encrypted_name, encrypted_email, encrypted_phone, encrypted_birthday
    )

    response = {
        "strength": strength,
        "explanation": explanation
    }

    return jsonify(response)

def evaluate_password_strength(encrypted_password, encrypted_name, encrypted_email, encrypted_phone, encrypted_birthday):
    try:
        # 解密文本信息并使用 base64 解码
        password = base64.b64decode(encrypted_password.encode('utf-8')).decode('utf-8') if encrypted_password else ''
        name = base64.b64decode(encrypted_name.encode('utf-8')).decode('utf-8') if encrypted_name else ''
        email = base64.b64decode(encrypted_email.encode('utf-8')).decode('utf-8') if encrypted_email else ''
        phone = base64.b64decode(encrypted_phone.encode('utf-8')).decode('utf-8') if encrypted_phone else ''
        birthday = base64.b64decode(encrypted_birthday.encode('utf-8')).decode('utf-8') if encrypted_birthday else ''

        print(f"Decrypted password: {password}")
        print(f"Decrypted name: {name}")
        print(f"Decrypted email: {email}")
        print(f"Decrypted phone: {phone}")
        print(f"Decrypted birthday: {birthday}")

        url = 'http://127.0.0.1:6006/submit'
        data = {
            'password': password,
            'name': name,
            'email': email,
            'phone': phone,
            'birthday': birthday
        }

        response = requests.post(url, json=data)
        print(response.status_code)
        if response.status_code == 200:
            try:
                response_json = response.json()
                analysis = response_json.get("analysis", "").replace('*', '')  # 去除所有 * 符号
                strength = extract_strength_from_analysis(analysis)
                explanation = extract_explanation_from_analysis(analysis)
                print(explanation)
                return strength, explanation
            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
        else:
            return "错误", "服务器返回错误代码: {}".format(response.status_code)

    except Exception as e:
        print(f"Error analyzing password: {str(e)}")
        return "错误", "分析密码时出错。"

def extract_strength_from_analysis(analysis):
    # 获取分析文本的第一段
    first_paragraph = analysis.split('\n')[0]

    if "非常强" in first_paragraph:
        return 5
    elif "中等"in first_paragraph:
        return 3
    elif "很弱"in first_paragraph:
        return 1
    elif "弱"in first_paragraph:
        return 2
    else:
        return 4

def extract_explanation_from_analysis(analysis):
    return analysis

if __name__ == '__main__':
    app.run(debug=True, port=6006)