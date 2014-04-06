from index import IndexHandler
from note import NoteHandler

urls = []
urls.append((r'/?', IndexHandler))
urls.append((r'/(.*)/(.*)', NoteHandler))
