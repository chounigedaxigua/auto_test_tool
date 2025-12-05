CC=g++
CFLAGS=-I. -L. -lcontrolcan -pthread
LDFLAGS=-L. -lcontrolcan

#g++  -o main main.cpp -I. -L. -lcontrolcan

main: main.o
	$(CC) $(LDFLAGS) -o main main.o

main.o: main.cpp controlcan.h
	$(CC) $(CFLAGS) -c main.cpp 

clean:
	rm -f main main.o  