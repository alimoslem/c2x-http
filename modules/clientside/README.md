# Client Side Scripts

Client side scripts will be stored in this directory

Web Interface
----

![CreateScript_sc](https://user-images.githubusercontent.com/61124903/130274826-c88fd4d1-b835-44e7-aac6-874ebcbe88f7.png)

After you have created script it will be in root of project.

Available Languages
----
- Python
- Go

Python
----
    Run the bot_script.py with python3 in target system
    you nead requests python library installed on target for running script
    python3 bot_script.py


Other instructions for Python client-side script [here](https://github.com/nxenon/c2x-http-client-py) 

Go
----
    For go lang you have to first compile the code created
    You have to first install Go version 1.13
    if you want the client to run in
    Linux :
    GOOS=linux go build bot_script.go
    Windows :
    GOOS=windows go build bot_script.go
    now you have c2x-http-client compiled.
    run it in target system and wait to connect to c2x server

GO client script does not work when you are using HTTPS protocol if you are using self-signed certificate for C2X-HTTP server.

Other instructions for GO client-side script [here](https://github.com/nxenon/c2x-http-client-go) 
