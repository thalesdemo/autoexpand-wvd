# autoexpand-wvd
 Automatically expand the screen ("Show Details") while connecting to Remote Desktop (for Windows Virtual Desktop).

## author
 Cina Shaykhian <cina.shaykhian@thalesgroup.com>

## version
 beta - 2021.10.06

## Table of contents
* [Overview](#overview)
* [Setup](#setup)
* [Source code](#source-code)

## Overview
This demo tool can be deployed to better streamline user experience in being prompted to enter their multi-factor authentication factor without having to click on the 'Show Details' button of the RDP connection. It can be useful in scenarios where the published applications, or session hosts, are secured with the SafeNet Windows Logon agent.

The executable must be installed on the user's Windows machines that are initating the Remote Desktop apps. A Windows task scheduler can be set to automatically launch this app once the user logs in to his machine.

The tool will continuously run in the background without any console window, or logs unless turned on by passing an argument in the command line.

![example.gif](https://github.com/thalesdemo/autoexpand-wvd/blob/main/example.gif)

## Setup

Double-click on the executable, or run with any combination of the arguments below:

###### Syntax:

```
usage: autoexpand-wvd-beta.exe [-a APPNAME] [-i INTERVAL] [-l LOGPATH] [-d] [-s]

optional arguments:
  -a APPNAME, --appname APPNAME
                        name of the application window (default = SDC Apps)
  -i INTERVAL, --interval INTERVAL
                        scan interval in seconds (default = 3.0)
  -l LOGPATH, --logpath LOGPATH
                        custom debug log path, default = %temp%\autoexpand-wvd.log
  -d, --debug           set switch to enable debugging (default = disabled)
  -s, --safemode        set switch to turn off app process checks + termination (default = disabled)
```


## Source code
To compile your own executable, install Python and Pipenv, then follow these steps.

After cloning this repository, run in sequence :
> `make install`
>
> `make`

To clean and start over :
> `make clean`
