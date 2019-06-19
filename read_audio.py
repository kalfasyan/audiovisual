import pyaudio
import wave
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
print("Using device: {}".format(p.get_device_info_by_index(3)))
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
		input_device_index=1,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)
    decoded = np.frombuffer(data, 'Float32')

    sig = decoded #savgol_filter(decoded,121,3)
    plt.plot(sig)
    # plt.ylim(0.1, 1.1) #1e-39)
    plt.pause(0.01)
    plt.clf()
    if i > 10:
        break

print("* done recording")

#stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
