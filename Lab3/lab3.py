from PIL import Image
import os
import random


# Перевод текстовых символов в битовую систему
def text_to_bits(text):
    bits = []
    for char in text:
        byte = ord(char)
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


# =========================
# 1. декодирование изображения из задания
# =========================
def decode_with_keys(image_path, keys_path):
    print("\n=== ДЕКОДИРОВАНИЕ ИСХ. ИЗОБРАЖЕНИЯ ===")

    try:
        image = Image.open(image_path).convert("RGB")
        pixels = image.load()
    except Exception:
        print("[!] Ошибка загрузки изображения")
        return

    text_bytes = []

    try:
        with open(keys_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                line = line.replace("(", "").replace(")", "")

                try:
                    x_str, y_str = line.split(",")
                    x, y = int(x_str), int(y_str)

                    r, g, b = pixels[x, y]
                    text_bytes.append(b)

                except Exception:
                    print(f"[!] Ошибка строки: {line}")

    except Exception:
        print("Ошибка чтения файла ключей")
        return

    text = bytes(text_bytes).decode("utf-8", errors="ignore")

    print("\n=== РЕЗУЛЬТАТ ===")
    print(text)


# =========================
# 2. кодирование своего изображения
# =========================
def encode_image(input_path, output_dir, text):
    print("\n=== КОДИРОВАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО ИЗОБРАЖЕНИЯ ===")

    try:
        image = Image.open(input_path).convert("RGB")
    except Exception:
        print("[!] Ошибка загрузки изображения, проверьте корректность пути")
        return

    text += "\x00"
    bits = text_to_bits(text)
    pixels = image.load()

    if not output_dir.strip():
        output_dir = os.path.dirname(input_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)

    output_image = os.path.join(output_dir, f"{name}_completed{ext}")
    key_path = os.path.join(output_dir, f"keys_{name}.txt")

    print(f"\nТекст: {text[:-1]}")
    print("Биты первого символа:")
    print(bits[:8])

    bit_index = 0
    coordinates = []

    max_capacity = image.width * image.height * 4
    if len(bits) > max_capacity:
        print(
            "[!] Текст слишком большой для исходного изображения. Выберите другое изображение"
        )
        return

    # =========================
    # генерация случайных координат для ключа
    # =========================
    all_coords = [(x, y) for y in range(image.height) for x in range(image.width)]
    random.shuffle(all_coords)

    # =========================
    # Часть кодирования изображения
    # =========================
    for x, y in all_coords:

        if bit_index >= len(bits):
            break

        r, g, b = pixels[x, y]
        original_r = r

        chunk = bits[bit_index : bit_index + 4]
        while len(chunk) < 4:
            chunk.append(0)

        bit_index += 4

        r = r & 0b11110000

        for i, bit in enumerate(chunk):
            r |= bit << (3 - i)

        pixels[x, y] = (r, g, b)
        coordinates.append((x, y))

        print(f"\nПиксель ({x},{y})")
        print(f"Исходный R: {format(original_r, '08b')}")
        print(f"Новый    R: {format(r, '08b')}")

    image.save(output_image)

    # =========================
    # Сохранение нового ключа
    # =========================
    with open(key_path, "w", encoding="utf-8") as f:
        for x, y in coordinates:
            f.write(f"({x},{y})\n")

    print("\n=== РЕЗУЛЬТАТ ===")
    print(f"Измененное изображение: {output_image}")
    print(f"Ключ: {key_path}")


# =========================
# 3. Декодирование пользовательского изображения
# =========================
def decode_lsb(image_path, key_path):
    print("\n=== ДЕКОДИРОВАНИЕ ВАШЕГО ИЗОБРАЖЕНИЯ ===")

    try:
        image = Image.open(image_path).convert("RGB")
        pixels = image.load()
    except Exception:
        print("Ошибка извлечения изображения, проверьте корректность пути и файл.")
        return

    bits = []

    try:
        with open(key_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                x, y = map(int, line.replace("(", "").replace(")", "").split(","))

                r, g, b = pixels[x, y]

                bits.extend([(r >> i) & 1 for i in range(3, -1, -1)])

    except Exception:
        print(
            "Ошибка извлечения ключа, проверьте корректность пути и наличие файла с ключом"
        )
        return

    chars = []

    for i in range(0, len(bits) - 7, 8):
        byte = bits[i : i + 8]

        value = 0
        for bit in byte:
            value = (value << 1) | bit

        chars.append(chr(value))

        if chars[-1] == "\x00":
            break

    text = "".join(chars).split("\x00")[0]

    print("\n=== РЕЗУЛЬТАТ ДЕКОДИРОВАНИЯ ===")
    print(text)


def main():
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Декодировать изображение преподавателя")
        print("2. Закодировать текст в изображение")
        print("3. Декодировать текст из изображения")
        print("4. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            image_path = input("Укажите путь к изображению: ")
            keys_path = input("Укажите путь к ключам: ")
            decode_with_keys(image_path, keys_path)

        elif choice == "2":
            input_path = input("Укажите путь к изображению: ")
            output_dir = input(
                "Папка для сохранения (или оставьте пустым для сохранения рядом с исх. изображением): "
            )
            text = input("Введите текст для кодирования: ")

            encode_image(input_path, output_dir, text)

        elif choice == "3":
            image_path = input("Укажите путь к изображению: ")
            key_path = input("Укажите путь к ключу: ")
            decode_lsb(image_path, key_path)

        elif choice == "4":
            print("Выход")
            break

        else:
            print("Неверный ввод, пожалуйста, повторите ввод")


if __name__ == "__main__":
    main()
# ИИ - 60%