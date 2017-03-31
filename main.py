import msvcrt as m
import ucamii

cam = ucamii.UCamII("COM11")

for i in range(1, 10):
    print("Switch power OFF and ON... and press any key.") 
    m.getch()
    
    print("Trying to SYNC...")
    
    sync_cycles = cam.sync()
    if sync_cycles>0:
        print("SYNC cycles: " + str(sync_cycles) + "\n")
    else:
        print("FAIL !!!\n")