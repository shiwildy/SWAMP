#define MyAppName "SWAMP"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "ShiWildy"
#define MyAppURL "https://github.com/shiwildy/SWAMP.git"
#define MyAppExeName "swamp.exe"

[Setup]
AppId={{527E0227-F3E6-4C74-861F-3A64C85AF584}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=C:\{#MyAppName}
DisableDirPage=yes
DisableProgramGroupPage=yes
OutputDir=..\output
OutputBaseFilename=swamp-setup
SetupIconFile=..\etc\logo\LOGO-SWAMP.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\swamp.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\bin\*"; DestDir: "{app}\bin\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\etc\*"; DestDir: "{app}\etc\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\www\*"; DestDir: "{app}\www\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\logs\*"; DestDir: "{app}\logs\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\tmp\*"; DestDir: "{app}\tmp\"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
