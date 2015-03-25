#-*- encoding=utf8 -*-

import pyrant
import pdb
import sys

tt = pyrant.Tyrant(host='192.168.1.168', port=11261)

getcrc = lambda sid, crc: tt.get(str(crc)+"-"+str(sid))

if __name__ == '__main__':
        print(getcrc(sys.argv[1], sys.argv[2]))
