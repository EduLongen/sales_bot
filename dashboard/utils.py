import qrcode
from io import BytesIO
import requests
import os
from dotenv import load_dotenv


def calculate_crc(data):
    crc = 0xFFFF
    data_bytes = (data + '6304').encode('utf-8')

    for byte in data_bytes:
        crc ^= (byte << 8)
        for _ in range(8):
            if (crc & 0x8000) != 0:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF

    return format(crc, '04X')

def generate_pix_qr_code(pix_payment):
    pix_info = f'0014BR.GOV.BCB.PIX01{len(pix_payment.pix_key):02d}{pix_payment.pix_key}'
    
    br_code_parts = [
        '00020126',  # Payload Format Indicator
        f'{len(pix_info):02d}{pix_info}',
        '52040000',  # Merchant Category Code
        '5303986',   # Transaction Currency
        '5802BR',    # Country Code
        f'59{len(pix_payment.description):02d}{pix_payment.description}',  # Description
        f'60{len("CityName"):02d}CityName',  # Static CityName placeholder, or fetch dynamically
        '62070503***',  # Additional Data Field (Reference Label placeholder)
    ]
    
    br_code = ''.join(br_code_parts)
    crc = calculate_crc(br_code)
    pix_data = f'{br_code}6304{crc}'
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(pix_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer

load_dotenv()

def send_telegram_message(message, chat_ids):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        raise ValueError("Bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    errors = []

    for chat_id in chat_ids:
        data = {
            'chat_id': str(chat_id),
            'text': message
        }
        print(chat_id)
        try:
            response = requests.post(url, json=data)
            print(f"Resposta do Telegram: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            errors.append(f"Erro de conexão para chat_id {chat_id}: {str(e)}")
    return errors