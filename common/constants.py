import os
import pathlib

WEBAPP_SERVER_PORT = 5000
BLOCK_CHAIN_SERVER_PORT = 5001
DEVELOPMENT_BLOCK_CHAIN_URL = f'http://localhost:{BLOCK_CHAIN_SERVER_PORT}'

ROOT_FOLDER_PATH = pathlib.Path(__file__).parent.parent.resolve()
BLOCK_DB_LOCATION = os.path.join(ROOT_FOLDER_PATH, 'master_node',
                                 'block_db.json')
STATE_DB_LOCATION = os.path.join(ROOT_FOLDER_PATH, 'master_node',
                                 'state_db.json')
BLOCK_DURATION_IN_SECONDS_LOWER_LIMIT = 60
