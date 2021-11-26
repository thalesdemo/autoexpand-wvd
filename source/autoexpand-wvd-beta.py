from pywinauto import Desktop
import pywinauto.timings
import win32gui # Libs to search procs with noconsole
import os, win32com.client # Libs to remove dup process (such as .exe unpacker)
import logging, tempfile, traceback, sys
import time
import argparse
from getpass import getuser

# Input params
ButtonName = 'Show Details '
defaultLogPath = tempfile.gettempdir() + '\\' + 'autoexpand-wvd.log'
current_user = getuser()
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--appsuffix', default=' Apps', help='name of the workspace suffix (default = <space>Apps)')
parser.add_argument('-i', '--interval',  default='3.0', help='scan interval in seconds (default = 3.0)', type=float)
parser.add_argument('-l', '--logpath',   default=defaultLogPath, help='custom debug log path, default = %%temp%%\\autoexpand-wvd.log')
parser.add_argument('-d', '--debug',     action='store_true', help='set switch to enable debugging (default = disabled)')
parser.add_argument('-s', '--safemode',  action='store_true', help='set switch to turn off app process checks + termination (default = disabled)')
args = parser.parse_args()

# Logging 
if(args.debug):
	FORMAT = '%(asctime)-15s | ' + current_user + ' | %(levelname)s | %(message)s'
	logging.basicConfig(filename=args.logpath, filemode='a', format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug('<>'*30 + '\n%s', args)

# Remove bootloader process	

if args.safemode:
	logger.debug('Safe mode enabled.')
else:
	proc_name = os.path.basename(sys.argv[0])
	my_pid = os.getpid()
	wmi = win32com.client.GetObject('winmgmts:')
	all_procs = wmi.InstancesOf('Win32_Process')
	
	for proc in all_procs:
		procName = proc.Properties_("Name").Value
		if procName == proc_name:
			procOwner = proc.ExecMethod_('GetOwner').Properties_('User').Value
			if procOwner == current_user:
				proc_pid = proc.Properties_("ProcessID").Value
				if proc_pid != my_pid:
					os.kill(proc_pid, 9)
					logger.debug('Cleaned up process, %s (pid %s)', str(procName), str(proc_pid))

# Handler to find window in running procs
def winEnumHandler( hwnd, ctx ):
	global FoundAppWindow
	if win32gui.IsWindowVisible( hwnd ):
		if win32gui.GetWindowText( hwnd ).endswith( args.appsuffix ):
			FoundAppWindow = win32gui.GetWindowText( hwnd )

logger.debug("App started.")
while(True):
	time.sleep(args.interval)
	try:
		FoundAppWindow = None
		win32gui.EnumWindows( winEnumHandler, None ) # sets FoundAppWindow 
		if FoundAppWindow:	
			logger.debug('Found window: %s', FoundAppWindow)
			# WindowSpecifications
			dlg = Desktop(backend="uia").window(title=FoundAppWindow)
			buttonCtrl = dlg.window(title=ButtonName, control_type='Button')
			if dlg.is_enabled():
				logger.debug('Ready window.')
				if buttonCtrl.exists( timeout=0 ):
					if buttonCtrl.is_enabled():
						logger.debug('Button enabled.')
						buttonCtrl.click()
						#todo: focus window to improve chall-response 

	except Exception as e:		
		logger.debug('Error type: %s', str(e.__class__.__name__))
		logger.debug(e)
		logger.debug(traceback.format_exc())
		logger.debug('General exception. Sleep 5 seconds.')
		time.sleep(5)