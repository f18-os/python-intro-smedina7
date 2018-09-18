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
    rc = os.fork()

    #Determine what commands the user wants to run
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:                   # child
        if '>' in userCommand:
            length = len(args)-1
            inputR = args.index('>')  #store index of '>'
            file = args[length]
            args = args[:inputR]
            os.close(1)                  #redirect child's stdout
            sys.stdout = open(file, "w")
            fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
            
        elif '<' in userCommand:
            #discussed concatination with Alex Melendez
            outputR = args.index('<')   #store index of '<'
            args =  args[:outputR] + args[outputR+1:]
            
        elif 'echo' in userCommand:
            #discussed echo with Elizardo Baeza
            echoCommand = userCommand.replace(userCommand[:5], '')
            args = ["echo", echoCommand]

        elif len(userCommand) == 2:
            userInput = userCommand.split(" ")
            args = [userInput[0]]
            
            
        elif userCommand != "exit":
            os.write(2, ("Command not found, try another command!\n").encode())
            #sys.exit(1)
        
        elif '|' in userCommand:
            inputR = args.index('|')
            length = len(args)-1
            firstCommand = args[:inputR]  #left side of pipe
            secondCommand = args[inputR+1:]  #right side of pipe
            args = [firstCommand, secondCommand]  #store the two commands into list
            
            file = args[length]
            os.close(1)                  #redirect child's stdout
            sys.stdin = open(args[0], "r")
            fd = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
    
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[1])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly


    else:                           # parent (forked ok)
        childPidCode = os.wait()

sys.exit(1)
print("Closing shell. Good-Bye.")