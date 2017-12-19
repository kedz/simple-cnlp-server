from .server import start, stop
from .client import annotate

class Session(object):
    def __init__(self, port=9000, memory=4):
        self.port = port
        self.memory = memory

    def __enter__(self):
        start(self.port, memory=self.memory)
        return self

    def annotate(self, text, annotators=["tokenize"]):
        return annotate(text, annotators=annotators, port=self.port)

    def __exit__(self, *args):
        stop(self.port)
