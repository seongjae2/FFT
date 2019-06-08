import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim((0, 3000))  # x축
ax.set_xlabel('Freguency')
ax.set_ylim((0, 3000))  # y축
ax.set_ylabel('Amplitude')

line, = ax.plot([], [], c='k', lw=1)

NOTE_MIN = 50  # D3
NOTE_MAX = 84  # C6
limit_a = 1700

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

# note <-> frequency

def freq_to_number(f):
    return 69 + 12 * np.log2(f / 440.0)


def number_to_freq(n):
    return 440 * (2.0 ** ((n - 69) / 12.0))


def note_name(n):
    return NOTE_NAMES[n % 12]

fmin = round(number_to_freq(NOTE_MIN))
fmax = round(number_to_freq(NOTE_MAX))

print(NOTE_NAMES)
print()

#matplot lib 각 프레임에 적용될 배경 초기화 작업

def init():
    line.set_data([], [])
    return line,


def animate(i):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    n = len(data)
    x = np.linspace(0, 44100/2, n/2)    # 균일한 배열 생성 (start, end, num-points)
    y = np.fft.fft(data) / n
    y = y[range(int(n/2))]
    y = np.absolute(y)
    max_f = np.argmax(y)*(44100/n)   # 원하는 진동수 범위 중 최대값을 가지는 진동수
    max_a = np.max(y)
    if max_a > limit_a:
        note = freq_to_number(max_f)
        note0 = int(round(69 + 12 * np.log2(max_f / 440.0)))
        print('freq: {:6.1f} Hz  \ta: {:5.2f}   \tnote: {:>3s} {}    \tgap: {:+1.3f}'.format(
            max_f, max_a, note_name(note0), note0 , (note - note0)))
    line.set_data(x, y)
    return line,


CHUNK = 2048    # (randomly chosen)number of frames that the signals are split into
FORMAT = pyaudio.paInt16
CHANNELS = 2    # Each frame will have 2 samples, 2 bytes
RATE = 44100    # the number of frames per second

# 음성 데이터 스트림을 여는 코드
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

#animation 출력

animation = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=200, interval=10, blit=True)


plt.show()