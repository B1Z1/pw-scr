import struct


def convert_internal_to_ieee754(internal_hex_str):
    try:
        internal_int = int(internal_hex_str, 16)

        # Obsługa specjalnego przypadku: Zero
        if internal_int == 0x00000000:
            return "00000000"

        ieee_sign_bit = 0  # Zakładamy, że konwertujemy tylko liczby dodatnie jak w przykładach.

        internal_exponent = (internal_int >> 24) & 0x7F  # Maska 0x7F = 01111111 (7 bitów)

        ieee_exponent = internal_exponent + 127

        if not (0 < ieee_exponent < 255):  # Znormalizowane liczby, wykluczamy 0 i 255 (inf/NaN)
            pass

        ieee_mantissa = internal_int & 0x007FFFFF  # Weź 23 najmłodsze bity

        ieee_float_bits = (ieee_sign_bit << 31) | (ieee_exponent << 23) | ieee_mantissa

        return f"{ieee_float_bits:08X}"

    except ValueError:
        return "Błąd: Niepoprawny format wejściowy. Oczekiwano 32-bitowego ciągu szesnastkowego."
    except Exception as e:
        return f"Wystąpił nieoczekiwany błąd: {e}"


def hex_to_float(hex_str):
    try:
        hex_int = int(hex_str, 16)

        return struct.unpack('>f', struct.pack('>I', hex_int))[0]
    except ValueError:
        return None


def main():
    print("--- Zadanie 5.2: Konwersja unikalnego kodu 'wewnętrznego' do IEEE 754 ---")
    print("Wprowadź 32-bitowy 'kod wewnętrzny' w formacie szesnastkowym (np. 83100000).")
    print("Konwersja bazuje na hipotezie struktury 'kodu wewnętrznego' z dostarczonego dokumentu.")

    while True:
        user_input = input("\nWprowadź kod wewnętrzny (hex, np. 83100000) lub 'q' aby wyjść: ").strip()
        if user_input.lower() == 'q':
            break

        # Usunięcie ewentualnych spacji, jeśli użytkownik wprowadzi "8000 0000"
        internal_hex_input = user_input.replace(" ", "")

        if len(internal_hex_input) != 8:
            print("Błąd: Kod wewnętrzny musi mieć 8 cyfr szesnastkowych.")
            continue

        ieee_hex_result = convert_internal_to_ieee754(internal_hex_input)

        if "Błąd" in ieee_hex_result:
            print(ieee_hex_result)
        else:
            print(f"Wprowadzony kod wewnętrzny (hex): {internal_hex_input}")
            print(f"Konwertowany kod IEEE 754 (hex): {ieee_hex_result}")

            # Weryfikacja wartości float
            float_value = hex_to_float(ieee_hex_result)
            if float_value is not None:
                print(f"Wartość zmiennoprzecinkowa (IEEE 754): {float_value}")
            else:
                print("Nie udało się skonwertować kodu IEEE 754 na wartość zmiennoprzecinkową.")


if __name__ == "__main__":
    main()