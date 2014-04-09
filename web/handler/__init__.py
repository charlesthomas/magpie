from index import IndexHandler
from config import ConfigHandler
from login import LoginHandler
from note import NoteHandler
from notebook import NotebookHandler
from search import SearchHandler

urls = []
urls.append((r'/?', IndexHandler))
urls.append((r'/config/?', ConfigHandler))
urls.append((r'/login/?', LoginHandler))
urls.append((r'/search/?', SearchHandler))

# do regex ones last so the others get routed properly
urls.append((r'/(.+)/(.+)', NoteHandler))
urls.append((r'/(.+)/?', NotebookHandler))
