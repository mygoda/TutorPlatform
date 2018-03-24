# -*- coding: utf-8 -*-
import logging, os, re, time, datetime

try:
    import codecs
except ImportError:
    codecs = None


class MyLoggerHandler(logging.FileHandler):
    def __init__(self, filename, when='D', backupCount=0, encoding=None, delay=False):
        dirName, baseName = os.path.split(filename)
        self.prefix = baseName
        self.when = when.upper()
        # S - Every second a new file
        # M - Every minute a new file
        # H - Every hour a new file
        # D - Every day a new file
        # month - Every month a new file
        if self.when == 'S':
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        elif self.when == 'M':
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$"
        elif self.when == 'H':
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}$"
        elif self.when == 'D':
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        elif self.when == 'MONTH':
            self.suffix = "%Y-%m"
            self.extMatch = r"^\d{4}-\d{2}$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)
        self.filefmt = "%s.%s" % (filename, self.suffix)
        self.filePath = datetime.datetime.now().strftime(self.filefmt)
        _dir = os.path.dirname(self.filePath)
        try:
            if os.path.exists(_dir) is False:
                os.makedirs(_dir)
        except Exception:
            print("can not make dirs")
            print("filepath is " + self.filePath)
            pass

        self.backupCount = backupCount
        if codecs is None:
            encoding = None
        self.delay = delay
        logging.FileHandler.__init__(self, self.filePath, 'a', encoding, delay)

    def shouldChangeFileToWrite(self):
        _filePath = datetime.datetime.now().strftime(self.filefmt)
        if _filePath != self.filePath:
            self.filePath = _filePath
            return 1
        return 0

    def doChangeFile(self):
        self.baseFilename = os.path.abspath(self.filePath)
        if self.stream is not None:
            self.stream.flush()
            self.stream.close()
        if not self.delay:
            self.stream = self._open()
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

    def getFilesToDelete(self):
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = self.prefix + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if re.compile(self.extMatch).match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            if self.shouldChangeFileToWrite():
                self.doChangeFile()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


