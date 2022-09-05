from engines.engine_tests import run_tests
from database.db import db_handler
from engines.utils import clear_assets_folder

if __name__ == "__main__":
    clear_assets_folder()
    db_handler.start_terminate_all_active_sessions()
    run_tests()