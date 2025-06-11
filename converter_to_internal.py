import struct


def convert_ieee754_to_internal_hex(ieee_hex_str):
    try:
        ieee_int = int(ieee_hex_str, 16)

        if ieee_int == 0x00000000:
            return "00000000"

        ieee_sign_bit = (ieee_int >> 31) & 0x1
        ieee_exponent = (ieee_int >> 23) & 0xFF
        ieee_mantissa = ieee_int & 0x007FFFFF  # 23 bity

        if ieee_sign_bit == 1:
            return "Błąd: Obsługa liczb ujemnych w kodzie wewnętrznym nie jest zdefiniowana w specyfikacji."

        internal_P_bit = 1

        internal_exponent = ieee_exponent - 127

        if not (0 <= internal_exponent <= 0x7F):  # 0x7F to 127 (max 7-bit unsigned)
            return "Błąd: Wykładnik IEEE 754 poza zakresem konwersji do wewnętrznego formatu."

        internal_mantissa = ieee_mantissa  # Kopiujemy 23 bity mantysy IEEE

        internal_float_bits = (internal_P_bit << 31) | (internal_exponent << 24) | internal_mantissa

        return f"{internal_float_bits:08X}"

    except ValueError:
        return "Błąd: Niepoprawny format wejściowy. Oczekiwano 32-bitowego ciągu szesnastkowego IEEE 754."
    except Exception as e:
        return f"Wystąpił nieoczekiwany błąd: {e}"


def float_to_hex(f_value):
    try:
        return struct.pack('>f', f_value).hex().upper()
    except Exception:
        return None


def main():
    print("--- Zadanie 5.3: Konwersja IEEE 754 do unikalnego kodu 'wewnętrznego' ---")
    print("Wprowadź 32-bitowy kod IEEE 754 w formacie szesnastkowym (np. 40000000).")
    print("Konwersja bazuje na hipotezie struktury 'kodu wewnętrznego' z dostarczonego dokumentu.")

    while True:
        user_input = input("\nWprowadź kod IEEE 754 (hex, np. 40000000) lub 'q' aby wyjść: ").strip()
        if user_input.lower() == 'q':
            break

        # Usunięcie ewentualnych spacji
        ieee_hex_input = user_input.replace(" ", "")

        if len(ieee_hex_input) != 8:
            print("Błąd: Kod IEEE 754 musi mieć 8 cyfr szesnastkowych.")
            continue

        internal_hex_result = convert_ieee754_to_internal_hex(ieee_hex_input)

        if "Błąd" in internal_hex_result:
            print(internal_hex_result)
        else:
            print(f"Wprowadzony kod IEEE 754 (hex): {ieee_hex_input}")

            # Spróbujmy wyświetlić wartość zmiennoprzecinkową dla wejścia IEEE 754
            try:
                float_val = struct.unpack('>f', bytes.fromhex(ieee_hex_input))[0]
                print(f"Wartość zmiennoprzecinkowa (IEEE 754): {float_val}")
            except Exception:
                print("Nie udało się zinterpretować wprowadzonego kodu IEEE 754 jako liczby zmiennoprzecinkowej.")

            print(f"Konwertowany kod wewnętrzny (hex): {internal_hex_result}")


if __name__ == "__main__":
    main()