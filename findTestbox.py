import serial.tools.list_ports
import sys

# Funktion zum Finden des Pyboard-Ports
# Diese Funktion durchsucht alle seriellen Ports und gibt den Port zurück, der das Pyboard enthält.
def find_pyboard_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Überprüfe Port: {port.device} - {port.description}")
        if "Pyboard" in port.description:
            return port.device
    return None

# Beispielnutzung:
if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello {name}")
    print("Suche nach Pyboard...")
    pyboard_port = find_pyboard_port()
    if pyboard_port:
        print(f"Pyboard gefunden an: {pyboard_port}")
    else:
        print("Kein Pyboard gefunden.")