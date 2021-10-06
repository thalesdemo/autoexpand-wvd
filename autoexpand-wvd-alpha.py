from pywinauto import Desktop
import pywinauto.timings
import win32gui # Libs to search procs with noconsole
import os, win32com.client # Libs to remove dup process (.exe unpacker)
import logging, tempfile, traceback, sys
import time
import argparse
from getpass import getuser

# Input params
defaultLogPath = tempfile.gettempdir() + '\\' + 'autoexpand-wvd.log'
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--appname',  default='SDC Apps', help='name of the application window (default = SDC Apps)')
parser.add_argument('-i', '--interval', default='3.0', help='scan interval in seconds (default = 3.0)', type=float)
parser.add_argument('-l', '--logpath',  default=defaultLogPath, help='custom debug log path, default = %%temp%%\\autoexpand-wvd.log')
parser.add_argument('-d', '--debug',    action='store_true', help="enable debugging (default = disabled)")
args = parser.parse_args()

# Logging 
if(args.debug):
	FORMAT = '%(asctime)-15s | ' + getuser() + ' | %(levelname)s | %(message)s'
	logging.basicConfig(filename=args.logpath, filemode='a', format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug('<>'*30 + '\n%s', args)

# Remove bootloader process	
proc_name = os.path.basename(sys.argv[0])
my_pid = os.getpid()
wmi = win32com.client.GetObject('winmgmts:')
all_procs = wmi.InstancesOf('Win32_Process')

for proc in all_procs:
   if proc.Properties_("Name").Value == proc_name:
        proc_pid = proc.Properties_("ProcessID").Value
        if proc_pid != my_pid:
            os.kill(proc_pid, 9)

# Handler to find window in running procs
def winEnumHandler( hwnd, ctx ):
	global FoundAppWindow
	if win32gui.IsWindowVisible( hwnd ):
		if win32gui.GetWindowText( hwnd ) == args.appname:
				FoundAppWindow = True

# WindowSpecifications
ButtonName = 'Show Details '
dlg = Desktop(backend="uia").window(title=args.appname)
buttonCtrl = dlg.window(title=ButtonName, control_type='Button')

logger.debug("App started.")
while(True):
	time.sleep(args.interval)
	try:
		FoundAppWindow = False
		win32gui.EnumWindows( winEnumHandler, None ) # sets FoundAppWindow 
		if FoundAppWindow:	
			logger.debug('Found window.')
			if dlg.is_enabled():
				logger.debug('Window is ready.')
				if buttonCtrl.exists(timeout=0):
					if buttonCtrl.is_enabled():
						logger.debug('Button exists & enabled.')
						buttonCtrl.click()

	except Exception as e:		
		logger.debug('Error Type: %s', str(e.__class__.__name__))
		logger.debug(e)
		logger.debug(traceback.format_exc())
		logger.debug('General exception. Pause 5 seconds.')
		time.sleep(5)