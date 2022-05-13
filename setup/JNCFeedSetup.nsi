;--------------------------------
; Includes

  !include "MUI2.nsh"
  !include "logiclib.nsh"

;--------------------------------
;Settings

  !define APPNAME "JNCFeed"
  !define APP_NAME_IN_INSTALLED_DIR "JNCFeed"
  !define COMPANYNAME "Miracutor"
  !define DESCRIPTION "Setup for JNCFeed"
  !define DEVELOPER "Miracutor" #License Holder
  # Files Directory
  !define FILE_DIR "..\dist" #Replace with the full path of install folder
  #!define LOGO_ICON_FILE "..\media\logo.ico"
  !define LICENSE_TEXT_FILE "..\LICENSE"
  #!define SPLASH_IMG_FILE "${FILE_DIR}\splash.bmp"
  #!define HEADER_IMG_FILE "${FILE_DIR}\header.bmp"
  # These three must be integers
  !define VERSIONMAJOR 1	#Major release Number
  !define VERSIONMINOR 1	#Minor release Number
  !define VERSIONBUILD 0	#Maintenance release Number (bugfixes only)
  !define BUILDNUMBER 0		#Source control revision number
  # These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
  # It is possible to use "mailto:" links in here to open email client
  !define HELPURL "https://github.com/Miracutor/JNCFeed/issues"
  !define UPDATEURL "https://github.com/Miracutor/JNCFeed/releases"
  !define ABOUTURL "https://github.com/Miracutor/JNCFeed"
  !define SLUG "${APPNAME} v${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
  SetCompressor /SOLID lzma

;--------------------------------
;General

  ;Name and file
  Name "${APPNAME}"
  OutFile "${APPNAME}-v${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}-dev-Windows-x64-Setup.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES64\${APPNAME}"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\${APPNAME}" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin ;Require admin rights on NT6+ (When UAC is turned on)

;--------------------------------
;Variables

  Var StartMenuFolder

;--------------------------------
; UI
  
  #!define MUI_ICON "..\media\logo.ico"
  #!define MUI_HEADERIMAGE
  #!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\welcome.bmp"
  #!define MUI_HEADERIMAGE_BITMAP "assets\head.bmp"
  !define MUI_ABORTWARNING
  !define MUI_WELCOMEPAGE_TITLE "${SLUG} Setup"

;--------------------------------
; Pages
  
  ; Installer pages
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "${LICENSE_TEXT_FILE}"
  ;!insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY

  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${APPNAME}" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

  !insertmacro MUI_PAGE_INSTFILES
  !define MUI_FINISHPAGE_RUN "$INSTDIR\${APPNAME}.exe"
  !insertmacro MUI_PAGE_FINISH

  ; Uninstaller pages
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
  ; Set UI language
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer section

Section "install"
  # Files for install directory - to build the installer, these should be in the same directory as the install script (this file)
  SetOutPath $INSTDIR
 
  # Add your Files Here
  # Files add here should be removed by the uninstaller (see section "uninstall")
  file "${FILE_DIR}\${APP_NAME_IN_INSTALLED_DIR}.exe"
  file "..\media\logo.ico"
  file "..\LICENSE"
  
  ################################################################################################################

  # Uninstaller - see function un.onInit and section "uninstall" for configuration
  writeUninstaller "$INSTDIR\uninstall.exe"

  SetOutPath $INSTDIR
  # Start Menu
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APP_NAME_IN_INSTALLED_DIR}.exe" "" "$INSTDIR\logo.ico"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\uninstall.lnk" "$INSTDIR\uninstall.exe" "" ""
  
  # Desktop Shortcut
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APP_NAME_IN_INSTALLED_DIR}.exe" "" "$INSTDIR\logo.ico"

  # Registry information for add/remove programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuitUninstallString" "$INSTDIR\uninstall.exe /S"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$INSTDIR\logo.ico"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "${HELPURL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.${BUILDNUMBER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" "${VERSIONMAJOR}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" "${VERSIONMINOR}"
  # There is no option for modifying or reparing the install
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
  # Startup the application on install
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "JNCFeed" '"$InstDir\JNCFeed.exe"'
SectionEnd

;--------------------------------
;Version Information

  VIProductVersion "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.${BUILDNUMBER}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${APPNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "Comments" "${DESCRIPTION}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "${COMPANYNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalTrademarks" "${APPNAME} is a trademark of ${COMPANYNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "${DEVELOPER} | ${COMPANYNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "${APPNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}.${BUILDNUMBER}"

;--------------------------------
;Uninstaller Section

Section "uninstall"
  #Remove Start Menu Launcher
  delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  delete "$SMPROGRAMS\${APPNAME}\uninstall.lnk"
  #Remove Desktop Shortcut
  delete "$DESKTOP\${APPNAME}.lnk"
  #Try to remove the Start Menu folder - this will only happen if it is empty
  rmDir "$SMPROGRAMS\${APPNAME}"

  ################################################################################################################
  #Remove files
  delete $INSTDIR\${APP_NAME_IN_INSTALLED_DIR}.exe
  delete $INSTDIR\logo.ico
  delete $INSTDIR\LICENSE
  
  ################################################################################################################
	
  # ALways delete uninstaller as the last section
  delete $INSTDIR\uninstall.exe

  # Try to remove the install directory - this will only happen if it is empty
  rmDir $INSTDIR

  #Delete installation folder from registry if available - this will only happen if it is empty
  DeleteRegKey /ifempty HKCU "Software\${APPNAME}"

  #Delete startup if available
  DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "JNCFeed"

  # Remove uninstaller information from the registry
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd

;--------------------------------
