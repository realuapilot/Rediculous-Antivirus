param=InputBox("Enter a directory to scan with quotes","Directory")

Dim objShell
Set objShell = WScript.CreateObject("WScript.Shell")
objShell.Run("""scan.exe """ & param)
Set objShell = Nothing