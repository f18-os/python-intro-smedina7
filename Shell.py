#!/usr/bin/python

import re
import sys
import time
import os

#command = None
file = None
userCommand = ""
args = []

while(userCommand != "exit"):

    #Store user input
    userCommand = input("steph-shell$ ")
    args = userCommand.split()
    

    pid = os.getpid()               # get and remember pid
    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
    rc = os.fork()

    #Determine what commands the user wants to run
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:                   # child
        if '>' in userCommand:
            inputR = args.index('>')  #store index of '>'
            file = args[3]
            args = args[:inputR]
            os.close(1)                  #redirect child's stdout
            sys.stdout = open(file, "w")
            fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
            
        elif '<' in userCommand:
            outputR = args.index('<')   #store index of '<'
            args =  args[:outputR] + args[outputR+1:]
            
        elif 'echo' in userCommand:
            echoCommand = userCommand.replace(userCommand[:5], '')
            args = ["echo", echoCommand]
            
        elif userCommand != "exit":
            os.write(2, ("Command not found, try another command!\n").encode())
            #sys.exit(1)
             
    
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly


    else:                           # parent (forked ok)
        childPidCode = os.wait()

sys.exit(1)
print("Closing shell. Good-Bye.")