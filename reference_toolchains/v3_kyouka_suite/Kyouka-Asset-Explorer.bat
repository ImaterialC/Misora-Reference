@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Kyouka Asset Explorer - Priconne Re:Dive Localization Suite

REM Launch Kyouka-Asset-Explorer.py using the newest available Python 3 installation
for %%V in (3.14 3.13 3.12 3.11 3.10) do (
  py -%%V -c "import sys" >nul 2>&1 && (
    py -%%V Kyouka-Asset-Explorer.py %*
    goto :done
  )
)
python Kyouka-Asset-Explorer.py %*

:done
echo.
pause
