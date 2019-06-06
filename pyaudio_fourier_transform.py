import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim((0, 2000))  # x축
ax.set_xlabel('Freguency')
ax.set_ylim((0, 2500))  # y축
ax.set_ylabel('Amplitude')
line, = ax.plot([], [], c='k', lw=1)

NOTE_MIN = 50  # D3
NOTE_MAX = 84  # C6


# note <-> frequency

def freq_to_number(f):
    return 69 + 12 * np.log2(f / 440.0)


def number_to_freq(n):
    return 440 * (2.0 ** ((n - 69) / 12.0))


def note_name(n):
    return NOTE_NAMES[n % 12] + str(n / 12 - 1)


fmin = round(number_to_freq(NOTE_MIN))
fmax = round(number_to_freq(NOTE_MAX))
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()



#matplot lib 각 프레임에 적용될 배경 초기화 작업

def init():
    line.set_data([], [])
    return line,


def animate(i):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    n = len(data)
    x = np.linspace(0, 44100 / 2, n / 2)    # 균일한 배열 생성 (start, end, num-points)
    y = np.fft.fft(data) / n
    y = np.absolute(y)
    y = y[range(int(n / 2))]                # 해결중... 전혀 안됨 아래부터
    max_f = np.argmax(y[fmin:fmax])+fmin    # 원하는 진동수 범위 중 최대값을 가지는 진동수
    max_a = np.max(y[fmin:fmax])
    if (max_a > 80):
        print(np.argmax(y[fmin:fmax]))
        n0 = int(round(69 + 12 * np.log2(max_f / 440.0)))  # 진동수 -> note number
        # print(n0, NOTE_NAMES[n0 % 12], str(n0 / 12 - 1))   # note number, notes, ?
    line.set_data(x, y)
    return line,


CHUNK = 1024    # (randomly chosen)number of frames that the signals are split into
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


# printing notes
if 0:
    NOTE_MIN = 50       # D3
    NOTE_MAX = 84       # C6
    FSAMP = 22050       # Sampling frequency in Hz
    FRAME_SIZE = 2048   # How many samples per frame?
    FRAMES_PER_FFT = 16 # FFT takes average across how many frames?

    SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
    FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

    NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()


    # note <-> frequency

    def freq_to_number(f):
        return 69 + 12 * np.log2(f / 440.0)


    def number_to_freq(n):
        return 440 * 2.0 ** ((n - 69) / 12.0)


    def note_name(n):
        return NOTE_NAMES[n % 12] + str(n / 12 - 1)


    def note_to_fftbin(n):
        return number_to_freq(n) / FREQ_STEP


    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
    num_frames = 0


    # As long as we are getting data:
    while stream.is_active():

        # Get frequency of maximum response in range
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

        # Get note number and nearest note
        n = freq_to_number(freq)
        n0 = int(round(n))

        # Console output once we have a full buffer
        num_frames += 1

        if num_frames >= FRAMES_PER_FFT:
            print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
                freq, note_name(n0), n-n0))
