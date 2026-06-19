import os

c = get_config()  # noqa: F821

# --- Spawner: each candidate gets their own isolated container ---------------
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = True  # clean up the container when the candidate logs out

# Per-user persistent work folder. Questions are seeded here on first launch.
notebook_dir = "/home/jovyan/work"
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"credit-assess-user-{username}": notebook_dir}

# Resource limits so one candidate cannot starve the host.
c.DockerSpawner.mem_limit = "2G"
c.DockerSpawner.cpu_limit = 1.0

# --- How spawned containers reach the hub ------------------------------------
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_connect_ip = os.environ["HUB_IP"]  # resolvable name of the hub container

# --- Authentication: username + password, with self-service signup -----------
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
c.NativeAuthenticator.open_signup = True   # candidates can create their own login
c.NativeAuthenticator.minimum_password_length = 6
c.Authenticator.allow_all = True
c.Authenticator.admin_users = {"admin"}    # create this user first; it reviews/administers

# --- Persistence -------------------------------------------------------------
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"
