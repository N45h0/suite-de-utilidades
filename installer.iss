[Setup]
AppName=Suite de Utilidades
AppVersion=1.0
DefaultDirName={commonpf}\SuiteUtilidades
DefaultGroupName=Suite de Utilidades
UninstallDisplayIcon={app}\main_app\main_app.exe
OutputDir=dist
OutputBaseFilename=SuiteUtilidadesSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=gui\icons\logosuitedeproductividad.ico

[Files]
Source: "gui\dist\main_app\*"; DestDir: "{app}\main_app"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "gui\dist\icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Suite de Utilidades"; Filename: "{app}\main_app\main_app.exe"; IconFilename: "{app}\icons\logosuitedeproductividad.ico"
Name: "{userdesktop}\Suite de Utilidades"; Filename: "{app}\main_app\main_app.exe"; IconFilename: "{app}\icons\logosuitedeproductividad.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"

[Run]
Filename: "{app}\main_app\main_app.exe"; Description: "Iniciar Suite de Utilidades"; Flags: nowait postinstall skipifsilent