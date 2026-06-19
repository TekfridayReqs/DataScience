# Credit Risk Modelling Assessment — browser edition

A self-contained assessment that runs entirely in the candidate's browser, so it
can be hosted free on **GitHub Pages**. Candidates write **Python or R**, run it
against a credit-risk dataset, and complete ten credit-modelling tasks. Python
runs via Pyodide and R via WebR — both are WebAssembly runtimes, so there is no
server to manage.

## Deploy from GitHub in three steps

1. Push this folder's contents to a GitHub repository (the repo root should
   contain `index.html`).
2. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push to `main`. The included workflow (`.github/workflows/deploy.yml`) builds
   and publishes the site. Your URL appears in the Actions run and under Settings → Pages,
   typically `https://<you>.github.io/<repo>/`.

That's it — anyone with the link can open it and work, and many candidates can use
it at the same time because each runs everything in their own browser.

## What candidates do

They open the page, enter a name and email (to label their submission), then move
through the ten tasks in the left rail. Each task has its own Python and R editor,
a Run button, and an output panel that shows printed results and Python plots.
Work is saved in the browser as they go. When finished they click **Download
answers** to get a JSON file of all their code, which they send to you.

The dataset is bundled at `data/credit_risk_dataset.csv` and is available to code
as `credit_risk_dataset.csv` (Python) or `/home/web_user/credit_risk_dataset.csv` (R).

## Honest trade-offs versus the server version

This browser edition is what GitHub can host, but running everything client-side
costs you some things the JupyterHub/Docker version has:

- **The login is not secure.** It only labels a submission; it does not
  authenticate anyone. For a controlled hiring process, gate access another way
  (share the link only with invited candidates, or put it behind an access layer).
- **No central submission capture.** There is no server to record answers, so
  candidates self-submit via the Download button. If you need automatic capture,
  you'd add an external endpoint (e.g. a form service or a small serverless
  function) — at which point it is no longer purely GitHub-hosted.
- **Library limits.** Pyodide includes pandas, numpy, scikit-learn, statsmodels,
  scipy, and matplotlib — enough for the full workflow — but the specialised
  credit packages (`optbinning`, `scorecardpy`) are not available, so candidates
  implement WoE/IV and scorecard scaling themselves. WebR ships base R plus a
  limited package set; R is best for analysis and text output here, and R plotting
  is not wired into the output panel in this version.
- **First load is slow.** The first Python run downloads the runtime and packages
  (tens of MB). It is cached afterwards.

If you need real authentication, automatic grading, central submission storage,
and the full Python/R credit libraries, the JupyterHub/Docker version is the right
choice — but it needs a Docker host (a small VM), not GitHub Pages.

## Swapping in the real Kaggle dataset

Replace `data/credit_risk_dataset.csv` with the real file. It must keep the same
column names so the tasks still apply: `person_age`, `person_income`,
`person_home_ownership`, `person_emp_length`, `loan_intent`, `loan_grade`,
`loan_amnt`, `loan_int_rate`, `loan_status` (target), `loan_percent_income`,
`cb_person_default_on_file`, `cb_person_cred_hist_length`. The shipped file is
synthetic data matching this schema so the app works out of the box.

## Notes

This is a working build that needs a quick test in a browser before you rely on
it — the Python path is solid; WebR is newer and more experimental. The runtime
versions are pinned in `index.html` (Pyodide) and loaded as `latest` (WebR); bump
them as you like.
