@echo off
set inPath=input
set outPath=output

for /f %%f in ('dir /b "%inPath%\"') do (
	echo a2l2pid.py %inPath%\%%f pidlist.csv %outPath%\%%~nf.csv
	a2l2pid.py %inPath%\%%f pidlist.csv %outPath%\%%~nf.csv
)

@pause