from flask import request, Flask, render_template, jsonify
from flask_sslify import SSLify
import sys
from openai import OpenAI

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
# sslify = SSLify(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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

    print(name, email, phone, birthday)


    strength, explanation = evaluate_password_strength(password, name, email, phone, birthday)

    response = {
        "strength": strength,
        "explanation": explanation
    }

    print(strength)

    return jsonify(response)

def evaluate_password_strength(password, name, email, phone, birthday):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。"
                    "你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，"
                    "种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
                )
            },
            {
                "role": "user",
                "content": f"请直接给出下面密码的强度（非常强，强，中等，弱，很弱），并解释为什么它强或弱：\n\n密码: {password}"
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
        return 0, "Error analyzing password."

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
    app.run(debug=True)