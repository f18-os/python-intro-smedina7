#!/usr/bin/python

import re
import sys
import time
import os

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

#Store user input
userCommand = input("Input command: ")
inputCommand = re.split('\s+', userCommand)
print(inputCommand)

command = None
argI = None
file = None

while(inputCommand !=exit):
    if '>' in inputCommand:
        #runs until it has read all the words
        #store in format for '>'
        # command args > file
        command = inputCommand[0]
        #print("Command val: " + command)
        argI = inputCommand[1]
        #print("Args val: " + argI)
        file = inputCommand[3]
        #print("File val: " + file)
    elif '<' in inputCommand:
        #store in format for '<'
        # file < command args
        file = inputCommand[0]
        command = inputCommand[2]
        argI = inputCommand[3]
    
    #Determine what commands the user wants to run
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())
        args = [command, argI]
        os.close(1)                 # redirect child's stdout
        sys.stdout = open(file, "w")
        fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
        
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())
sys.exit(1)
print("Closing shell. Good-Bye.")