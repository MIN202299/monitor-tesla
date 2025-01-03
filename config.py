import os

EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 465,
    'sender_email': os.environ.get('SENDER_EMAIL'),
    'sender_password': os.environ.get('SENDER_PASSWORD'),
    'receiver_email': os.environ.get('RECEIVER_EMAIL')
} 