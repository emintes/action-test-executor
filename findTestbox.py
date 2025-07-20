import serial.tools.list_ports
import sys
import subprocess

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
    print(sys.argv)
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello {name}")
    print("Suche nach Pyboard...")
    pyboard_port = find_pyboard_port()
    if pyboard_port:
        print(f"Pyboard gefunden an: {pyboard_port}")
        result = subprocess.run(["mpremote connect " + pyboard_port + " fs cp entrypoint.sh :entrypoint.sh"], capture_output=True, text=True, shell=True)
        # Rückgabecode
        print("Return code:", result.returncode)

        # Standardausgabe
        print("stdout:", result.stdout)

        # Fehlerausgabe
        print("stderr:", result.stderr)
    else:
        print("Kein Pyboard gefunden.")
    
    print("FERTIG")
    sys.exit(1)