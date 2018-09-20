#!/usr/bin/python

import re
import sys
import time
import os
import fileinput

#command = None
file = None
userCommand = ""
args = []
commandFound = True

try:
    while(userCommand != "exit"):  #2
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
        
        #for pipe
        pr,pw = os.pipe()
        for f in (pr, pw):
            os.set_inheritable(f, True)
        
        if 'cd' in userCommand: #4
            inputR = args.index('cd')
            newDir = args[inputR+1:]  #1
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
                
                
                #in case file that is being read has an exec
##                openF = open(args[-1], "r")
##                openOS = os.open(args[-1], os.O_RDONLY)  #6
##                fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
##                dup2(openOS, fd)
##                
                args =  args[:outputR] + args[outputR+1:]
                
            elif 'echo' in userCommand:
                #2
                echoCommand = userCommand.replace(userCommand[:5], '')
                args = ["echo", echoCommand]
                
            elif len(userCommand) == 2:
                #2
                userInput = userCommand.split(" ")
                args = [userInput[0]]
            
            elif 'cd' in userCommand:
                inputR = args.index('cd')
                newDir = args[inputR+1:]
                
            elif '|' in userCommand:               
                os.close(1)                 # redirect child's stdout
                os.dup2(pw)
                for fd in (pr, pw):
                    os.close(fd)
                
                length =len(args)-1
                inputR = args.index('|')
                
                args = [args[:outputR], args[outputR+1:]]
                    
            
            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, args[0])
                #print(args[0])
                try:
                    os.execve(program, args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    commandFound = False
                    #pass                              # ...fail quietly
                
            if commandFound is False:
                if userCommand != 'exit':
                    os.write(2, ("Command not found, try another command!\n").encode())
            
        else:                           # parent (forked ok)
            if '|' in userCommand:
                os.close(0)
                os.dup(pr)
                for fd in (pw, pr):
                    os.close(fd)
            childPidCode = os.wait()
    
    sys.exit(1)
    print("Closing shell. Good-Bye.")
            
except EOFError:
    sys.exit(0)
    print("Closing shell. Good-Bye.") #2
