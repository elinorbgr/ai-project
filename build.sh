gcc -fPIC -I/usr/include/lttoolbox-3.2 -c libltpy.cpp -o libltpy.o
g++ -fPIC -DPIC -shared libltpy.o /usr/lib/liblttoolbox3.so -o libltpy.so
rm libltpy.o
