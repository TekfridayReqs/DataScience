FROM quay.io/jupyterhub/jupyterhub:5

RUN python3 -m pip install --no-cache-dir \
        dockerspawner \
        jupyterhub-nativeauthenticator

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
WORKDIR /srv/jupyterhub
