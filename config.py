# setup kafka

def setup_kafka_logging():
    from app import app
    from app.clients.kafka import KafkaLoggingHandler
    kh = KafkaLoggingHandler("localhost", 9092, "YouELP")
    app.logger.addHandler(kh)

WTF_CSRF_ENABLED = True
SECRET_KEY = 'C3489A49C685C85C4D84D1AD12A4F'

