import logging

from microblog.app.clients.kafka import KafkaLoggingHandler

class Logger:
    def __init__(self):
        kh = KafkaLoggingHandler("localhost", 9092, "test_log")
        #OR
        #kh = KafkaLoggingHandler("localhost", 9092, "test_log", "key1")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(kh)

    def get(self):
        return self.logger

