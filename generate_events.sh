#!/bin/bash

set -eu

function note() {
    echo "[$(tput bold)$(tput setaf 2) INFO $(tput sgr0)] ${*}"
}

function err() {
    echo "[$(tput bold)$(tput setaf 1) ERROR $(tput sgr0)] ${*}"
}

function warn() {
    echo "[$(tput bold)$(tput setaf 3) WARNING $(tput sgr0)] ${*}"
}

function die() {
    echo "$(basename ${0}): ${*}"
    return 1
}

# tput helper
# Taken from: (http://linuxtidbits.wordpress.com/2008/08/11/output-color-on-bash-scripts/)
function tputcolors() {
    echo -e "$(tput bold) reg  bld  und   tput-command-colors$(tput sgr0)"
    for i in $(seq 1 7); do
      echo " $(tput setaf $i)Text$(tput sgr0) $(tput bold)$(tput setaf $i)Text$(tput sgr0) $(tput sgr 0 1)$(tput setaf $i)Text$(tput sgr0)  \$(tput setaf $i)"
      done
    echo ' Bold            $(tput bold)'
    echo ' Underline       $(tput sgr 0 1)'
    echo ' Reset           $(tput sgr0)'
    echo ""
}

function usage() {
cat << EOF
usage: $0 [OPTIONS]

Generate Cinemateca events using scrapy crawler.

OPTIONS:
 -h             Shows this message
 -d             Number of days to generate
 -s             Start date in the format YYYY-MM-DD
EOF
}

function generate() {
    date=${1:-$(date +%Y-%m-%d)}
    file=${2}
    command="scrapy crawl cinemateca -t ujson -a date=${date} -o ${file}"

    if [ -e ${file} ]; then
        rm -f ${file}
    fi

    ${command}
}

while getopts ":hd:s:" OPTION; do
        case ${OPTION} in
                h)
                        usage
                        exit 0
                        ;;
                d)
                        NUMDAYS=${OPTARG}
                        ;;
                s)
                        START=${OPTARG}
                        ;;
                \?)
                        echo "Invalid option: -${OPTARG}" >&2
                        usage >&2
                        exit 1
                        ;;
                :)
                        echo "Option -${OPTARG} requires an argument." >&2
                        usage >&2
                        exit 1
                        ;;

        esac
done

# $ date --date "2013-07-01 10 days" +%Y-%m-%d
# 2013-07-11
START=${START:-$(date +%Y-%m-%d)}
NUMDAYS=${NUMDAYS:-0}
END=$(date --date "${START} ${NUMDAYS:-0} days" +%Y-%m-%d)
echo $END

# activate virtualenv for scrapy
VENV="/srv/venvs/cinemateca-feed/"
SCRAPY="/srv/git/cinemateca-feed/cinemateca_scrapper/"
EVENTS="/var/www/events/"
set +u
source ${VENV}/bin/activate
set -u
cd ${SCRAPY}

for i in $(seq 1 ${NUMDAYS}); do
    date=$(date --date "${START} ${i} days" +%Y-%m-%d)
    echo ${date}
    generate ${date} "${EVENTS}/${date}.json"
done

