from index import IndexHandler
from history import HistoryHandler
from note import NoteHandler

urls = []
urls.append((r'/?', IndexHandler))
urls.append((r'/(.*)/(.*)/history/?', HistoryHandler))
urls.append((r'/(.*)/(.*)', NoteHandler))
