[Setup]
AppName=CriderGPT Offline
AppVersion=1.0.0
AppPublisher=Jessie Crider
AppPublisherURL=https://cridergpt.com
DefaultDirName={pf}\CriderGPT
DefaultGroupName=CriderGPT
OutputDir=dist
OutputBaseFilename=CriderGPT_Offline_Setup
SetupIconFile=ui\assets\cridergpt.ico
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\CriderGPT_Offline.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "offline_ui\build\*"; DestDir: "{app}\ui"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\CriderGPT Offline"; Filename: "{app}\CriderGPT_Offline.exe"; IconFilename: "{app}\ui\assets\cridergpt.ico"
Name: "{commondesktop}\CriderGPT Offline"; Filename: "{app}\CriderGPT_Offline.exe"; IconFilename: "{app}\ui\assets\cridergpt.ico"

[Run]
Filename: "{app}\CriderGPT_Offline.exe"; Description: "Launch CriderGPT Offline"; Flags: nowait postinstall skipifsilent
