from flask import request, Flask, render_template, jsonify
from openai import OpenAI
import requests

app = Flask(__name__)

# 请替换成你的OpenAI API密钥
api_key = "sk-Z6ttNnGzWksu7LYIOVVNuvXi3GqD5g6rykmK7NAn7ZcqTP7Q"
client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    birthday = data.get('birthday')

    # 这里可以添加你的密码强度评估逻辑
    # 这里只是一个示例返回
    strength = evaluate_password_strength(password)
    explanation = "这是一个密码强度解释的示例。"

    response = {
        "strength": strength,
        "explanation": explanation
    }
    return jsonify(response)

def evaluate_password_strength(password):
    # 这是一个简单的示例函数，可以根据你的实际需求进行修改
    length = len(password)
    if length >= 12:
        return 5
    elif length >= 10:
        return 4
    elif length >= 8:
        return 3
    elif length >= 6:
        return 2
    else:
        return 1


if __name__ == '__main__':
    app.run(debug=True)
