hex_power = "1F30 4145 09"
hex_reset = "1F30 414F 09"
hex_start = "1F30 4151 09"
hex_stop = "1F30 4150 09"

ba_power = bytes.fromhex(hex_power)
ba_reset = bytes.fromhex(hex_reset)
ba_start = bytes.fromhex(hex_start)
ba_stop = bytes.fromhex(hex_stop)

print(ba_power)