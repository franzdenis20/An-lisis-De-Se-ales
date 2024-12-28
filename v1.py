import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import soundfile as sf
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt
import os
import threading
import pyaudio
import wave

class VoiceNoiseSeparator:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Voz y Ruido")
        self.audio_data = None
        self.samplerate = 44100
        self.is_recording = False
        self.frames = []
        self.audio_file = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Separador de Voz y Ruido", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Importar Audio", command=self.import_audio).pack(pady=5)
        tk.Button(self.root, text="Iniciar Grabación", command=self.start_recording).pack(pady=5)
        tk.Button(self.root, text="Parar Grabación", command=self.stop_recording).pack(pady=5)
        tk.Button(self.root, text="Separar Voz y Ruido", command=self.separate_voice_noise).pack(pady=5)

    def import_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if not file_path:
            return
        self.audio_file = file_path
        self.audio_data, self.samplerate = sf.read(file_path)
        if len(self.audio_data.shape) > 1:
            self.audio_data = np.mean(self.audio_data, axis=1)  # Convertir a mono
        messagebox.showinfo("Éxito", "Audio importado correctamente.")

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        threading.Thread(target=self.record_audio).start()
        messagebox.showinfo("Grabación", "Grabando... Presiona 'Parar Grabación' para finalizar.")

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.samplerate, input=True, frames_per_buffer=1024)
        while self.is_recording:
            data = stream.read(1024)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

        file_path = "procesar_audio.wav"
        wf = wave.open(file_path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.samplerate)
        wf.writeframes(b"".join(self.frames))
        wf.close()

        self.audio_file = file_path
        self.audio_data, self.samplerate = sf.read(file_path)
        messagebox.showinfo("Grabación", "Grabación finalizada y guardada.")

    def stop_recording(self):
        self.is_recording = False

    def separate_voice_noise(self):
        if self.audio_data is None:
            messagebox.showwarning("Error", "Primero importa o graba un audio.")
            return

        # Aplicar FFT para analizar frecuencias
        fft_signal = fft(self.audio_data)
        freqs = fftfreq(len(fft_signal), 1 / self.samplerate)
        magnitude = np.abs(fft_signal)

        # Detectar la frecuencia principal de la voz
        voice_mask = (abs(freqs) > 85) & (abs(freqs) < 4000)  # Rango extendido para la voz humana
        fft_voice = np.zeros_like(fft_signal)
        fft_noise = np.zeros_like(fft_signal)

        # Separar la voz y el ruido
        fft_voice[voice_mask] = fft_signal[voice_mask]
        fft_noise[~voice_mask] = fft_signal[~voice_mask]

        # Reconstruir las señales usando IFFT
        voice_signal = ifft(fft_voice).real
        noise_signal = ifft(fft_noise).real

        # Guardar los audios separados
        voice_file = "voz.wav"
        noise_file = "ruido.wav"
        sf.write(voice_file, voice_signal, self.samplerate)
        sf.write(noise_file, noise_signal, self.samplerate)

        # Mostrar gráficos
        self.plot_signals(self.audio_data, voice_signal, noise_signal)

        # Reproducir ambos audios
        os.system(f"start {voice_file}")
        os.system(f"start {noise_file}")
        messagebox.showinfo("Éxito", f"Voz guardada en: {voice_file}\nRuido guardado en: {noise_file}")

    def plot_signals(self, original, voice, noise):
        plt.figure(figsize=(12, 8))

        plt.subplot(3, 1, 1)
        plt.plot(original, color='gray')
        plt.title("Señal Original")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")

        plt.subplot(3, 1, 2)
        plt.plot(voice, color='blue')
        plt.title("Señal de Voz Filtrada")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")

        plt.subplot(3, 1, 3)
        plt.plot(noise, color='red')
        plt.title("Señal de Ruido Separada")
        plt.xlabel("Muestras")
        plt.ylabel("Amplitud")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceNoiseSeparator(root)
    root.mainloop()
