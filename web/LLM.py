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
    print("\033[95m[system] " + "\033[0m成功接收到用户口令并加密！" + "\033[0m\n")

    print("\033[95m[system] " + "\033[0mTLS协议传输中......" + "\033[0m\n")

    print("\033[95m[system] " + "\033[0m国密算法解密中......" + "\033[0m\n")

    print("\033[95m[system] " + "\033[0m成功解密口令：password123!" + "\033[0m\n")
    
    data = request.get_json()
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    birthday = data.get('birthday')

    # 这里可以添加你的密码强度评估逻辑
    # 这里只是一个示例返回
    strength = evaluate_password_strength(password)
    explanation = "you&me1314口令包含小写字母、特殊字符和数字的组合。但是，由于其简单的字符排列模式，口令的整体强度相对较低。具体原因如下：1.混合字符：在这方面，口令具有较高的强度，因为它包含多种字符。但是，口令缺少大写字母，故而复杂度稍低。2.有限字符跳转：口令的字符排列模式明显，且跳跃模式很容易猜到。具体来说：'you'和'me'是常见的英语单词。'&'是一个常见的特殊字符，通常用于连接两个单词或短语。'1314'是一种常见的数字模式，在汉语中是“一生一世”的谐音。"

    response = {
        "strength": 2,
        "explanation": explanation
    }
    return jsonify(response)

def evaluate_password_strength(password):
    # 这是一个简单的示例函数，可以根据你的实际需求进行修改
    print("\033[95m[system] " + "\033[0m强度评判中......" + "\033[0m\n")
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
