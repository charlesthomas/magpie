## To Do
### ``web/handler/history.py``
(line 8) This is SUPER broken - it just hangs

(line 9) paginate by using -n y / --skip=x*y

(line 11) get rid of control chars


### ``web/handler/note.py``
(line 9) need to escape strings, b/c somewhere, spaces are breaking stuff

(line 35) this should say "creating" if 'note' == ''


### ``web/server.py``
(line 25) add username/password

(line 26) have default username/password in config file, create reset-password functionality


### ``web/template/base.html``
(line 28) this causes the newbook note button to not work again until a page refresh -->

(line 56) this causes the new note button to not work again until a page refresh -->

######Generated using [todo.md](https://github.com/charlesthomas/todo.md)
