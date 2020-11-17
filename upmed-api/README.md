# upmed-api

## Getting Started

1. Import the `.env` file shared privately within the Starmen team and place it
in the `upmed-api/` directory.
2. Install requirements with `pip3 install -r requirements.txt`.
3. Run `export FLASK_APP=$PWD/src/app.py && export PORT=8080` to add the `FLASK_APP` and `PORT` environment variables.
4. Start the server by running `gunicorn app:app`. Run `export FLASK_DEBUG=true` to enter debugging mode.

## Submitting Code & Deploying

1. `git commit` your changes and `git push` to a non-`main` branch. Prefix your branch with either
    - `feat-` (for feature branches)
    - `wip-` (for work-in-progress branches)
    - or `fix-` (for bug fixes).
2. [Submit a pull request (PR)](https://github.com/anthonykrivonos/4156-Starmen) on GitHub.
3. Have your PR approved by **at least one** other person.
4. Merge your PR into `main`.
5. Your code will be automatically deployed to Heroku.

## Folder Structure

```
src/
    api/
        hcp/
            hcp.py
                - contains all endpoints related to HCPs
        patient/
            patient.py
                - contains all endpoints related to patients
    app.py
        - Web server root
tst/
```
