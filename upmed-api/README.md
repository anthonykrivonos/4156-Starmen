# upmed-api

## Getting Started

1. Import the `.env` file shared privately within the Starmen team and place it
in the `upmed-api/` directory.
2. Install requirements with `pip3 install -r requirements.txt`.
3. Start the server by running `python3 src/app.py`.

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
