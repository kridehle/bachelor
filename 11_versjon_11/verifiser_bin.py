import struct

def read_and_print_binary_file(filename):
    try:
        with open(filename, "rb") as f:
            while chunk := f.read(2):  # Leser 2 byte (16-bit) om gangen
                value = struct.unpack("<h", chunk)[0]  # "<h" leser som little-endian 16-bit signert
                print(f"{value}", end=" ")  # Skriver ut verdien med mellomrom
    except FileNotFoundError:
        print(f"Filen {filename} ble ikke funnet.")
    except Exception as e:
        print(f"En feil oppstod: {e}")
        
def read_and_print_raw_binary(filename):
    try:
        with open(filename, "rb") as f:
            while chunk := f.read(2):  # Leser 2 byte (16-bit) om gangen
                bits = "".join(f"{byte:08b}" for byte in chunk)  # Konverterer til binærstreng
                print(bits, end=" ")  # Skriver ut bitene med mellomrom
    except FileNotFoundError:
        print(f"Filen {filename} ble ikke funnet.")
    except Exception as e:
        print(f"En feil oppstod: {e}")

# Bruk programmet
filename = "iq_data.bin"  # Endre til riktig filnavn
read_and_print_binary_file(filename)
