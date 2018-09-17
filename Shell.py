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
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())
        if '>' in userCommand:
            inputR = args.index('>')  #store index of '>'
            file = args[3]
            args = args[:inputR]
            os.close(1)                  #redirect child's stdout
            sys.stdout = open(file, "w")
            fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
 #           sys.exit(1)
        elif '<' in userCommand:
            outputR = args.index('<')   #store index of '<'
            args =  args[:outputR] + args[outputR+1:]
 #           sys.exit(1)
        
 #       elif userCommand != "exit":
            
            #sys.exit(1)
             
    
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        os.write(1, ("Command not found, try another command!").encode())
        
 #       sys.exit(1)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                 (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                 childPidCode).encode())
sys.exit(1)
print("Closing shell. Good-Bye.")