import logging
import os
import sys
from datetime import datetime


def _isDocker() -> bool:
    path = "/proc/self/cgroup"
    return os.path.exists("/.dockerenv") or (
        os.path.isfile(path) and any("docker" in line for line in open(path))
    )


def _streamSupportsColor(stream) -> bool:
    if "PYCHARM_HOSTED" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode":
        return True

    is_a_tty = hasattr(stream, "isatty") and stream.isatty()
    if sys.platform != "win32":
        return is_a_tty or _isDocker()

    return is_a_tty and ("ANSICON" in os.environ or "WT_SESSION" in os.environ)


class _ColourFormatter(logging.Formatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m"),
    ]

    FORMATS = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        record.exc_text = None
        return output


class DailyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=0):
        self._filename = filename
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        today = str(datetime.now().date())
        if today != self._filename:
            self.stream.close()
            self.baseFilename = self._filename = os.path.join(
                "logs", today, self.baseFilename.split(os.sep)[-1]
            )
            os.makedirs(os.path.dirname(self._filename), exist_ok=True)
            self.stream = self._open()
        super().emit(record)


class LevelFilter:
    __level: int

    def __init__(self, level=logging.NOTSET):
        self.__level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return not self.__level or record.levelno == self.__level


def setFileHandlers(logger: logging.Logger):
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    today = str(datetime.now().date())

    os.makedirs(f"logs/{today}", exist_ok=True)

    FileOutputHandlerInfo = DailyFileHandler(
        f"logs/{today}/infos.log",
    )
    FileOutputHandlerInfo.setFormatter(formatter)
    FileOutputHandlerInfo.addFilter(LevelFilter(logging.INFO))

    FileOutputHandlerWarn = DailyFileHandler(
        f"logs/{today}/warnings.log",
    )
    FileOutputHandlerWarn.setFormatter(formatter)
    FileOutputHandlerWarn.addFilter(LevelFilter(logging.WARNING))

    FileOutputHandlerError = DailyFileHandler(
        f"logs/{today}/errors.log",
    )
    FileOutputHandlerError.setFormatter(formatter)
    FileOutputHandlerError.addFilter(LevelFilter(logging.ERROR))

    logger.addHandler(FileOutputHandlerInfo)
    logger.addHandler(FileOutputHandlerWarn)
    logger.addHandler(FileOutputHandlerError)


def setupLogging():
    level = logging.INFO
    handler = logging.StreamHandler()
    if isinstance(handler, logging.StreamHandler) and _streamSupportsColor(
        handler.stream
    ):
        formatter = _ColourFormatter()
    else:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
    if os.getenv("ENV") == "production":
        setFileHandlers(logger)
