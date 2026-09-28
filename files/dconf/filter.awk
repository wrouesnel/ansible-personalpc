# Filter `dconf dump` keyfile output, dropping keys whose full path matches
# the `exclude` regex (e.g. /org/cinnamon/command-history). Sections left
# with no keys are dropped too.
#
#   dconf dump / | awk -v exclude='^/org/cinnamon/command-history$' -f filter.awk

function flush() {
    if (nkeys > 0) {
        if (printed) print ""
        print header
        for (i = 1; i <= nkeys; i++) print keys[i]
        printed = 1
    }
    nkeys = 0
}

/^\[.*\]$/ {
    flush()
    header = $0
    section = substr($0, 2, length($0) - 2)
    next
}

/^[^=]+=/ {
    path = "/" section "/" substr($0, 1, index($0, "=") - 1)
    if (exclude == "" || path !~ exclude) keys[++nkeys] = $0
    next
}

END { flush() }
