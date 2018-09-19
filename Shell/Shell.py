#!/usr/bin/python

import re
import sys
import time
import os

#command = None
file = None
userCommand = ""
args = []

try:
    while(userCommand != "exit"):
        try:
            envCommand = os.environ['ps1']
            
        except:
            osEn = False
        
        
        if osEn is False:
            envCommand = ("$ ")

    #Store user input
 #   userCommand = input("steph-shell$ ")
        userCommand = input(envCommand)
        #print(userCommand)
        args = userCommand.split(" ")
        #print(args)
        
        if 'cd' in userCommand:
            inputR = args.index('cd')
            newDir = args[inputR+1:]
            try:
                os.chdir(os.path.expanduser(newDir[0]))
                
            except FileNotFoundError:
                os.write(2, ("Try another command!\n").encode())
                pass
        pid = os.getpid()               # get and remember pid
        rc = os.fork()
        #Determine what commands the user wants to run
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
            
        elif rc == 0:                   # child
            if '>' in userCommand:
                length =len(args)-1
                inputR = args.index('>')  #store index of '>'
                file = args[length]
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
                
            elif len(userCommand) == 2:
                userInput = userCommand.split(" ")
                args = [userInput[0]]
            
            elif 'cd' in userCommand:
                inputR = args.index('cd')
                newDir = args[inputR+1:]
            
            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, args[0])
                #print(args[0])
                try:
                    os.execve(program, args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    os.write(2, ("Command not found, try another command!\n").encode())
                    pass                              # ...fail quietly
        else:                           # parent (forked ok)
            childPidCode = os.wait()
        
    sys.exit(0)
            
except EOFError:
    sys.exit(0)
    print("Closing shell. Good-Bye.")
