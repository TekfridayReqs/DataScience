# Credit Risk Modelling Assessment Platform

A multi-user assessment environment where candidates log in, work concurrently in
**Python or R**, and complete ten credit-modelling tasks against a credit-risk
dataset. It is built on JupyterHub, which provides login, isolated per-user
servers, concurrency, and both Python and R kernels out of the box. Each candidate
runs in their own resource-limited Docker container.

## What's in here

```
credit-assessment-platform/
├── docker-compose.yml          # runs the hub
├── jupyterhub/
│   ├── Dockerfile              # hub image (DockerSpawner + NativeAuthenticator)
│   └── jupyterhub_config.py    # login, signup, per-user containers, limits
└── singleuser/
    ├── Dockerfile              # candidate image: Python + R + credit libs + data
    ├── scripts/
    │   ├── generate_sample_data.py   # synthetic data matching the real schema
    │   └── load_kaggle_data.py       # swap in the real Kaggle data
    └── questions/
        ├── credit-model-assessment-questions.md   # the 10 tasks
        └── 00_start_here.ipynb                     # starter notebook
```

## Prerequisites

- Docker and the Docker Compose plugin on a Linux host (a small cloud VM is fine
  for a handful of concurrent candidates; scale the VM with expected concurrency).

## Setup

From the `credit-assessment-platform/` directory:

```bash
# 1. Build the candidate image (Python + R + libraries + dataset + questions).
#    This step also generates the synthetic dataset, so it works with no Kaggle account.
docker build -t credit-assess-singleuser ./singleuser

# 2. Build and start the hub.
docker compose up -d --build
```

Open `http://<host>:8000`. The first account you should create is **`admin`**
(sign up with that username); it administers the hub. Candidates then sign up
with their own username and password and start working immediately. Multiple
candidates can be logged in and running code at the same time — each gets an
isolated container.

> Login uses username + password via NativeAuthenticator, with self-service
> signup enabled. If you prefer email-based usernames, candidates can simply use
> their email address as the username. See "Hardening" below to change the auth
> model (e.g. admin-approved accounts or one-time codes).

## Using the real Kaggle dataset

The platform ships with a synthetic dataset that matches the real schema exactly,
so the questions are meaningful before you wire in Kaggle. To use the real data,
provide Kaggle API credentials and run the loader inside the candidate image.

The simplest approach is to bake it in at build time. Add this to the end of
`singleuser/Dockerfile`, supplying credentials as build arguments, then rebuild:

```dockerfile
ARG KAGGLE_USERNAME
ARG KAGGLE_KEY
RUN KAGGLE_USERNAME=$KAGGLE_USERNAME KAGGLE_KEY=$KAGGLE_KEY \
    python /home/jovyan/scripts/load_kaggle_data.py
```

```bash
docker build --build-arg KAGGLE_USERNAME=you --build-arg KAGGLE_KEY=xxxx \
  -t credit-assess-singleuser ./singleuser
```

Both the synthetic and real files land at `/home/jovyan/data/credit_risk_dataset.csv`,
so the notebooks and questions need no changes.

## How candidates experience it

On first launch, the ten questions and the starter notebook are copied into each
candidate's `work` folder. They open `00_start_here.ipynb`, load the data in
Python or R, and create notebooks to answer the tasks in
`credit-model-assessment-questions.md`. Work persists per user across sessions.

## Reviewing submissions

As the `admin` user you can access the hub's admin panel to see and manage users.
Each candidate's notebooks live in their per-user Docker volume
(`credit-assess-user-<username>`); copy them out for review, or open a candidate's
server from the admin panel. For structured auto-grading, consider layering in
**nbgrader**, which is purpose-built for releasing and grading notebook
assignments.

## Hardening before real use

- **Authentication**: self-service signup is convenient for testing but open. For
  real hiring, switch to admin-approved accounts (`NativeAuthenticator.open_signup
  = False`) or one-time access links so candidates can't create arbitrary accounts.
- **HTTPS**: put the hub behind a reverse proxy (Caddy, Nginx, Traefik) with TLS.
  Never run it on plain HTTP over the internet.
- **Untrusted code**: candidate code runs server-side. Containers are isolated and
  resource-limited here; for stricter isolation, disable outbound network from the
  candidate containers and remove the terminal. Keep any real database access
  read-only (a dedicated read-only login limited to specific views).
- **Data**: if you load a real dataset with candidate or customer information,
  collect only what you need and set a retention/cleanup policy.

## Notes and known rough edges

This is a runnable scaffold, not a tested production deployment. The
DockerSpawner-to-hub networking (`HUB_IP`, the shared `jupyterhub-net` network)
sometimes needs small adjustments depending on your Docker setup — if a candidate
container can't reach the hub, that is the first thing to check. The single-user
image is large (R + Python data stacks), so the first build takes a while.
