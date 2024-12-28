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
        """
        Inicializa la clase del separador de voz y ruido, configurando los
        atributos principales y llamando a la función para crear la interfaz.
        """
        self.root = root
        self.root.title("Separador de Voz y Ruido")
        self.audio_data = None  # Almacenará los datos del audio procesado
        self.samplerate = 44100  # Frecuencia de muestreo predeterminada
        self.is_recording = False  # Estado de grabación
        self.frames = []  # Almacenará los datos grabados
        self.audio_file = None  # Ruta del archivo de audio
        self.setup_ui()  # Configura la interfaz de usuario

    def setup_ui(self):
        """
        Configura los elementos de la interfaz gráfica, como botones y etiquetas.
        """
        self.root.configure(bg="#1e1e1e")  # Activar modo oscuro
        self.root.geometry("1200x650")  # Tamaño de la ventana

        # Imagen de fondo
        self.bg_image = tk.PhotoImage(file="Fourier-Fondo.png")  # Archivo de imagen
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Título de la aplicación
        tk.Label(self.root, text="Separador de Voz y Ruido", font=("Arial", 20, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=20)

        # Contenedor de botones
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=20)

        # Botones con sus respectivos comandos
        button_style = {"font": ("Arial", 12), "bg": "#444444", "fg": "white", "relief": "flat", "width": 18}
        tk.Button(button_frame, text="Importar Audio", command=self.import_audio, **button_style).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Iniciar Grabación", command=self.start_recording, **button_style).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Parar Grabación", command=self.stop_recording, **button_style).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(button_frame, text="Separar Voz y Ruido", command=self.separate_voice_noise, **button_style).grid(row=0, column=3, padx=10, pady=5)

    def import_audio(self):
        """
        Permite al usuario importar un archivo de audio para procesar.
        Convierte audio estéreo a mono si es necesario.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if not file_path:
            return
        self.audio_file = file_path
        self.audio_data, self.samplerate = sf.read(file_path)
        if len(self.audio_data.shape) > 1:
            self.audio_data = np.mean(self.audio_data, axis=1)  # Convertir a mono
        messagebox.showinfo("Éxito", "Audio importado correctamente.")

    def start_recording(self):
        """
        Inicia la grabación de audio utilizando PyAudio.
        """
        self.is_recording = True
        self.frames = []
        threading.Thread(target=self.record_audio).start()
        messagebox.showinfo("Grabación", "Grabando... Presiona 'Parar Grabación' para finalizar.")

    def record_audio(self):
        """
        Captura el audio del micrófono y lo almacena en bloques.
        """
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
        """
        Detiene la grabación de audio.
        """
        self.is_recording = False

    def separate_voice_noise(self):
        """
        Separa la señal de voz y ruido del audio utilizando la Transformada Rápida de Fourier (FFT).
        Además, imprime en consola la frecuencia dominante de la voz.
        """
        if self.audio_data is None:
            messagebox.showwarning("Error", "Primero importa o graba un audio.")
            return

        # Aplicar FFT para analizar frecuencias
        fft_signal = fft(self.audio_data)
        freqs = fftfreq(len(fft_signal), 1 / self.samplerate)
        magnitude = np.abs(fft_signal)

        # Detectar la frecuencia principal de la voz
        voice_mask = (abs(freqs) > 85) & (abs(freqs) < 4000)
        fft_voice = np.zeros_like(fft_signal)
        fft_noise = np.zeros_like(fft_signal)

        # Separar la voz y el ruido
        fft_voice[voice_mask] = fft_signal[voice_mask]
        fft_noise[~voice_mask] = fft_signal[~voice_mask]

        # Reconstruir las señales usando IFFT
        voice_signal = ifft(fft_voice).real
        noise_signal = ifft(fft_noise).real

        # Identificar la frecuencia dominante en la voz
        dominant_freq_index = np.argmax(magnitude[voice_mask])
        dominant_freq = freqs[voice_mask][dominant_freq_index]
        print(f"Frecuencia dominante de la voz: {dominant_freq:.2f} Hz")

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
        """
        Muestra gráficas comparativas de la señal original, la señal de voz y la señal de ruido.
        """
        plt.style.use('dark_background')
        
        plt.figure(figsize=(12, 8))

        # Gráfica de la señal original
        plt.subplot(3, 1, 1)
        plt.plot(original, color='#AAAAAA')  # Gris claro
        plt.title("Señal Original", color='white')
        plt.xlabel("Muestras", color='white')
        plt.ylabel("Amplitud", color='white')
        plt.grid(color='#444444', linestyle='--', linewidth=0.5)

        # Gráfica de la señal de voz
        plt.subplot(3, 1, 2)
        plt.plot(voice, color='#00BFFF')  # Azul claro
        plt.title("Señal de Voz Filtrada", color='white')
        plt.xlabel("Muestras", color='white')
        plt.ylabel("Amplitud", color='white')
        plt.grid(color='#444444', linestyle='--', linewidth=0.5)

        # Gráfica del ruido
        plt.subplot(3, 1, 3)
        plt.plot(noise, color='#FF4500')  # Naranja rojizo
        plt.title("Señal de Ruido Separada", color='white')
        plt.xlabel("Muestras", color='white')
        plt.ylabel("Amplitud", color='white')
        plt.grid(color='#444444', linestyle='--', linewidth=0.5)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceNoiseSeparator(root)
    root.mainloop()
