# unmatched

# Local dev environment (Docker)

Make sure you have Docker or Docker Desktop (recommended) installed

Then build and run containers for local development with

```
docker compose build
docker compose up -d
```

To stop the containers use
`docker compose stop`

Dont use `down` command since it also removes containers, networks, volumes, and images created by docker-compose up. If you do run it by mistake, then just rebuild containers again with `docker compose build``
