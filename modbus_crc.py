import time

def calculate_crc16_modbus(data_bytes):
    # Początkowa wartość rejestru CRC
    crc = 0xFFFF
    # Wielomian używany w MODBUS RTU (odwrócony 8005h)
    polynomial = 0xA001

    for byte in data_bytes:
        crc ^= byte
        for _ in range(8):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= polynomial
            else:
                crc >>= 1
    return crc

def validate_hex_input(hex_string):
    if not hex_string:
        return None, "Wprowadzono pusty ciąg."

    hex_string = hex_string.replace(" ", "")

    if len(hex_string) % 2 != 0:
        return None, "Nieparzysta liczba cyfr heksadecymalnych. Każdy bajt to dwie cyfry."

    try:
        byte_list = []
        for i in range(0, len(hex_string), 2):
            byte_list.append(int(hex_string[i:i+2], 16))
        return byte_list, None
    except ValueError:
        return None, "Nieprawidłowe znaki heksadecymalne w ciągu."

def main():
    print("--- Obliczanie CRC-16 MODBUS RTU ---")

    while True:
        hex_input = input("Wprowadź sekwencję bajtów w notacji heksadecymalnej (max 256 bajtów, np. 01 10 00 11): ").strip()
        data_bytes, error = validate_hex_input(hex_input)
        if error:
            print(f"Błąd: {error}")
        elif len(data_bytes) > 256:
            print(f"Błąd: Sekwencja bajtów przekracza maksymalną długość 256 bajtów (wprowadzono {len(data_bytes)} bajtów).")
        else:
            break

    while True:
        try:
            n_repetitions_str = input(f"Wprowadź liczbę powtórzeń algorytmu CRC (1 do 10^9): ").strip()
            n_repetitions = int(n_repetitions_str)
            if not (1 <= n_repetitions <= 10**9):
                print("Błąd: Liczba powtórzeń musi być w zakresie od 1 do 10^9.")
            else:
                break
        except ValueError:
            print("Błąd: Proszę wprowadzić prawidłową liczbę całkowitą.")

    print(f"\nObliczanie CRC dla sekwencji: {[f'{b:02X}' for b in data_bytes]} (liczba bajtów: {len(data_bytes)})")
    print(f"Liczba powtórzeń: {n_repetitions}")

    # Pomiar czasu
    start_time = time.perf_counter()

    final_crc = 0
    for _ in range(n_repetitions):
        final_crc = calculate_crc16_modbus(data_bytes)

    end_time = time.perf_counter()
    total_time_ms = (end_time - start_time) * 1000

    print(f"\nWyliczona CRC (hex): {final_crc:04X}")
    print(f"Łączny czas realizacji {n_repetitions} powtórzeń: {total_time_ms:.3f} ms")

if __name__ == "__main__":
    main()