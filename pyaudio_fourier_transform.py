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

NOTE_MIN = 40  # 50 : D3
NOTE_MAX = 84  # C6
limit_a = int(input("limit of Amplitude? "))
N_CHUNK = int(input("(16일 때 오차범위 +- 1.4hz) N_CHUNK? "))    # 16일 때 오차범위 +- 1.4hz


save_note = bool(input("Do you want to save NOTES? (1 or 0) : "))
if(save_note):
    f = open("NOTE.txt",'w')

# saving notes
def notetxt(x):
    data = note_name(x)
    f.write(data+"\n")


NOTE_NAMES = '도C 도#C# 레D 레#D# 미E 파F 파#F# 솔G 솔#G# 라A 라#A# 시B'.split()

# note <-> frequency

def freq_to_number(f):
    return 69 + 12 * np.log2(f / 440.0)


def number_to_freq(n):
    return 440 * (2.0 ** ((n - 69) / 12.0))


def note_name(n):
    return NOTE_NAMES[n % 12]

F_MIN = number_to_freq(NOTE_MIN)

print(NOTE_NAMES)
print("NOTE_MIN :", NOTE_MIN , "\tMinimum Frequency :", F_MIN)

#matplot lib 각 프레임에 적용될 배경 초기화 작업

p_note = 0  # note 저장을 위한 이전 노트

def init():
    line.set_data([], [])
    return line,


def animate(i):

    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    n = len(data)
    x = np.linspace(0, 44100, n/2)    # 균일한 배열 생성 (start, end, num-points)
    y = np.fft.fft(data) / n
    y = y[range(int(n/2))]
    y = np.absolute(y)
    max_f = (float)(np.argmax(y))*(44100/n)*2   # note min max 적용해야함. 원하는 진동수 범위 중 최대값을 가지는 진동수
    max_a = np.max(y)
    if max_a > limit_a and max_f > F_MIN:
        note = freq_to_number(max_f)
        note0 = int(round(note))
        print('freq: {:6.1f} Hz  \ta: {:5.2f}   \tnote: {:>3s} {}    \tgap: {:+1.3f}'.format(
            max_f, max_a, note_name(note0), note0, (note - note0)))
        if (save_note):
            global p_note
            if p_note != note0 :
                notetxt(note0)
                p_note = note0

    line.set_data(x, y)
    return line,


CHUNK = 1024*N_CHUNK    # (randomly chosen)number of frames that the signals are split into
                        # 오차범위 : 1024*16 -> +-1.3hz

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