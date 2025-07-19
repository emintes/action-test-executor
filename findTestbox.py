import serial.tools.list_ports

def find_pyboard_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Überprüfe Port: {port.device} - {port.description}")
        if "Pyboard" in port.description:
            return port.device
    return None

# Beispielnutzung:
if __name__ == "__main__":
    pyboard_port = find_pyboard_port()
    if pyboard_port:
        print(f"Pyboard gefunden an: {pyboard_port}")
    else:
        print("Kein Pyboard gefunden.")