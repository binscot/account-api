import multiprocessing

from app.core.logging import logger

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
wsgi_app = "app.main:app"
timeout = 60
loglevel = "info"
bind = "0.0.0.0:8000"
max_requests = 1000
max_requests_jitter = 100


def on_starting(server):
    server.log.info("Starting Scheduler...")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢄⡾⣯⢷⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢢⡼⣾⢻⣃⣔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡳⣫⡿⡽⠓⠁⠀⠀⠀⠀⠀⠀⠀⠀⠴⣄⣟⣿⢸⡿⣡⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⢀⣾⡄⠀⠀⢼⢴⢫⣯⢿⠽⠒⠀⡀⡀⡀⡀⡀⠀⠀⠀⠀⣿⢾⡝⡾⣽⠏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⢀⢸⣞⣧⣠⠀⠈⡿⠘⣊⣴⣲⣽⢯⡿⣽⣟⣯⣯⡷⣶⣔⣯⢿⢝⣼⣟⡷⢓⠁⠀⠀⠀⢀⣄⡄⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⡈⣟⣾⢱⣯⡀⢀⣴⢽⣗⣿⣺⣽⢯⣟⣷⣻⣞⣷⣻⢷⡯⣯⣗⣟⣷⢳⠒⣀⠀⢠⣆⡴⣟⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠈⣙⡾⣗⠝⣠⡷⣿⢽⣻⢾⣽⢾⣻⣽⢾⣳⣿⣺⡯⣿⡽⡷⣯⣃⢂⢀⣀⡼⣖⡷⢏⣿⡽⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠈⢽⡻⢰⡫⠉⢝⡿⣽⣟⣾⣻⣽⡞⠉⠩⡺⣷⣻⢷⣟⣿⢽⣺⣫⣛⣎⣯⣵⢾⣻⣓⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠠⠀⠀⠠⠀⠀⠀⠀⠀⠀⣺⢦⡤⣼⢯⡷⣟⣾⣻⣞⣷⢤⣠⣾⣻⢾⣻⣗⡿⣯⠷⢟⢾⢽⠾⠽⠉⢡⡥⣤⣤⣄⠄⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣯⣏⠙⠝⠿⠽⠳⠻⠚⡉⣽⣽⢾⡯⣿⣳⣯⡟⠇⣴⢶⣲⣖⣮⣞⡾⣯⢿⠽⠚⢋⠋⠀⠀⠀⠀⠀⠀⠁")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⣟⣟⡷⣶⢶⣵⢾⣽⣻⣽⢾⡯⣿⡽⡾⠓⣡⢾⡽⣯⢿⣞⣷⢯⡿⣽⣻⣟⡿⣶⢴⣀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠟⠽⠾⡻⠾⠽⠞⠏⠟⣑⣡⢶⣽⢾⣻⣽⢯⣟⣷⣻⣽⣻⡽⣗⣯⡿⣝⠯⡿⣵⠀⠀⠀⠂⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢡⡶⣗⣯⡿⣞⣯⡿⣾⡈⢟⣾⣻⣽⢾⣻⢾⣽⣻⣽⢷⣻⡷⣖⡌⠈⠂⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⢀⠀⠠⠐⠈⠀⡀⠀⠀⡀⠄⠀⠁⠀⢠⣻⣽⢯⢃⠩⠩⠳⡿⣽⣳⠨⣷⣻⢾⣻⣽⣟⣾⣽⢾⣻⡽⣯⢿⡽⣆⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣻⡄⠀⠀⠀⠀⣀⣠⣞⣷⣻⠍⠀⠀⠀⠨⡿⣽⢯⠀⠨⠙⡻⣽⣞⣷⣻⣞⣿⢽⣯⢿⡊⢻⣽⠄⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠁⠀⠀⠀⠀⠀⠘⣷⣻⣄⠀⠀⠀⠩⡗⠻⣮⠛⠝⠆⠀⠀⢨⡿⣽⣻⠀⠀⠀⠀⠨⣳⣯⡷⣟⣾⣟⣾⣻⠀⠈⠞⠅⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⣽⡽⣗⣄⠀⠀⠀⠀⠁⠁⠀⠀⢀⣠⣯⢿⡽⣧⡀⠀⠀⠀⠀⡼⣗⡿⣯⢷⣻⡾⡝⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠈⢾⣻⡽⣯⢷⣤⣀⠀⠀⠀⠀⠀⠋⠃⢿⠝⠹⡏⡙⠀⠀⣀⣴⢿⡯⣟⣯⣿⢽⡯⠁⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢟⣯⡿⣯⢿⣺⡷⣶⢤⣠⣀⡀⡀⡀⡀⣀⣀⣄⣤⣾⣺⣽⢯⣟⣯⡷⡿⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⡀⠀⠀⠀⠀⠀⢀⠀⠄⠀⠀⠀⠕⢿⡽⣯⡷⣿⢽⣯⡷⣿⢽⣯⢿⡽⣗⣿⢽⣾⣳⢿⣺⡿⣽⣳⡟⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⢿⣽⣻⣞⣯⢿⣽⢾⣻⣽⢯⡿⣽⡾⣽⣻⣽⡽⠯⠃⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠓⠏⠿⣽⢾⣻⣽⢾⣻⡽⡷⡟⠯⠛⠈⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈")
    logger.info("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠀⠁⠁⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠁⠀⠀")
    logger.info("  binscot api start")
