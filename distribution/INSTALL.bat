@echo off
echo.
echo 🚀 Smart File Organizer - Installation
echo =====================================
echo.
echo This will install Smart File Organizer on your computer.
echo.
echo 📁 Installation Directory: %USERPROFILE%\SmartFileOrganizer
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

:: Create installation directory
mkdir "%USERPROFILE%\SmartFileOrganizer" 2>nul

:: Copy files
echo.
echo 📦 Copying files...
copy /Y "SmartFileOrganizer.exe" "%USERPROFILE%\SmartFileOrganizer\"
copy /Y "USER_GUIDE.md" "%USERPROFILE%\SmartFileOrganizer\"
copy /Y "Run_SmartFileOrganizer.bat" "%USERPROFILE%\SmartFileOrganizer\"

:: Create desktop shortcut
echo.
echo 🖥️  Creating desktop shortcut...
echo [InternetShortcut] > "%USERPROFILE%\Desktop\Smart File Organizer.url"
echo URL=file:///%USERPROFILE%\SmartFileOrganizer\SmartFileOrganizer.exe >> "%USERPROFILE%\Desktop\Smart File Organizer.url"
echo IconFile=%USERPROFILE%\SmartFileOrganizer\SmartFileOrganizer.exe >> "%USERPROFILE%\Desktop\Smart File Organizer.url"
echo IconIndex=0 >> "%USERPROFILE%\Desktop\Smart File Organizer.url"

:: Create Start Menu shortcut
echo.
echo 📝 Creating Start Menu shortcut...
mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Smart File Organizer" 2>nul
echo [InternetShortcut] > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Smart File Organizer\Smart File Organizer.url"
echo URL=file:///%USERPROFILE%\SmartFileOrganizer\SmartFileOrganizer.exe >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Smart File Organizer\Smart File Organizer.url"
echo IconFile=%USERPROFILE%\SmartFileOrganizer\SmartFileOrganizer.exe >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Smart File Organizer\Smart File Organizer.url"
echo IconIndex=0 >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Smart File Organizer\Smart File Organizer.url"

echo.
echo ✅ Installation Complete!
echo.
echo 🎉 You can now find Smart File Organizer in:
echo    • Desktop: Double-click "Smart File Organizer" icon
echo    • Start Menu: Look for "Smart File Organizer"
echo    • Folder: %USERPROFILE%\SmartFileOrganizer
echo.
echo 📖 For help, check USER_GUIDE.md in the installation folder.
echo.
echo Press any key to exit...
pause > nul