#!/bin/sh

abort()
{
   local message=${1}

   echo $message
   exit 1
}

MAIN_FILES="configuration library softwares tools README.md"
DESC_FILES="DESC DESC.fr DESC.ja DESC.zh_CN"
MODES="cli gui"
UI_FILES="ui"
PACKAGING_FILES="build/DEPS.main build/POSTINST.sh"

cp ${DESC_FILES} "armbian" &&
mkdir -p "armbian/all" &&
cp ${PACKAGING_FILES} "armbian"

[[ $? -eq 0 ]] || abort "Could copy the basic armbian dependency files"

for mode in ${MODES}
do
	mkdir -p "armbian/all-archs/${mode}/module" &&
	cp -r ${MAIN_FILES} "armbian/all/${mode}/module" &&
	cp "module.${mode}" "armbian/all/${mode}/module/module" &&
	cp "build/DEPS.${mode}" "armbian/all/${mode}"
done

[[ $? -eq 0 ]] || abort "Could not copy the modules content"

cp -r ${UI_FILES} "armbian/all/gui/module"

[[ $? -eq 0 ]] || abort "Could not copy the UI files"
