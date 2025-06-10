import os

def change_ip_address(interface, new_ip, subnet_mask, gateway):
    # IP adresini değiştirme komutları
    os.system(f"netsh interface ip set address name=\"{interface}\" static {new_ip} {subnet_mask} {gateway}")
    print(f"IP adresi değiştirildi: {new_ip}")

def change_mac_address(interface, new_mac):
    # MAC adresini değiştirmek için önce arayüzü devre dışı bırak, sonra MAC adresini değiştir, ve tekrar etkinleştir
    os.system(f"netsh interface set interface \"{interface}\" admin=disable")
    os.system(f"reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\0001 /v NetworkAddress /t REG_SZ /d {new_mac.replace(':', '')} /f")
    os.system(f"netsh interface set interface \"{interface}\" admin=enable")
    print(f"MAC adresi değiştirildi: {new_mac}")

def main():
    interface = "Ethernet"  # Değiştirmek istediğiniz ağ bağdaştırıcısının adı
    new_ip = "192.168.1.200"  # Yeni IP adresi
    subnet_mask = "255.255.255.1"  # Alt ağ maskesi
    gateway = "192.168.1.1"  # Varsayılan ağ geçidi
    new_mac = "00:11:22:33:44:50"  # Yeni MAC adresi

    # IP adresini değiştirme
    change_ip_address(interface, new_ip, subnet_mask, gateway)
    
    # MAC adresini değiştirme
    change_mac_address(interface, new_mac)

if __name__ == "__main__":
    main()
