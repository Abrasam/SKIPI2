alt = 0
try:
    with open("gps.txt", 'r') as file:
        data = file.readline()
        data = data.split(",")
        at = int(data[9])
except KeyboardInterrupt:
    raise
except:
    pass
print(alt)
