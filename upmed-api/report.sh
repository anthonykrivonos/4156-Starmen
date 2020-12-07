TS=$(date +%s)
FLDR="report-${TS}"
function header() {
    echo "============ upmed-api $1 Report Generated on ${TS} ============"
    echo '\n\n'
}
# Create output folder
mkdir "reports/${FLDR}"

# Checkstyle
echo "Writing checkstyle report to reports/${FLDR}/checkstyle.txt."
# shellcheck disable=SC2046
echo $(header "Checkstyle") >> "reports/${FLDR}/checkstyle.txt"
pycodestyle --statistics ./src >> "reports/${FLDR}/checkstyle.txt"
echo "done."

# Bug Checking
echo "Writing Bug report report to reports/${FLDR}/bugreport.txt."
# shellcheck disable=SC2046
echo $(header "Bug Checking") >> "reports/${FLDR}/bugreport.txt"
pylint -v -E --ignore=[,models,tst] -j 0 --suggestion-mode=y -e --report=yes upmed-api >> "reports/${FLDR}/bugreport.txt"
echo "done."

# Reporting
echo "Writing unit testing report to reports/${FLDR}/test.txt."
cd ..
# shellcheck disable=SC2046
echo $(header "Unit Test") >> "upmed-api/reports/${FLDR}/test.txt"
python3 -m upmed-api.tst.api.patient_test.patient_test 2>> "upmed-api/reports/${FLDR}/test.txt"
python3 -m upmed-api.tst.api.patient_test.patient_endpoint_test 2>> "upmed-api/reports/${FLDR}/test.txt"

python3 -m upmed-api.tst.api.hcp_test.hcp_test 2>> "upmed-api/reports/${FLDR}/test.txt"
python3 -m upmed-api.tst.api.hcp_test.hcp_endpoint_test 2>> "upmed-api/reports/${FLDR}/test.txt"

python3 -m upmed-api.tst.api.appointment_test.appointment_test 2>> "upmed-api/reports/${FLDR}/test.txt"
python3 -m upmed-api.tst.api.appointment_test.appointment_endpoint_test 2>> "upmed-api/reports/${FLDR}/test.txt"

# Coverage Checking
echo "Writing Coverage report to reports/${FLDR}/coverage.txt."
# shellcheck disable=SC2046
echo $(header "Coverage Test") >> "upmed-api/reports/${FLDR}/test.txt"
coverage run -a --branch -m upmed-api.tst.api.patient_test.patient_test 2>> "upmed-api/reports/${FLDR}/coverage.txt"
coverage run -a --branch -m upmed-api.tst.api.patient_test.patient_endpoint_test 2>> "upmed-api/reports/${FLDR}/coverage.txt"
coverage run -a --branch -m upmed-api.tst.api.hcp_test.hcp_test 2>> "upmed-api/reports/${FLDR}/coverage.txt"
coverage run -a --branch -m upmed-api.tst.api.hcp_test.hcp_endpoint_test 2>> "upmed-api/reports/${FLDR}/coverage.txt"
coverage run -a --branch -m upmed-api.tst.api.appointment_test.appointment_test 2>> "upmed-api/reports/${FLDR}/coverage.txt"
coverage run -a --branch -m upmed-api.tst.api.appointment_test.appointment_endpoint_test 2>> "upmed-api/reports/${FLDR}/coverage.txt"
coverage report -m >>"upmed-api/reports/${FLDR}/coverage.txt"


echo "done."

