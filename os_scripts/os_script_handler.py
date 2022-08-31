
import platform
current_system = platform.system()
from os_scripts.mac.script_handler import MacHandler
from os_scripts.windows.script_handler import WindowsHandler

os_script = MacHandler()

if current_system == 'Darwin': # Running on Apple Mac
    os_script = MacHandler()
elif current_system == 'Windows': # Running on Windows
    os_script = WindowsHandler()
else:
    pass
    # raise Exception('Unknown OS. Cannot provide OS Script functionality.')
