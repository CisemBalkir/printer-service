import uuid
import random
import time
import base64
import qrcode
from io import BytesIO
from datetime import datetime
from app.services.logger_service import write_log


class PrinterSimulator:

    def __init__(self):

        self.state = {
            "connected": False,
            "mode": None,
            "paper": "ok",
            "cover": "closed",
            "temperature": "normal",
            "last_job": None,
            "queue_count": 0,
            "retry_count": 0
        }

        self.queue = []

    # ---------------- CONNECT ----------------
    def connect(self, mode: str):

        if mode not in ["usb", "lan"]:
            raise Exception("INVALID_MODE")

        self.state["connected"] = True
        self.state["mode"] = mode
        self.state["retry_count"] = 0

        write_log({
            "op": "connect",
            "mode": mode,
            "status": "success",
            "ts": datetime.utcnow().isoformat()
        })

        return {
            "status": "connected",
            "mode": mode
        }

    # ---------------- STATUS ----------------
    def get_status(self):
        self.state["queue_count"] = len(self.queue)
        return self.state

    # ---------------- PRINT TEXT ----------------
    def print_text(self, text: str):

        if not self.state["connected"]:
            raise Exception("COMM_ERROR")

        error = random.choice([None, None, "PAPER_OUT", "PAPER_JAM", "OVERHEAT"])
        job_id = str(uuid.uuid4())

        if error:
            job = {
                "job_id": job_id,
                "status": "error",
                "type": "text",
                "error": error,
                "ts": datetime.utcnow().isoformat()
            }

            self.queue.append(job)
            self.state["last_job"] = job

            write_log({
                "op": "print_text",
                "status": "error",
                "error": error,
                "job_id": job_id,
                "text": text
            })

            raise Exception(error)

        job = {
            "job_id": job_id,
            "status": "success",
            "type": "text",
            "text": text,
            "ts": datetime.utcnow().isoformat()
        }

        self.queue.append(job)
        self.state["last_job"] = job

        write_log({
            "op": "print_text",
            "status": "success",
            "job_id": job_id,
            "text": text
        })

        return job

    # ---------------- PRINT IMAGE ----------------
    def print_image(self, image_data: str):

        if not self.state["connected"]:
            raise Exception("COMM_ERROR")

        error = random.choice([None, "PAPER_OUT", "PAPER_JAM"])
        job_id = str(uuid.uuid4())

        if error:
            job = {
                "job_id": job_id,
                "status": "error",
                "type": "image",
                "error": error,
                "ts": datetime.utcnow().isoformat()
            }

            self.queue.append(job)
            self.state["last_job"] = job

            write_log({
                "op": "print_image",
                "status": "error",
                "job_id": job_id,
                "error": error
            })

            raise Exception(error)

        job = {
            "job_id": job_id,
            "status": "success",
            "type": "image",
            "ts": datetime.utcnow().isoformat()
        }

        self.queue.append(job)
        self.state["last_job"] = job

        write_log({
            "op": "print_image",
            "status": "success",
            "job_id": job_id
        })

        return job

    # ---------------- PRINT QR ----------------
    def print_qr(self, text: str):

        if not self.state["connected"]:
            raise Exception("COMM_ERROR")

        job_id = str(uuid.uuid4())

        qr = qrcode.make(text)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        job = {
            "job_id": job_id,
            "status": "success",
            "type": "qr",
            "qr": qr_base64,
            "ts": datetime.utcnow().isoformat()
        }

        self.queue.append(job)
        self.state["last_job"] = job

        write_log({
            "op": "print_qr",
            "status": "success",
            "job_id": job_id
        })

        return job

    # ---------------- REPRINT ----------------
    def reprint(self, job_id: str):

        job = next((j for j in self.queue if j["job_id"] == job_id), None)

        if not job:
            raise Exception("JOB_NOT_FOUND")

        if job["status"] == "success":
            return {
                "status": "already_success",
                "job": job
            }

        error = random.choice([None, "PAPER_OUT", "PAPER_JAM", None])

        if error:
            job["status"] = "error"
            job["error"] = error

            write_log({
                "op": "reprint",
                "status": "error",
                "job_id": job_id,
                "error": error
            })

            raise Exception(error)

        job["status"] = "success"
        job["error"] = None

        self.state["last_job"] = job

        write_log({
            "op": "reprint",
            "status": "success",
            "job_id": job_id
        })

        return job

    # ---------------- SIMPLE RECONNECT SIM ----------------
    def reconnect(self):

        self.state["retry_count"] += 1

        # exponential backoff sim
        time.sleep(min(2 ** self.state["retry_count"], 5))

        self.state["connected"] = True

        write_log({
            "op": "reconnect",
            "status": "success",
            "retry": self.state["retry_count"]
        })

        return {"status": "reconnected"}