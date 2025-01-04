import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 465,
    'sender_email': os.environ.get('SENDER_EMAIL'),
    'sender_password': os.environ.get('SENDER_PASSWORD'),
    'receiver_email': os.environ.get('RECEIVER_EMAIL')
} 