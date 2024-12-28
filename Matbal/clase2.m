clc; clear all;
t=0:0.1:10;
a=0;
for n=1:100 %ir cambiando de 5 a 7 a 100
    a=a+(2/pi)*[(-(-1)^n+1)/n].*sin(n.*t);
    
end
plot(t,a);