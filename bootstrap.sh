# See: https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
# Note: you can't refactor this out: its at the top of every script so the scripts can find their includes.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

function log() {
  echo "$*" 1>&2
}

function fatal() {
  echo "$*" 1>&2
  exit 1
}

# Run-once script to setup Ansible before it's ready.

if ! sudo apt update; then
  fatal "apt update failed"
fi


if ! sudo apt install -u python3-pip; then
  fatal "python3-pip installation failed"
fi

if ! pip install uv ; then
  fatal "Failed to install uv"
fi
