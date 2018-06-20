# Load a file in a running Leo session from the command line.

TYPE=@auto

if [ "$1" == "--ask" ]; then
    curl --silent --show-error http://localhost:8130/_/exec/commanders/ | cat -n
    echo
    shift
    read -p "Select outline: " WHICH
    WHICH=$[WHICH-1]
else
    WHICH=0
fi

if [ "$1" == "--use" ]; then
    shift
    TYPE="$1"
    shift
fi

FILE="$1"

docmd () {
    CMD="curl --silent --show-error --get --data-urlencode c=$WHICH"
    for i in "$@"; do
        CMD="$CMD --data-urlencode \"cmd=$i\""
    done
    CMD="$CMD http://localhost:8130/_/exec/"
    eval $CMD
}

HEAD="$TYPE $FILE"

nd=$(docmd "nd = g.findNodeAnywhere(c, '$HEAD')" "bool(nd)")
if [ "$nd" == 'False' -o "$nd" == 'None' ]; then
    nd=$(docmd "nd = g.findTopLevelNode(c, 'Edits')" "bool(nd)")
    if [ "$nd" == 'False' -o "$nd" == 'None' ]; then
        docmd "nd = c.rootPosition().insertAfter()" "nd.h = 'Edits'"
    fi;
    docmd "nd = nd.insertAsNthChild(0)" \
          "nd.h = '$HEAD'" \
          "c.selectPosition(nd)" \
          "c.k.simulateCommand('refresh-from-disk')" >/dev/null
fi;
docmd "c.selectPosition(nd)" "c.redraw()" >/dev/null
