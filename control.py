import socket 
import sys
import pprint
import json

MASTER_IP = "127.0.0.1"
UDP_PORT = 9966 

def single_command(command, site=None, worker=False, response=False): 
    packet = {
            "id": 1235,
            "cmd": command,
            } 
    if site:
        packet["site"] = site
    if worker:
        packet["worker"] = worker
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.bind(("0.0.0.0", 9967)) 
    s.sendto(json.dumps(packet), (MASTER_IP, UDP_PORT)) 
    if response:
        p, addr = s.recvfrom(40960) 
        s.close()
        return json.loads(p)
    else:
        s.close() 


cmd = {
        "start": (2, True),
        "startall": (0, False), 
        "stop": (2, True),
        "stopall": (0, False), 
        "get": (2, True),
        "getall": (0, True)
        } 



def main(): 
    arg1 = sys.argv[1] 
    if arg1 in cmd:
        nargs, res = cmd[arg1] 
        if res:
            res = single_command(arg1,
                    *sys.argv[2:2+nargs],
                    response = True)
            pprint.pprint(res)
        else:
            single_command(arg1, 
                    None, None,
                    False)
    else:
        print """ 
        avaiable command:
            start
            startall
            stop
            stopall
        """


if __name__ == "__main__":
    main()


