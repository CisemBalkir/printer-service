from fastapi import FastAPI
from pydantic import BaseModel
from app.printer.simulator import PrinterSimulator
import json
import os

app = FastAPI()

printer = PrinterSimulator()

# ----------------------
# MODELS
# ----------------------

class ConnectRequest(BaseModel):
    mode: str


class PrintTextRequest(BaseModel):
    text: str


class PrintImageRequest(BaseModel):
    image: str


class PrintQRRequest(BaseModel):
    text: str


class ReprintRequest(BaseModel):
    job_id: str


# ----------------------
# BASE
# ----------------------

@app.get("/")
def root():
    return {"message": "Printer Service Running"}


# ----------------------
# CONNECT
# ----------------------

@app.post("/connect")
def connect_printer(req: ConnectRequest):

    try:
        return printer.connect(req.mode)

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ----------------------
# STATUS
# ----------------------

@app.get("/status")
def get_status():
    return printer.get_status()


# ----------------------
# PRINT TEXT
# ----------------------

@app.post("/print/text")
def print_text(req: PrintTextRequest):

    try:
        result = printer.print_text(req.text)

        return {
            "status": "success",
            "job": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# ----------------------
# PRINT IMAGE
# ----------------------

@app.post("/print/image")
def print_image(req: PrintImageRequest):

    try:
        result = printer.print_image(req.image)

        return {
            "status": "success",
            "job": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# ----------------------
# PRINT QR
# ----------------------

@app.post("/print/qr")
def print_qr(req: PrintQRRequest):

    try:
        result = printer.print_qr(req.text)

        return {
            "status": "success",
            "job": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# ----------------------
# REPRINT
# ----------------------

@app.post("/reprint")
def reprint(req: ReprintRequest):

    try:
        result = printer.reprint(req.job_id)

        return {
            "status": "success",
            "job": result
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# ----------------------
# HEALTH
# ----------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "connected": printer.state["connected"]
    }


# ----------------------
# LOGS (SAFE VERSION)
# ----------------------

@app.get("/logs")
def logs():

    log_path = "app/logs/logs.json"

    if not os.path.exists(log_path):
        return []

    try:
        with open(log_path, "r") as f:
            return json.load(f)

    except:
        return []