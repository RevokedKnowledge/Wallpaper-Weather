Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c WeatherTimeBat.bat"
oShell.Run strArgs, 0, false