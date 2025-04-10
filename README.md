#Group Chat Project
##Installation Guide
To install this group chat application, simply clone this repository onto your local device and follow the run instructions below

##Run Instructions
1. First verify that you have python installed on your device
2. Open your command prompt and navigate to this repository
3. enter the commmand: "pip install tkinter" to install the tkinter library locally (this is used for the graphical interface)
4.  To startup the server, enter the command: "python3 GC-Server.py"
5.  To open a client application, enter the command: "python3 GC-Client.py" (Server must be running before launching the client)

##Client Guide

###Startup/Username
When you first open a client application, it will prompt you to enter your name, this will serve as your display name when sending messages to other users.
If you choose to not enter a name, it will assign you a guest profile. If the application closes after entering your username, then the client application was
unable to connect to the host server. 

###Sending Messages
To send a message, type up to two lines of text into the labeled input box. When you are finished typing your message, hit the green send button.
The message should pop up next to your name on a new line in the message board.

###Recieving Messages
To view messages sent to the groupchat, simply look at the message board window. The window will automatically scroll to show the most recent messages as they are added. However, if you would like to look at previous messages you can simply use the scroll bar on the right to scroll back.

