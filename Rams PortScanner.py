import pyfiglet
import sys
import socket
import getopt
from threading import Thread
from datetime import datetime
  
#cool banner module so it will look like a real tool ;)
banner = pyfiglet.figlet_format("RAM's PORTSCANN")
print(banner)

# the thread will simply scan the port range given,
# todo: implement differant scanning method 
def scanThread(target, portRange):

    portMinMax = portRange.split("-")

    try:
        for port in range(int(portMinMax[0]) - 1, int(portMinMax[1]) ):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target,port))
            if result == 0:
                print("Port {} is open".format(port))
            s.close()
         
    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()
    


def main(argv):
    targetAddress = ''
    portRange = '1-65535' # incase the user doesnt enter a port number
    threadAmount = 100 # increase for better speed
    helptext = '-h : for help \n-t xxx.xxx.xxx.xxx : enter ip address \n-p 1-65535 : enter port range DEFAULT SCAN ALL PORTS\nsafe scanning :D'

    # grab options -h -t -p
    try:
        opts, args = getopt.getopt(argv,"ht:p:",["target=","port="])
    except getopt.GetoptError: 
        print (helptext)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (helptext)
            sys.exit()
        elif opt == '-t':
            targetAddress = arg
        elif opt == '-p':
            portRange = arg

    #splitting the port to string to the min and max
    portMinMax = portRange.split('-')
    
    print("\_(~ - ~)_/" * 4)
    print("Target ip: " + targetAddress)
    print("Port range: " + portRange)
    print("Starting Scan")
    print("-" * 40)

    #creating increments so it will be easy to split into threads
    #and rounding them so we dont get a float
    portIncrements = round( (int( portMinMax[1] ) - int( portMinMax[0])) / threadAmount )

    #divides the port range into small segments for each thread
    for index in range(threadAmount):
        #incase the number we divided isnt a natural number we set the last thread to reach the max port number
        if (index + 1) == threadAmount :
            dividedPortMinMax = str(round (portIncrements * (index + 1) - portIncrements + 1)) + '-' + str(portMinMax[1])
        else:
            dividedPortMinMax = str(round (portIncrements * (index + 1) - portIncrements + 1)) + '-' + str(portIncrements * (index + 1))

        #creating the thread and starting it
        thread = Thread(target = scanThread, args = (targetAddress, dividedPortMinMax))
        thread.start()
    

if __name__ == "__main__":
    main(sys.argv[1:])
