set pfn=dekart

CLS
COLOR 1E
ECHO UPDATING...
ECHO.

@echo off
setlocal enabledelayedexpansion

set n=1


:loop
set "bkpfn=bkp-%pfn%-00!n!.zip"
if !n! GEQ 10 set "bkpfn=bkp-%pfn%-0!n!.zip"
if !n! GEQ 100 set "bkpfn=bkp-%pfn%-!n!.zip"

if exist "!bkpfn!" (
    set /a n+=1
    goto :loop
)


7z a "!bkpfn!" *.py

echo 🔁 Backup created: !bkpfn!


