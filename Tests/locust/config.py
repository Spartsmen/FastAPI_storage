import logging


class Config:
    conf_name = '1_test'
    pacing_sec = 0.1
    api_host = 'http://localhost:8000'


class LogConfig():
    logger = logging.getLogger('demo_logger')
    logger.setLevel('DEBUG')
    file = logging.FileHandler(filename='test_logs.log')
    file.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file)
    logger.propagate = False


logger = LogConfig().logger
cfg = Config()
