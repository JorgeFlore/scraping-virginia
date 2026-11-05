import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import subprocess

class PACApiService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PACApiService"
    _svc_display_name_ = "PAC API Service"
    _svc_description_ = "Servicio para mantener la API PAC corriendo"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.process:
            self.process.terminate()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        api_path = os.path.dirname(os.path.abspath(__file__))
        cmd = [sys.executable, os.path.join(api_path, "run_api.py")]
        
        while True:
            try:
                self.process = subprocess.Popen(cmd, cwd=api_path)
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
                if self.process.poll() is not None:
                    continue
            except Exception as e:
                servicemanager.LogErrorMsg(str(e))
                break

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PACApiService)