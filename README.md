# Welcome to the Unmatched Board Game Stats Project!

We're excited to make stats pretty and easy to use for the Unmatched board game. Our data is sourced from the amazing work carried out by [UM League](https://www.umleague.net/fighterstats).

In this project, you'll find beautifully presented and user-friendly stats to enhance your Unmatched board game experience. Dive in and enjoy the insights!

Happy gaming!

# Local dev environment (Docker), Setup and Usage Guide

## Prerequisites

- Ensure you have Docker or Docker Desktop (recommended) installed on your machine.

## Building and Running Containers for Local Development

1. **Build the containers:**
   ```sh
   docker compose build
   ```
1. **Start the containers:**
   ```sh
   docker compose up -d
   ```

## Stopping Containers

To stop the containers without removing them, use:

```sh
docker compose stop
```

**Important:** Avoid using the `docker compose down` command as it removes containers, networks, volumes, and images created by docker compose up. If you accidentally run down, you can rebuild the containers with:

```sh
docker compose build
```

## Database Population

The backend container automatically populates the database with data from the xls file located at `/backend/src/data/deck-fighter.xls`.

A hash is created for the xls file, and on each container start, the backend container entrypoint script checks if the file has changed by comparing hashes. If the file has not changed, the database is not re-populated, otherwise a fresh database population is carried out.

If you need to manually re-populate the database, you can run the script at any time:

```sh
docker compose build
```
