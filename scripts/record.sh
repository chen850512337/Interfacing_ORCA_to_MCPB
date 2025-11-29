#!/bin/bash
# Record Multiwfn operations to file for later usage

OUTNAME=operations.in

program_usage(){
cat <<EOF

*****************************************************************
*       Record Multiwfn operations to file for later usage      *
*****************************************************************

Usage: record.sh

- This script records all commands given to Multiwfn into file $OUTNAME
- After quiting Multiwfn, interupt with Ctrl+C
- The command file can then be executed in another job directory:

  Multiwfn < $OUTNAME

- Useful when you need to construct many similar Multiwfn jobs.
- Make sure proper set the Multiwfn environment variables.
- Make sure Multiwfn is in the PATH.

EOF
}

# Check parameters
while [[ $# -gt 0 ]]
do
  case "$1" in
    "-h" | "-help" | "--help" ) program_usage ; exit 1 ;;
    *  ) program_usage ; exit 1 ;;
  esac
done

tee $OUTNAME | Multiwfn
