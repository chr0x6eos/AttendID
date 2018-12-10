:main
set /p path=Enter name of picture to use:
C:\Python27\python.exe detect_ext.py test_data/%path% haarcascade_frontalface_default.xml
goto main