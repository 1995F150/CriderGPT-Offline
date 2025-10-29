[Setup]
AppName=CriderGPT Offline
AppVersion=1.0.0
DefaultDirName={autopf}\CriderGPT Offline
DefaultGroupName=CriderGPT Offline
OutputBaseFilename=CriderGPT_Offline_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=offline_ui\public\cridergpt.ico

[Files]
Source: "dist\CriderGPT-Offline.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CriderGPT Offline"; Filename: "{app}\CriderGPT-Offline.exe"
Name: "{userdesktop}\CriderGPT Offline"; Filename: "{app}\CriderGPT-Offline.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CriderGPT-Offline.exe"; Description: "Launch CriderGPT Offline"; Flags: nowait postinstall skipifsilent
