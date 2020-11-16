#!/usr/bin/env bash

# Ignore checking errors
exec 2>/dev/null

TS=$(date +%s)
FLDR="report-${TS}"
function header {
    echo "============ upmed-web $1 Report Generated on ${TS} ============"
    echo $'\n\n'
}

# Create output folder
mkdir "reports"
mkdir "reports/${FLDR}"

# Coverage and unit
echo "Writing coverage and unit testing report to reports/${FLDR}/coverage.txt."
echo $(header "Coverage and Unit") >> "reports/${FLDR}/coverage.txt"
yarn test >> "reports/${FLDR}/coverage.txt"
echo "Done."

# Styling
echo "Writing styling report to reports/${FLDR}/styling.txt."
echo $(header "Styling") >> "reports/${FLDR}/styling.txt"
yarn soft-format >> "reports/${FLDR}/styling.txt"
echo "Done."

# Linting
echo "Writing linting report to reports/${FLDR}/linting.txt."
echo $(header "Linting") >> "reports/${FLDR}/linting.txt"
yarn soft-lint >> "reports/${FLDR}/linting.txt"
echo "Done."

# Linting
echo "Writing bug report to reports/${FLDR}/bugs.txt."
echo $(header "Bug") >> "reports/${FLDR}/bugs.txt"
yarn bugs >> "reports/${FLDR}/bugs.txt"
echo "Done."

echo "Finished writing reports."

exit 0
