import re


def parse_password_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 定义正则表达式以匹配密码和其强度原因
    pattern = re.compile(r'(\w+)\s这个密码的强度较高，主要原因如下：\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)

    password_data = []
    for match in matches:
        password, reasons = match
        reasons_list = [reason.strip() for reason in reasons.split('\n') if reason]
        password_data.append({'password': password, 'reasons': reasons_list})

    return password_data


def print_password_data(password_data):
    for entry in password_data:
        print(f"Password: {entry['password']}")
        print("Reasons:")
        for reason in entry['reasons']:
            print(f"  - {reason}")
        print()


# 读取和解析文件内容
standard_data = parse_password_data('standard_result.txt')
llm_data = parse_password_data('LLM_result.txt')

# 打印解析结果
print("Standard Result:")
print_password_data(standard_data)

print("LLM Result:")
print_password_data(llm_data)
