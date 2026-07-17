# Docker image CI/CD

This project deploys with Docker images published by GitHub Actions.

## Flow

1. Push to `main`.
2. `CI` runs frontend and backend checks.
3. `CD` builds and pushes images to GitHub Container Registry:
   - `ghcr.io/<lowercase-owner>/toutiao-api:<sha>`
   - `ghcr.io/<lowercase-owner>/toutiao-frontend:<sha>`
4. If SSH deploy is enabled, the server pulls those images and runs `docker-compose.prod.yml`.

## GitHub variables

Repository settings -> Secrets and variables -> Actions -> Variables:

- `ENABLE_SSH_DEPLOY`: set to `true` after the server is ready.
- `VITE_API_BASE_URL`: frontend API base URL, for example `http://your-server-ip:8000`.
- `VITE_AI_API_ENDPOINT`: optional AI API endpoint.
- `VITE_AI_MODEL`: optional AI model name.

## GitHub secrets

Repository settings -> Secrets and variables -> Actions -> Secrets:

- `SSH_HOST`: server IP or hostname.
- `SSH_USER`: SSH user, for example `root`.
- `SSH_PRIVATE_KEY`: private key used to connect to the server.
- `APP_DIR`: project path on the server, for example `/root/toutiao_project`.
- `VITE_AI_API_KEY`: optional AI API key used during frontend build.

## Server setup

Install Git, Docker, and Docker Compose on the server, then clone the repository:

```bash
git clone https://github.com/Frankie222222222222/toutiao_project.git
cd toutiao_project
cp backend/.env.example backend/.env
```

Edit `backend/.env` for production. The MySQL password in `backend/.env` should match `MYSQL_ROOT_PASSWORD` in the server shell or `.env` file used by Docker Compose.

Manual deploy command:

```bash
IMAGE_NAMESPACE=frankie222222222222 IMAGE_TAG=latest docker compose -f docker-compose.prod.yml up -d
```
