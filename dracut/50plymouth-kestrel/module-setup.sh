#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

check() {
    THEME=kestrel
    [ -e /lib/plymouth/themes/$THEME ] ||
    [ -e /usr/share/plymouth/themes/$THEME ]
}

depends() {
    echo "plymouth"
}

installkernel() {
    return 0
}

install() {

    THEME=kestrel

    # Ubuntu stores themes on /lib/plymouth/themes
    [ -e /lib/plymouth/themes/$THEME ] &&
       THEME_PATH=/lib/plymouth/themes

    # Debian stores themes on /usr/share/plymouth/themes
    [ -e /usr/share/plymouth/themes/$THEME ] &&
       THEME_PATH=/usr/share/plymouth/themes

    PLUGIN_PATH=$(plymouth --get-splash-plugin-path)

    THEME_FILE=${THEME_PATH}/${THEME}/${THEME}.plymouth
    
    [ -d "${THEME_PATH}/${THEME}" ] &&
        for x in ${THEME_PATH}/${THEME}/* ; do
            [ -f "$x" ] && inst $x
        done
    
    MODULE="$(sed -n 's/^ModuleName=\(.*\)/\1/p' ${THEME_FILE}).so"
    [ -e "${PLUGIN_PATH}/${MODULE}" ] &&
        inst ${PLUGIN_PATH}/${MODULE}

    IMAGE_DIR="$(sed -n 's/^ImageDir=\(.*\)/\1/p' ${THEME_FILE})"
    [ -d "${IMAGE_DIR}" ] &&
        for x in ${IMAGE_DIR}/* ; do
            [ -f "$x" ] && inst $x
        done

}
