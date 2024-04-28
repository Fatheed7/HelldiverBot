$activateScript = Join-Path -Path .\env\Scripts -ChildPath 'Activate'
& $activateScript
$pythonScript = Join-Path -Path .\env\Scripts -ChildPath 'pythonw.exe'
& $pythonScript app.py