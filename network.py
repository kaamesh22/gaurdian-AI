import os
import time
import subprocess

RSSI_THRESHOLD = -85  
LATENCY_THRESHOLD = 300 
PACKET_LOSS_THRESHOLD = 30  

def check_wifi_signal():
    """Check WiFi signal strength using Windows netsh command"""
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True).stdout
        if "Signal" in result:
            signal_strength = int(result.split("Signal")[1].split(":")[1].strip().replace("%", ""))
            rssi = (signal_strength / 2) - 100  
            return rssi
    except:
        pass
    return None  

def check_latency():
    """Ping Google DNS (8.8.8.8) to measure latency"""
    try:
        response = subprocess.run(["ping", "-n", "3", "8.8.8.8"], capture_output=True, text=True).stdout
        if "time=" in response:
            latency_values = [float(line.split("time=")[-1].split("ms")[0]) for line in response.split("\n") if "time=" in line]
            avg_latency = sum(latency_values) / len(latency_values)
            return avg_latency
    except:
        pass
    return None  

def check_packet_loss():
    """Check packet loss percentage"""
    try:
        response = subprocess.run(["ping", "-n", "10", "8.8.8.8"], capture_output=True, text=True).stdout
        if "Lost =" in response:
            sent = int(response.split("Sent = ")[1].split(",")[0])
            lost = int(response.split("Lost = ")[1].split(",")[0])
            loss_percentage = (lost / sent) * 100
            return loss_percentage
    except:
        pass
    return None  

def classify_network():
    """Classifies network as Good or Low based on signal, latency & packet loss"""
    wifi_signal = check_wifi_signal()
    latency = check_latency()
    packet_loss = check_packet_loss()

    print(f"WiFi Signal: {wifi_signal} dBm | Latency: {latency} ms | Packet Loss: {packet_loss}%")

    if wifi_signal and wifi_signal > RSSI_THRESHOLD:
        if latency and latency < LATENCY_THRESHOLD and packet_loss and packet_loss < PACKET_LOSS_THRESHOLD:
            return "Good Network - Cloud AI Mode"
        else:
            return "Low Network - Switching to Edge AI"
    else:
        return "No Network - Fully Offline Edge AI Mode"

while True:
    status = classify_network()
    print(f"Network Status: {status}\n")
    time.sleep(10)
