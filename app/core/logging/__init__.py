import os
import yaml
from pathlib import Path
from datetime import datetime
import logging.config

project_dir = Path(__file__).parents[4]
log_dir = os.path.join(project_dir, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

yaml_file_path = os.path.join(os.path.dirname(__file__), "../../resources/properties/logging_handlers_config.yaml")
with open(yaml_file_path, "r") as file:
    config = yaml.safe_load(file)

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
config['handlers']['file']['filename'] = os.path.join(log_dir, f"binscot_api_log_{current_time}.log")
logging.config.dictConfig(config)

logger = logging.getLogger("uvicorn.access")
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
