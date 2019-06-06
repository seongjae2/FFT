import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim((0, 2000))  # x축
ax.set_ylim((0, 2000))
line, = ax.plot([], [], c='k', lw=1)


def init():
    line.set_data([], [])
    return line,


def animate(i):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    n = len(data)
    x = np.linspace(0, 44100 / 2, n / 2)
    y = np.fft.fft(data) / n
    y = np.absolute(y)
    y = y[range(int(n / 2))]
    line.set_data(x, y)
    return line,


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

animation = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=200, interval=10, blit=True)

plt.show()

# printing notes

NOTE_MIN = 50       # D3
NOTE_MAX = 84       # C6
FSAMP = 22050       # Sampling frequency in Hz
FRAME_SIZE = 1024   # How many samples per frame?
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
