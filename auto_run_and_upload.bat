@echo off
cd /d "C:\Users\SHIVA TIWARI\.gemini\antigravity\scratch\viral_ai_shorts_pipeline"
echo ======================================================== >> auto_upload.log
echo [RUN STARTED] %date% %time% >> auto_upload.log
"C:\Users\SHIVA TIWARI\AppData\Local\Python\pythoncore-3.14-64\python.exe" run_pipeline.py --mode upload --platform all >> auto_upload.log 2>&1
echo [RUN FINISHED] %date% %time% >> auto_upload.log
