# GrillBot - Docs

Documentation site for GrillBot project.

## Requirements

- Docker with Compose v2. The image installs Python and the dependencies and
  renders the [D2](https://d2lang.com) diagrams in `data/`, so nothing else is
  needed locally.

## Run locally

```sh
docker compose up --build -d   # http://localhost:8080 (change with DOCS_PORT)
docker compose logs -f
docker compose down
```

For development with live reload (templates, static files and Python sources
are synced into the container):

```sh
docker compose -f compose.yaml -f compose.dev.yaml up --build --watch
```

Edited a diagram in `data/*.d2` or `requirements.txt`? Run the command again
with `--build`; those are baked into the image.

## Production server and configuration

The image runs [gunicorn](https://gunicorn.org) (`gunicorn.conf.py`): one worker
with four threads, dropped to an unprivileged user after binding port 80.
`GET /health` answers `200` without calling any upstream, and the image's
`HEALTHCHECK` uses it, so Docker Swarm only routes to and keeps healthy tasks.

Dependency lists on the service pages are downloaded from GitHub and cached in
the process:

| Variable | Default | Meaning |
|---|---|---|
| `CACHE_TTL_SECONDS` | `7200` | How long downloaded project files stay fresh. If a refresh fails, the previous data is served for up to 24 hours. |
| `HEALTH_TTL_SECONDS` | `30` | How long an online/offline check is reused. |

## License

GrillBot docs, like the whole of GrillBot, are released under the [MIT License](LICENSE).
Contributions are accepted under the same terms.
