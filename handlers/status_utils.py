import time
from datetime import datetime
from database.db import db_handler


dt_secs = lambda secs: time.strftime('%H:%M:%S', time.gmtime(secs))

def get_bot_version_git():
    import glob
    import os
    list_of_files = glob.glob(f"{os.getcwd()}/.git") # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getmtime)
    return datetime.fromtimestamp(int(os.path.getmtime(latest_file)))


def runtime_since_launch() -> tuple[str, str]:
    ct = time.time()
    run_timestamp = db_handler.get_latest_launch_time()
    if not run_timestamp:
        run_timestamp = ct
        db_handler.log_event('run', 'bot_launch')
    net_errs = db_handler.get_errors('network_timeout')

    try:
        last_err_time = net_errs[-1]['timestamp']
    except:
        last_err_time = run_timestamp

    runtime_since_launch = ct - run_timestamp
    runtime_since_error = ct - last_err_time
    return dt_secs(runtime_since_launch), dt_secs(runtime_since_error)