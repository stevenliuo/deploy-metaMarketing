# Setup on Windows 10

- Install Python 3.11
- Allow PowerShell scripts execution: PS> Set-ExecutionPolicy RemoteSigned
- Install TightVNC

# Prepare Virtual Environment

- Copy project to `C:\Opt\PPT_AI\anton-deleeck.web_app_mvp.screenshots`
- Setup Virtual Environment (in powershell):
```
CD C:\Opt\PPT_AI\anton-deleeck.web_app_mvp.screenshots
C:\Users\dataox\AppData\Local\Programs\Python\Python311\python.exe venv venv
. venv\Scripts\activate.ps1
pip install -r requirements.txt
```

# Start

Connect via VNC client.

Execute:
```
CD C:\Opt\PPT_AI\anton-deleeck.web_app_mvp.screenshots
.\start.ps1
```

Note: Don't connect using RDP or the session will be logged out.
