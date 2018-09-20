The following repo is for the Shell Lab Assignment that was given for CS 4375.

WHAT IS THE LAB:

Dr. Freudenthal gave a set of sample code and we needed to figure out how to program a shell that handles the usual commands, redirects, and piping. Further detailed instructions are found in the read me file of the assignment repo here: https://github.com/robustUTEP/os-shell/blob/master/README.md 


ISSUES WITH THE LAB:

This lab was run and compiled using an app called Thonny on a Mac.

There were issues with being able to use the arch1 virtual machine because the permissions weren't set up correctly. I unfortunately couldn't run it there.

Other run issue was on my Mac itself. Thinking that since Mac has python built in, it should run. However, it kept giving a 'module' error meaning that it wasn't reading the python version correctly. I luckily found Thonny in order to actually test my shell and it hasn't given me any problems with testing it.

Another issue is the exit. When I enter exit, it does what it's supposed to; it exits, however, it does not print out the "Good-bye" message that I want, it only prints out an error message given by the system. 

Piping was the category that I struggled the most with getting correct. I currently do not have it working but the code where I attempted to implement it does appear. It doesn't give an error when I pass a command with '|' but it gets stuck and doesn't do anything.

For the "Command Not Found" handler, where I originally placed it, would cause for the error message to appear for almost every command even though the command did appear. It was difficult to figure out how to put that in the right place. The placement of the handler is still uncertain however it has stopped printing out when it isn't supposed to.

I wasn't able to figure out how to keep the shell running even though the file was not found. Usually when the file is not found, it makes the shell end automatically. I believe it has something to do with the "pass" in the for loop where the execution is occurring but there's still uncertainty whether that is the correct solution or not. Commenting out the "pass" does keep the shell running even though the file doesn't exist.
