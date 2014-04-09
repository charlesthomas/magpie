from index import IndexHandler
from history import HistoryHandler
from note import NoteHandler
from notebook import NotebookHandler
from search import SearchHandler

urls = []
urls.append((r'/?', IndexHandler))
# urls.append((r'/?', NotebookHandler))
urls.append((r'/search/?', SearchHandler))
urls.append((r'/(.*)/(.*)/history/?', HistoryHandler))
urls.append((r'/(.+)/(.+)', NoteHandler))
urls.append((r'/(.+)/?', NotebookHandler))
