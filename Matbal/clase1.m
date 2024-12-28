clc;
clear all;
Fs = 3000;
Ts = 1 / Fs;
L = 500;
t = (0:L-1)*Ts;
x=3*sin(2.*pi*50.*t);
v=6*sin(2.*pi*120.*t);
w=4*sin(2.*pi*70.*t);
z = x + v + w ;
y=fft(z);y=abs(z);
%plot(t,z);
subplot(2,1,1),plot(z), title("La suma de Señales"), xlabel("Tiempo[s]"), ylabel("Segundos");
subplot(2,1,2),plot(y), title("Transformada Fourier"), ylabel("Amplitud"), xlabel("Frecuencia[Hz]");