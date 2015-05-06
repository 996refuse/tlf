import os

import sys
import signal 

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    base = "/proc"
    arg = sys.argv[1] 
    for i in os.listdir(base): 
        try:
            pid = int(i)
        except:
            continue 
        try:
            line = open(os.path.join(base, i, "cmdline")).read()
        except:
            continue 
        comm = open(os.path.join(base, i, "comm")).read() 
        if "python" not in comm: 
            continue
        if "kill_worker" in line:
            continue
        if arg in line: 
            try:
                os.kill(int(i), signal.SIGTERM) 
            except OSError as e:
                print e 

