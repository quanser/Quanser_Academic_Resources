import sounddevice as sd

print(sd.query_devices())

# 6 Speakers (Quanser Mechatronic S, MME (0 in, 2 out)
info = sd.query_devices(6) 
print(info)

# 16 Speakers (Quanser Mechatronic Sensors Trainer), Windows DirectSound (0 in, 2 out)
info = sd.query_devices(16) 
print(info)

# 20 Speakers (Quanser Mechatronic Sensors Trainer), Windows WASAPI (0 in, 2 out)
info = sd.query_devices(20) 
print(info)


# 49 Speakers (Quanser Mechatronic Sensors Trainer Speaker), Windows WDM-KS (0 in, 2 out)
info = sd.query_devices(49) 
print(info)