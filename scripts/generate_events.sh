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

function debug() {
    if [ ${VERBOSE} -eq 1 ]; then
        echo "[$(tput bold)$(tput setaf 5) DEBUG $(tput sgr0)] ${*}"
    fi
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
 -v             Be verbose
 -S             Scrapy's crawler path
 -P             Path to store events
 -V             Virtualenv path
EOF
}

function generate() {
    local date=${1:-$(date +%Y-%m-%d)}
    local file=${2:-./${date}.json}
    local command="scrapy crawl cinemateca -t ujson -a date=${date} -o ${file}"

    ${command}
}

# next_date date inc
# Returns date in 'inc' days from a specified date 'date'.
function next_date() {
    local date=${1:-$(date +%Y-%m-%d)}
    local inc=${2:-1}

    date --date "${date} ${inc} days" +%Y-%m-%d
}

VERBOSE=0
while getopts ":hvd:s:P:S:V:" OPTION; do
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
                P)
                        EVENTS=${OPTARG}
                        ;;
                S)
                        SCRAPY=${OPTARG}
                        ;;
                V)
                        VENV=${OPTARG}
                        ;;
                v)
                        VERBOSE=1
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

# activate virtualenv for scrapy
VENV=${VENV:-"/srv/venvs/cinemateca-feed/"}
SCRAPY=${SCRAPY:-"/srv/git/cinemateca-feed/cinemateca_scrapper/"}
EVENTS=${EVENTS:-"/var/www/events/"}
set +u
source ${VENV}/bin/activate
set -u
cd ${SCRAPY}

#for i in $(seq 1 ${NUMDAYS}); do
#    date=$(date --date "${START} ${i} days" +%Y-%m-%d)
#    generate ${date} "${EVENTS}/${date}.json"
#done

# $ date --date "2013-07-01 10 days" +%Y-%m-%d
# 2013-07-11
START=${START:-$(date +%Y-%m-%d)}
NUMDAYS=${NUMDAYS:-0}
END=$(date --date "${START} ${NUMDAYS} days" +%Y-%m-%d)
note "Generating events from ${START} to ${END}."

date=${START}
generate ${date} "${EVENTS}/${date}.json"
while [ "${date}" != ${END} ]; do
    generate ${date} "${EVENTS}/${date}.json"
    date=$(next_date ${date} 1)
    debug "Next date: ${date}"
done

