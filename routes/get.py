import logging


def index():
    return "Hello, World!"


def test():
    logging.warning("tets")
    return "Test route"


def hello(test):
    return "Hello, Worzaejkfdospjld!" + test
