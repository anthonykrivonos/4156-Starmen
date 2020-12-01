#!/bin/bash

# Checkstyle
echo "Running checkstyle."
# shellcheck disable=SC2046
pycodestyle --statistics ./src
echo "done."

# Coverage
echo "Running bug checking."
# shellcheck disable=SC2046
pylint -v -E --ignore=[,models,tst] -j 0 --suggestion-mode=y -e --report=yes upmed-api
echo "done."

# Reporting
echo "Running unit tests."
cd ..
# shellcheck disable=SC2046
python3 -m upmed-api.tst.api.patient_test.patient_test
python3 -m upmed-api.tst.api.hcp_test.hcp_test
python3 -m upmed-api.tst.api.appointment_test.appointment_test
echo "done."
cd upmed-api

# Run server
cd src && gunicorn app:app
