import time
import subprocess
import re

RSSI_THRESHOLD = -85
LATENCY_THRESHOLD = 300
PACKET_LOSS_THRESHOLD = 30

def check_wifi_signal():
    """Check WiFi signal strength using Windows netsh command"""
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
        if "Signal" in result:
            lines = result.splitlines()
            for line in lines:
                if "Signal" in line:
                    signal_strength_str = line.split(":")[1].strip().replace("%", "")
                    try:
                        signal_strength = int(signal_strength_str)
                        rssi = (signal_strength / 2) - 100
                        return rssi
                    except ValueError:
                        return None
        return None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None
    except Exception:
        return None

def check_latency():
    """Ping Google DNS (8.8.8.8) to measure latency"""
    try:
        response = subprocess.run(["ping", "-n", "3", "8.8.8.8"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
        print("Ping Response:\n", response) 
        latency_values = []
        for line in response.splitlines():
            match = re.search(r"time(?:=|<?)(\d+)ms", line, re.IGNORECASE)
            if match:
                latency_values.append(int(match.group(1)))

        if latency_values:
            avg_latency = sum(latency_values) / len(latency_values)
            return avg_latency
        return None 
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Latency Error: {e}") 
        return None

def check_packet_loss():
    """Check packet loss percentage"""
    try:
        response = subprocess.run(["ping", "-n", "10", "8.8.8.8"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout
        match = re.search(r"Lost = (\d+)", response)
        if match:
            lost = int(match.group(1))
            match_sent = re.search(r"Sent = (\d+)", response)
            if match_sent:
                sent = int(match_sent.group(1))
                if sent > 0:
                    loss_percentage = (lost / sent) * 100
                    return loss_percentage
                else:
                    return None
            else:
                return None
        else:
            return None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None
    except Exception:
        return None

def classify_network():
    """Classifies network as Good or Low based on signal, latency & packet loss"""
    wifi_signal = check_wifi_signal()
    latency = check_latency()
    packet_loss = check_packet_loss()

    print(f"WiFi Signal: {wifi_signal} dBm | Latency: {latency} ms | Packet Loss: {packet_loss}%")

    if wifi_signal is not None and wifi_signal > RSSI_THRESHOLD:
        if latency is not None and latency < LATENCY_THRESHOLD and packet_loss is not None and packet_loss < PACKET_LOSS_THRESHOLD:
            return "Good Network - Cloud AI Mode"
        else:
            return "Low Network - Switching to Edge AI"
    else:
        return "No Network - Fully Offline Edge AI Mode"

while True:
    status = classify_network()
    print(f"Network Status: {status}\n")
    time.sleep(10)