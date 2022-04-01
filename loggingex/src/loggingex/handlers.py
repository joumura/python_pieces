import logging
import logging.handlers
import os
import time


class MyTimedRotatingFileHandler(logging.handlers.BaseRotatingHandler):
    """
        指定した時間単位でログファイルを分割するログハンドラー

        TimedRotatingFileHandlerと異なり、非常駐プロセスにも対応している。
        例えば、when='D'とすると、ログファイル名に日付が入り、ログが日毎に切り替わる。
            分割単位は、Y, M, D, H, MI が指定可能。
        ログファイル名は、指定された拡張子を維持する。
        古いログファイルを削除する機能は無い。

        @author kazuhiko@jomura.net
        @version 2022.03.17
    """
    WHEN_ITEMS = {'Y': '%Y',
                  'M': '%Y%m',
                  'D': '%Y%m%d',
                  'H': '%Y%m%d%H',
                  'MI': '%Y%m%d%H%M'}

    def __init__(self, filename, when='D', encoding=None, delay=False):
        self.basebaseFilename, self.basebaseFileext\
            = os.path.splitext(filename)
        self.when = when.upper()
        logging.handlers.BaseRotatingHandler.__init__(
            self, self.__make_logfilename(), 'a', encoding, delay)

    def shouldRollover(self, record):
        return self.baseFilename != self.__make_logfilename()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.baseFilename = self.__make_logfilename()
        if not self.delay:
            self.stream = self._open()

    def __make_logfilename(self):
        time_str = time.strftime(self.WHEN_ITEMS[self.when])
        return ''.join(
            [self.basebaseFilename, '.', time_str, self.basebaseFileext])
