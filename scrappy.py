import cv2
import numpy as np
import urllib.request
import time
import threading
import math


# url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/002.png'

def getPokemon(start, end):
    print("Started working for range :", start, "to", end)
    for i in range(start, end):
        try:
            url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/' + \
                  '{:03d}'.format(i) + '.png'
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            binary_str = response.read()
            byte_array = bytearray(binary_str)
            numpy_array = np.asarray(byte_array, dtype="uint8")
            image = cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)
            cv2.imwrite("images/" + '{:04d}'.format(i) + '.png', image)
            print("Saved " + '{:04d}'.format(i) + '.png')
        except Exception as e:
            print(str(e))


start_time = time.time()
thread_count = 8  # Put your thread count here (usually 2*cores)
image_count = 801
thread_list = []

for i in range(thread_count):
    start = math.floor(i * image_count / thread_count) + 1  # 0, 100,
    end = math.floor((i+1) * image_count / thread_count) + 1 # 100, 200
    thread_list.append(threading.Thread(target=getPokemon, args=(start, end)))

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

end_time = time.time()
print("Done")
print("Time taken : " + str(end_time - start_time) + "sec")
