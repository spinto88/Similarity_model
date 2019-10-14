all:
	gcc -c -fPIC -O3 -Wall -g dynamics.c -o dynamics.o
	gcc -c -fPIC -O3 -Wall -g active_links.c -o active_links.o 
	gcc -shared dynamics.o active_links.o -o libc.so
clean:
	rm -rfv *.o libc.so *.pyc
