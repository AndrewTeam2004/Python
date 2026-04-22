import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


print("=== Программа анализа WAV-файла ===")

filename = "31.wav"
required_rate = 192000  # частота дискретизации по заданию

# пробуем прочитать файл
try:
    rate, data = wavfile.read(filename)
except:
    print("Ошибка чтения файла")
    print("Убедитесь, что файл существует и перезапустите программу")
    exit()

# проверка требуемой частоты дискретизации
if rate != required_rate:
    print("Неверная частота:", rate)
    print("Сохраните файл в требуемой частоте", required_rate)
    exit()

# проверка моно
if len(data.shape) != 1:
    print("Файл не моно канальный")
    print("Сохраните файл в моно формате")
    exit()

print("Файл соответствует требованиям")
print("Частота дискретизации:", rate)
print("Количество отсчетов:", len(data))

# ввод количества отсчетов
while True:
    try:
        n = int(input("Сколько отсчетов использовать: "))
        if 1 <= n <= len(data):
            break
        else:
            print("Введите число от 1 до", len(data))
    except:
        print("Ошибка ввода")

signal = data[:n]

# ---------------------------
# 1.1 Дискретные отсчеты
plt.figure()
plt.plot(signal)
plt.title("Дискретные отсчеты сигнала")
plt.xlabel("Номер отсчета")
plt.ylabel("Амплитуда")
plt.grid()

# ---------------------------
# 1.2 Осциллограмма
time = np.arange(n) / rate
plt.figure()
plt.plot(time, signal)
plt.title("Осциллограмма")
plt.xlabel("Время (сек)")
plt.ylabel("Амплитуда")
plt.grid()

# ---------------------------
# 1.3 Спектр
fft = np.fft.fft(signal)
amplitude = np.sqrt(np.real(fft) ** 2 + np.imag(fft) ** 2)
freq = np.fft.fftfreq(n, 1 / rate)
half = n // 2
plt.figure()
plt.plot(freq[:half], amplitude[:half])
plt.title("Спектр сигнала")
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплитуда")
plt.grid()

# ---------------------------
# 1.4 Гистограмма
plt.figure()
plt.hist(signal, bins=50)
plt.title("Гистограмма сигнала")
plt.xlabel("Амплитуда")
plt.ylabel("Количество")
plt.grid()
plt.show()
