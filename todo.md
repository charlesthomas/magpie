## To Do
### ``magpie/handler/config.py``
(line 17) need confirm password field?


### ``magpie/handler/note.py``
(line 37) () in the text seems to break this


### ``magpie/handler/search.py``
(line 21) filter out duplicates if the filename is already in the search results

(line 22) this doesn't exclude the .git folder

(line 35) this doesn't play well with colons in filenames


### ``magpie/template/base.html``
(line 33) this causes the newbook note button to not work again until a page refresh -->

(line 76) this causes the new note button to not work again until a page refresh -->


### ``setup.py``
(line 12) add classifiers


### ``utils/email_notes.py``
(line 43) there seems to be a bug where other notes in other notebooks can be deleted

(line 97) add try/except like web to prevent this from failing if there's no change


### ``utils/pdf_scraper.py``
(line 18) figure out why line breaks don't seem to be rendering

######Generated using [todo.md](https://github.com/charlesthomas/todo.md)
