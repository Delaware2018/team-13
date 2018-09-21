'''
    setup.py

    Setup script
'''
import subprocess

# installs python package requirements
subprocess.Popen('pip install -r requirements.txt').wait()