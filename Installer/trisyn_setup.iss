[Setup]
AppName=TriSyn GUI
AppVersion=1.0
UpdateUninstallLogAppName=False
DefaultDirName={pf}\TriSyn GUI

[Files]
Source: "trisyn_standalone.zip"; DestDir: "{app}"; Flags: deleteafterinstall nocompression
Source: "extract.bat"; DestDir: "{app}"; Flags: deleteafterinstall
Source: "run.bat"; DestDir: "{app}"
Source: "python.ico"; DestDir: "{app}"

[Run]
Filename: "{app}\extract.bat"; Flags: waituntilterminated runminimized
Filename: "{app}\run.bat"; Flags: postinstall runascurrentuser

[Icons]
Name: "{userstartmenu}\TriSyn\TriSyn GUI"; Filename: "{app}\run.bat"; IconFilename: "{app}\python.ico"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\trisyn_standalone"
Type: filesandordirs; Name: "{app}\SimDataImages"
