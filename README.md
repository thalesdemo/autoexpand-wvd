# autoexpand-wvd
 Automatically expand the screen ("Show Details") while connecting to Remote Desktop (for Windows Virtual Desktop).

## author
 Cina Shaykhian <cina.shaykhian@thalesgroup.com>

## version
 beta - 2021.11.25

## Table of contents
* [Overview](#overview)
* [Setup](#setup)
* [Source code](#source-code)

## Overview
This demo tool can be deployed to better streamline user experience in being prompted for multi-factor authentication without having the user click on the *Show Details* button in the RDP window. It can be useful in scenarios where the published applications, or session hosts, are secured with the SafeNet Windows Logon agent.

The executable must be installed on every machine where users are initating the Remote Desktop apps (run under the user context). To automate launch on startup, a simple Windows task scheduler can be configured.

This application is portable and does not require admin privilege. It continuously runs in the background without any console window, or for that matter, without logs unless explicitely turned on by passing an argument [-d] in the command line.

![example.gif](https://github.com/thalesdemo/autoexpand-wvd/blob/main/example.gif)

## Setup

Double-click on the executable, or run with any of the optional arguments below:

###### Syntax:

```
usage: autoexpand-wvd-beta.exe [-a APPSUFFIX] [-i INTERVAL] [-l LOGPATH] [-d] [-s]

optional arguments:
  -a APPSUFFIX, --appsuffix APPSUFFIX
                        name of the application window (default = <space>Apps)
  -i INTERVAL, --interval INTERVAL
                        scan interval in seconds (default = 3.0)
  -l LOGPATH, --logpath LOGPATH
                        custom debug log path, default = %temp%\autoexpand-wvd.log
  -d, --debug           set switch to enable debugging (default = disabled)
  -s, --safemode        set switch to turn off app process checks + termination (default = disabled)
```


>__NOTE__
>
>You must match `APPSUFFIX` to the end portion of your Remote App window's title. In this example, `APPSUFFIX` is set to *<space>Apps* since the title is *SDC Apps* (see animated gif).
>
>A WVD admin could always rename this window from CLI:
>
>``Set-RdsRemoteDesktop -TenantName <WVDCompanyTenant> -HostPoolName <WVDHostPool> -AppGroupName "<Desktop App Group>" -FriendlyName "New Name"``
  

## Source code
To compile your own executable, install Python and Pipenv, then follow these steps.

After cloning this repository, run in sequence:
> `make install`
>
> `make`

To clean and start over:
> `make clean`
