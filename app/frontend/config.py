import os

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

ENDPOINTS = {
    "login": "/api/auth/login",
    "upload_jd": "/api/jd/upload-jd",
    "upload_resume": "/api/resume/upload-resume",
    "analyze": "/api/ats/analyze",
    "schedule": "/api/interview/schedule",
}

ALLOWED_TYPES = ["pdf", "docx", "png", "jpg", "jpeg"]

MIME_MAP = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
}

APP_NAME = "TalentFlow"
APP_TAGLINE = "AI Recruitment Platform"

# Color palette
COLORS = {
    "primary": "#6366f1",
    "primary_dark": "#4f46e5",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6",
}
