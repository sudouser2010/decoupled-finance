import os
import pathlib

PORT = 5001
ROOT_FOLDER_PATH = pathlib.Path(__file__).parent.parent.resolve()
BLOCK_DB_LOCATION = os.path.join(ROOT_FOLDER_PATH, 'master_node',
                                 'block_db.json')
STATE_DB_LOCATION = os.path.join(ROOT_FOLDER_PATH, 'master_node',
                                 'state_db.json')
