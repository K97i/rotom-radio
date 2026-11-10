import unicodedata
from datetime import timedelta

class Song:
    @staticmethod
    def parseTime(self, time: str = ""):
        if len(time) <= 0:
            return ""

        keys = ['seconds', 'minutes', 'hours']
    
        timeParts = map(int, reversed(time.split(':')))
        
        kwargs = dict(zip(keys, timeParts))
        return timedelta(**kwargs)

    def __init__(self, title: str = "", artist: str = "", lastPosition: int = None, hotness: timedelta = timedelta()):
        self.title = title.strip()
        self.artist = artist.strip()
        self.lastPosition = lastPosition
        self.hotness = Song.parseTime(hotness) 

    def _normalize(self, text: str) -> str:
        nfd = unicodedata.normalize('NFD', text)
        no_accents = "".join([c for c in nfd if unicodedata.category(c) != 'Mn'])
        return unicodedata.normalize('NFKC', no_accents).lower()

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False

        return (
            self._normalize(self.title) == self._normalize(other.title) and 
            self._normalize(self.artist) == self._normalize(other.artist)
        )

    def __hash__(self):
        return hash((self._normalize(self.title), self._normalize(self.artist)))

    def to_dict(self):
        return {
            "Title": self.title,
            "Artist": self.artist,
            "Last Position": self.lastPosition,
            "Hotness": str(self.hotness) if self.hotness else "0:00:00",
        }