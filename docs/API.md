# API

## Auth
- `POST /register`
- `POST /login`
- `POST /logout`
- `POST /token`
- `GET /session-info`
- `GET /session-data`

## Planners
- `POST /generate-home`
- `POST /generate-party`
- `POST /generate-jewelry` (multipart; optional `outfit_image`)
- `GET /recommendations-details/{recommendation_id}`
- `GET /history`

## Health
- `GET /health`
- `GET /startup`
