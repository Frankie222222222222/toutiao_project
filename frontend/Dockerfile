# syntax=docker/dockerfile:1.7

FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ARG VITE_API_BASE_URL
ARG VITE_AI_API_ENDPOINT
ARG VITE_AI_MODEL

ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_AI_API_ENDPOINT=$VITE_AI_API_ENDPOINT
ENV VITE_AI_MODEL=$VITE_AI_MODEL

RUN --mount=type=secret,id=VITE_AI_API_KEY \
    export VITE_AI_API_KEY="$(cat /run/secrets/VITE_AI_API_KEY 2>/dev/null || true)" && npm run build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
