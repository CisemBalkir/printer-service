# Printer Service (FastAPI + Mock Simulator)

## Project Overview

This project is a printer middleware simulation service built with FastAPI.  
It simulates USB and LAN connected thermal printers without requiring real hardware.

---

## Features

- USB / LAN connection support
- Print text
- Print image (mock)
- Print QR code
- Job queue system
- Reprint failed jobs
- Error simulation:
  - PAPER_OUT
  - PAPER_JAM
  - OVERHEAT
  - COMM_ERROR

---

##  How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run locally

```bash
uvicorn app.main:app --reload
```

### 3. Run with Docker

```bash
docker compose up --build
```

---

##  API Endpoints

### Connect Printer

POST `/connect`

```json
{
  "mode": "usb"
}
```

---

### Print Text

POST `/print/text`

```json
{
  "text": "Hello Printer"
}
```

---

### Print Image

POST `/print/image`

```json
{
  "image": "base64_string"
}
```

---

### Print QR

POST `/print/qr`

```json
{
  "text": "https://example.com"
}
```

---

### Status

GET `/status`

---

### Reprint

POST `/reprint`

```json
{
  "job_id": "uuid"
}
```

---

### Health Check

GET `/health`

---

##  Testing

Open Swagger UI:

http://localhost:8000/docs

Test all endpoints directly from browser.

---

## Architecture

- FastAPI → API layer
- Printer Simulator → core logic
- Logger → logs all operations
- Queue system → job tracking
