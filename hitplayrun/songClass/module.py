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
        self.title = title
        self.artist = artist
        self.lastPosition = lastPosition
        self.hotness = Song.parseTime(hotness) 

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        return self.title.lower() == other.title.lower() and self.artist.lower() == other.artist.lower()

    def __hash__(self):
        return hash((self.title.lower(), self.artist.lower()))

    def to_dict(self):
        return {
            "Title": self.title,
            "Artist": self.artist,
            "Last Position": self.lastPosition,
            "Hotness": str(self.hotness) if self.hotness else "0:00:00",
        }