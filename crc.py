import time


def calculate_crc(bit_sequence_int):
    crc_rg = 0x0000  # 15-bitowy rejestr CRC, inicjalizowany na 0
    polynomial = 0x4599  # Wielomian generujący 4599hex

    bit_length = bit_sequence_int.bit_length()

    for i in range(bit_length - 1, -1, -1):
        nxtbit = (bit_sequence_int >> i) & 1

        crcnxt = nxtbit ^ ((crc_rg >> 14) & 1)  # CRCNXT = NXTBIT EXOR CRC_RG(14)

        crc_rg = (crc_rg << 1) & 0x7FFF  # Przesunięcie w lewo o 1 bit, zachowując 15 bitów
        crc_rg &= ~0x0001  # CRC_RG(0) = 0 - zerowanie najmniej znaczącego bitu

        if crcnxt:
            crc_rg ^= polynomial  # CRC_RG(14:0) = CRC_RG(14:0) EXOR (4599hex)

    return crc_rg


def main():
    while True:
        bit_string_input = input("Wprowadź ciąg bitów (do 96 bitów) lub 'q' aby zakończyć: ")
        if bit_string_input.lower() == 'q':
            break

        if not all(c in '01' for c in bit_string_input):
            print("Nieprawidłowy format. Wprowadź tylko '0' i '1'.")
            continue

        if len(bit_string_input) > 96:
            print("Ciąg bitów może mieć maksymalnie 96 bitów.")
            continue

        try:
            num_repetitions_str = input("Podaj liczbę powtórzeń obliczenia CRC (1 do 10^9): ")
            num_repetitions = int(num_repetitions_str)
            if not (1 <= num_repetitions <= 10 ** 9):
                print("Liczba powtórzeń musi być w zakresie od 1 do 10^9.")
                continue
        except ValueError:
            print("Nieprawidłowa liczba powtórzeń. Wprowadź liczbę całkowitą.")
            continue

        # Konwersja ciągu bitów na liczbę całkowitą
        bit_sequence_as_int = int(bit_string_input, 2)

        start_time = time.perf_counter()

        calculated_crc = 0  # Inicjalizacja dla zakresu
        for _ in range(num_repetitions):
            calculated_crc = calculate_crc(bit_sequence_as_int)

        end_time = time.perf_counter()

        total_time = end_time - start_time
        average_time = total_time / num_repetitions

        print(f"\nObliczona suma kontrolna CRC: {calculated_crc:04X} (hex)")  # Formatowanie na 4 cyfry heksadecymalne
        print(f"Łączny czas realizacji dla {num_repetitions} powtórzeń: {total_time:.6f} sekund")
        print(f"Średni czas jednokrotnej realizacji CRC: {average_time:.9f} sekund")


if __name__ == "__main__":
    main()
