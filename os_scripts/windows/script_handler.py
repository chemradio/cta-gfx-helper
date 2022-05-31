# tempcode

import interlinks
# v2
class WindowsHandler:
    def __init__(self) -> None:
        from interlinks import cfg
        self.adobe_version_year = cfg['adobe_version']


    def run_script(self, script_code: str):
        import os
        os.system(f'''osascript <<END
        {script_code}\n
        END''')


    def launcher(self):
        return self.run_script(f'''tell application "Adobe After Effects Render Engine (Beta)"
«event miscfile» "{interlinks.path_to_ae_tg_script}"
end tell''')


    def quit_adobe_apps(self):
        return self.run_script('''set myProcesses to {"Adobe After Effects %(year)s", "Adobe Media Encoder %(year)s"} -- The ones to quit.
tell application "System Events"
    repeat with myProcess in myProcesses
        set theID to (unix id of processes whose name is myProcess)
        try
            -- Should stop the application with no dialogs and no items saved.
            do shell script "pkill " & myProcess
        end try
    end repeat
end tell''' % {'year': self.adobe_version_year})


    def quit_ae(self):
        return self.run_script(f'''tell application "System Events"
set theID to (unix id of processes whose name is "Adobe After Effects {self.adobe_version_year}")
try
    -- Should stop the application with no dialogs and no items saved.
    do shell script "pkill " & "Adobe After Effects {self.adobe_version_year}"
end try
end tell''')


    def quit_ame(self):
        return self.run_script(f'''tell application "System Events"
set theID to (unix id of processes whose name is "Adobe Media Encoder {self.adobe_version_year}")
try
    -- Should stop the application with no dialogs and no items saved.
    do shell script "pkill " & "Adobe Media Encoder {self.adobe_version_year}"
end try
end tell''')


    def quit_chrome(self):
        return self.run_script('''tell application "System Events"
set theID to (unix id of processes whose name is "Google Chrome")
try
    -- Should stop the application with no dialogs and no items saved.
    do shell script "pkill " & "Google Chrome"
end try
end tell''')


    def restart_adobe_apps(self):
        return self.run_script('''set myProcesses to {"Adobe After Effects %(year)s", "Adobe Media Encoder %(year)s"} -- The ones to quit.
tell application "System Events"
	repeat with myProcess in myProcesses
		set theID to (unix id of processes whose name is myProcess)
		-- try
		-- Should stop the application with no dialogs and no items saved.
		do shell script "pkill " & myProcess
		-- end try
	end repeat
end tell

delay 5

repeat with myProcess in myProcesses
	tell application myProcess
		activate
	end tell
end repeat''' % {'year': self.adobe_version_year})


    def start_adobe_apps(self):
        return self.run_script('''set myProcesses to {"Adobe After Effects %(year)s", "Adobe Media Encoder %(year)s"} -- The ones to quit.
repeat with myProcess in myProcesses
	tell application myProcess
		activate
	end tell
end repeat''' % {'year': self.adobe_version_year})


    def start_ae(self):
        return self.run_script('''tell application "Adobe After Effects Render Engine (Beta)"
	activate
end tell''')


    def start_ame(self):
        return self.run_script(f'''tell application "Adobe Media Encoder {self.adobe_version_year}"
	activate
end tell''')


# very sophisticated version
# # script texts
# launcher = '''tell application "Adobe After Effects Render Engine (Beta)"
# 	«event miscfile» "/Users/tim/code/cta_quoter_ae_estk/scriptsFolder/Telegram-Automated-Script.jsx"
# end tell'''

# quit_adobe_apps = '''set myProcesses to {"Adobe After Effects %(year)s", "Adobe Media Encoder %(year)s"} -- The ones to quit.
# tell application "System Events"
# 	repeat with myProcess in myProcesses
# 		set theID to (unix id of processes whose name is myProcess)
# 		try
# 			-- Should stop the application with no dialogs and no items saved.
# 			do shell script "pkill " & myProcess
# 		end try
# 	end repeat
# end tell''' % {'year': self.adobe_version_year}

# quit_ae = f'''tell application "System Events"
# 	set theID to (unix id of processes whose name is "Adobe After Effects {self.adobe_version_year}")
# 	try
# 		-- Should stop the application with no dialogs and no items saved.
# 		do shell script "pkill " & "Adobe After Effects {self.adobe_version_year}"
# 	end try
# end tell'''

# quit_ame = f'''tell application "System Events"
# 	set theID to (unix id of processes whose name is "Adobe Media Encoder {self.adobe_version_year}")
# 	try
# 		-- Should stop the application with no dialogs and no items saved.
# 		do shell script "pkill " & "Adobe Media Encoder {self.adobe_version_year}"
# 	end try
# end tell'''

# quit_chrome = '''tell application "System Events"
# 	set theID to (unix id of processes whose name is "Google Chrome")
# 	try
# 		-- Should stop the application with no dialogs and no items saved.
# 		do shell script "pkill " & "Google Chrome"
# 	end try
# end tell'''

# restart_adobe_apps = '''set myProcesses to {"Adobe After Effects %(year)s", "Adobe Media Encoder %(year)s"} -- The ones to quit.
# tell application "System Events"
# 	repeat with myProcess in myProcesses
# 		set theID to (unix id of processes whose name is myProcess)
# 		-- try
# 		-- Should stop the application with no dialogs and no items saved.
# 		do shell script "pkill " & myProcess
# 		-- end try
# 	end repeat
# end tell

# delay 5

# repeat with myProcess in myProcesses
# 	tell application myProcess
# 		activate
# 	end tell
# end repeat''' % {'year': self.adobe_version_year}

# start_adobe_apps = '''set myProcesses to {"Adobe After Effects %(year)s", "Adobe Media Encoder %(year)s"} -- The ones to quit.
# repeat with myProcess in myProcesses
# 	tell application myProcess
# 		activate
# 	end tell
# end repeat''' % {'year': self.adobe_version_year}

# start_ae = '''tell application "Adobe After Effects Render Engine (Beta)"
# 	activate
# end tell'''

# start_ame = f'''tell application "Adobe Media Encoder {self.adobe_version_year}"
# 	activate
# end tell'''


# script_names = ('launcher', 'quit_adobe_apps', 'quit_ae', 'quit_ame', 'quit_chrome',
#             'restart_adobe_apps', 'start_adobe_apps', 'start_ae', 'start_ame',)

# scripts = {sn: globals()[sn]
#     for sn in script_names
# }


# class MacHandler:
#     def __init__(self) -> None:
#         pass


# import inspect
# def run_script(cls):
#     var_name = inspect.stack()[1][4][0].split('.')[1].split('(')[0]
#     script_code = globals()[var_name]
#     import os
#     os.system(f'''osascript <<END
#     {script_code}\n
#     END''')


# for sn, st in scripts.items():
#     setattr(MacHandler, sn, classmethod(run_script))