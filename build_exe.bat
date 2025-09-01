@echo off
echo ========================================
echo Smart File Organizer - EXE Builder
echo ========================================
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
python -m PyInstaller build_exe.spec

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is located in the 'dist' folder:
echo - SmartFileOrganizer.exe (GUI version - no console)
echo.
echo Users can double-click SmartFileOrganizer.exe to run the tool!
echo.
pause
