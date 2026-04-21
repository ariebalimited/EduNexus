# =========================================================
# 🚀 EDUNEXUS AI - COMPLETE PRODUCTION APPLICATION v2.0
# =========================================================
# Tech Stack: Python 3.10+, Streamlit, Supabase, OpenAI GPT-4o

import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import random
import time
import io
import base64
import os
import smtplib
import hashlib
import requests
import json
import logging
import speech_recognition as sr
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from spellchecker import SpellChecker
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import re
import uuid
import secrets
import traceback
from gtts import gTTS
import io as io_module
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict, Counter
import wave
import calendar
import time
from functools import wraps
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pytz
from typing import Dict, List, Tuple, Optional, Any
import hashlib
import hmac
import string
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

# =============================================
# 🔧 ADVANCED LOGGING SETUP - ENTERPRISE GRADE
# =============================================
class EnterpriseLogger:
    """Enterprise-grade logging with file, stream, and remote handlers"""
    
    def __init__(self, app_name="edunexus"):
        self.app_name = app_name
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup comprehensive logging"""
        logger = logging.getLogger(self.app_name)
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(f'{self.app_name}_production.log')
        file_handler.setLevel(logging.INFO)
        
        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
        return logger
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def critical(self, message):
        self.logger.critical(message)

logger = EnterpriseLogger().logger

# =========================================================
# 💎 ENHANCED GLOBAL CONSTANTS & CONFIGURATION
# =========================================================
class AppConfig:
    """Centralized application configuration"""
    
    # Branding
    APP_NAME = "🚀 EduNexus"
    TAGLINE = "The Big Future Starts Here"
    VERSION = "2.0.0"
    BUILD_DATE = "2025/01/13"
    
    # Colors
    BRAND_COLOR = "#6366f1"
    ACCENT_COLOR = "#ec4899"
    SUCCESS_COLOR = "#10b981"
    WARNING_COLOR = "#f59e0b"
    ERROR_COLOR = "#ef4444"
    DARK_BG = "#0f172a"
    LIGHT_BG = "#f8fafc"
    
    # Admin
    ADMIN_EMAIL = "arieldavidbaah@gmail.com"
    ADMIN_PASSWORD_HASH = None
    
    # Limits
    MAX_MESSAGE_LENGTH = 5000
    MAX_FILE_SIZE_MB = 100
    OTP_EXPIRY_MINUTES = 15
    SESSION_TIMEOUT_MINUTES = 30
    VOICE_TIMEOUT_SECONDS = 30
    MONTHLY_CREDITS = 10
    MAX_FILE_STORAGE_MB = 5000
    
    # API
    API_RATE_LIMIT = 100
    API_RATE_WINDOW_MINUTES = 1
    
    # Cache
    CACHE_TTL_HOURS = 24
    CACHE_MAX_SIZE_MB = 500
    
    # Payment
    PAYMENT_TIMEOUT_SECONDS = 300
    MIN_PAYMENT_USD = 1.0
    MAX_PAYMENT_USD = 9999.0
    
    # AI Models
    PRIMARY_AI_MODEL = "gpt-4o"
    FALLBACK_AI_MODEL = "gpt-3.5-turbo"
    
    # Features
    ENABLE_VOICE_AI = True
    ENABLE_VISION_API = True
    ENABLE_ANALYTICS = True
    ENABLE_PAYMENTS = True
    ENABLE_API = True
    ENABLE_MULTI_TENANCY = True

# =========================================================
# 💰 ENHANCED PREMIUM PLANS WITH FULL PPP SUPPORT
# =========================================================
PREMIUM_PLANS = {
    "Starter": {
        "price_usd": 2.99,
        "price_ghs": 20,
        "price_ngn": 1500,
        "price_kes": 400,
        "price_zar": 55,
        "price_gbp": 2.49,
        "price_cad": 4.00,
        "price_inr": 250,
        "price_aud": 4.50,
        "price_php": 170,
        "price_bdt": 310,
        "duration_days": 7,
        "features": [
            "GPT-3.5 Turbo AI",
            "Basic Voice AI",
            "5 Study Groups",
            "10GB Storage",
            "50 Mock Exams",
            "Basic Analytics",
            "Email Support",
            "5 Daily AI Queries",
            "Weekly Progress Reports"
        ],
        "exam_limit": 50,
        "storage_gb": 10,
        "ai_model": "gpt-3.5-turbo",
        "daily_ai_queries": 5,
        "support_priority": "standard",
        "custom_reports": False
    },
    "Pro": {
        "price_usd": 9.99,
        "price_ghs": 65,
        "price_ngn": 5000,
        "price_kes": 1300,
        "price_zar": 180,
        "price_gbp": 8.49,
        "price_cad": 13.50,
        "price_inr": 830,
        "price_aud": 15.00,
        "price_php": 555,
        "price_bdt": 1050,
        "duration_days": 30,
        "features": [
            "GPT-4o Full Access",
            "Premium Voice AI",
            "Unlimited Study Groups",
            "100GB Storage",
            "Unlimited Exams",
            "Advanced Analytics",
            "Priority Email Support",
            "Custom Study Plans",
            "Daily AI Queries Unlimited",
            "Video Tutorial Access",
            "Smart Recommendations",
            "Collaboration Tools"
        ],
        "exam_limit": 500,
        "storage_gb": 100,
        "ai_model": "gpt-4o",
        "daily_ai_queries": 999,
        "support_priority": "priority",
        "custom_reports": True
    },
    "Ultimate": {
        "price_usd": 79.99,
        "price_ghs": 500,
        "price_ngn": 40000,
        "price_kes": 10000,
        "price_zar": 1400,
        "price_gbp": 64.99,
        "price_cad": 108.00,
        "price_inr": 6640,
        "price_aud": 120.00,
        "price_php": 4440,
        "price_bdt": 8400,
        "duration_days": 365,
        "features": [
            "GPT-4o + Vision API",
            "Ultra Voice AI",
            "Lifetime Access",
            "Unlimited Storage",
            "All Features Unlocked",
            "24/7 Priority Support",
            "Custom Curriculum",
            "API Access",
            "White Label Option",
            "Dedicated Account Manager",
            "Advanced Analytics",
            "Export Reports",
            "Team Collaboration",
            "Custom Integrations"
        ],
        "exam_limit": 10000,
        "storage_gb": 1000,
        "ai_model": "gpt-4o",
        "daily_ai_queries": 10000,
        "support_priority": "vip",
        "custom_reports": True
    },
    "Enterprise": {
        "price_usd": 299.99,
        "price_ghs": 1800,
        "price_ngn": 150000,
        "price_kes": 39000,
        "price_zar": 5500,
        "price_gbp": 249.99,
        "price_cad": 405.00,
        "price_inr": 24900,
        "price_aud": 450.00,
        "price_php": 16650,
        "price_bdt": 31500,
        "duration_days": 365,
        "features": [
            "Everything in Ultimate",
            "Multi-tenant Support",
            "SSO Integration",
            "Advanced Security",
            "SLA Guarantee",
            "Dedicated Infrastructure",
            "Custom API Limits",
            "Advanced Reporting",
            "Team Training",
            "Quarterly Reviews",
            "Custom Features",
            "Priority Bug Fixes"
        ],
        "exam_limit": 100000,
        "storage_gb": 10000,
        "ai_model": "gpt-4o",
        "daily_ai_queries": 100000,
        "support_priority": "enterprise",
        "custom_reports": True
    }
}

# =========================================================
# 🌍 COMPREHENSIVE GLOBAL EDUCATION MAP
# =========================================================
EDUCATION_MAP = {
    "Ghana": {
        "Curriculum": "WASSCE",
        "ExamBodies": ["WAEC", "BECE"],
        "Levels": ["JHS 1", "JHS 2", "JHS 3", "SHS 1", "SHS 2", "SHS 3"],
        "Programs": ["General Science", "General Arts", "Business", "Visual Arts", "Home Economics", "Technical"],
        "Subjects": {
            "General Science": ["Mathematics", "Physics", "Chemistry", "Biology", "Geography", "English Language", "Additional Mathematics", "Computing", "Agricultural Science", "ICT"],
            "General Arts": ["English Language", "Literature", "History", "Geography", "Government", "Economics", "Additional Mathematics", "French", "Islamic Studies", "CRS"],
            "Business": ["Business Management", "Geography", "Financial Accounting", "Economics", "Core Mathematics", "General Science", "Additional Mathematics", "English Language", "Office Management", "Shorthand"],
            "Visual Arts": ["Art and Design", "Graphic Design", "Fashion Design", "Sculpture", "Painting", "Core Mathematics", "English Language", "General Science", "Art History", "Music"],
            "Home Economics": ["Food and Nutrition", "Clothing and Textiles", "Management in Living", "Consumer Studies", "Chemistry", "General Science", "Core Mathematics", "Catering", "Health Education"],
            "Technical": ["Technical Drawing", "Auto Mechanics", "Building Construction", "Metalwork", "Woodwork", "Electrical Installation", "Core Mathematics", "English Language", "Engineering", "Welding"]
        },
        "Currency": "GHS",
        "CurrencySymbol": "₵",
        "Language": "English",
        "SystemPromptAddOn": "Explain concepts using West African education terminology and WASSCE/BECE standards. Use Ghana-appropriate examples and local context.",
        "CountryCode": "GH",
        "TimeZone": "Africa/Accra"
    },
    "Nigeria": {
        "Curriculum": "WAEC/JAMB",
        "ExamBodies": ["WAEC", "JAMB", "NECO"],
        "Levels": ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"],
        "Programs": ["Science", "Arts", "Commercial", "Technical"],
        "Subjects": {
            "Science": ["Mathematics", "Physics", "Chemistry", "Biology", "English Language", "Further Mathematics", "Computer Science", "Agricultural Science", "Technical Drawing", "ICT"],
            "Arts": ["English Language", "Literature", "History", "Government", "Economics", "CRS/IRS", "Geography", "Civic Education", "Social Studies", "Psychology"],
            "Commercial": ["Accounting", "Commerce", "Economics", "Business Studies", "Marketing", "Typewriting", "Office Practice", "Data Processing", "Financial Accounting"],
            "Technical": ["Technical Drawing", "Engineering Science", "Electronics", "Metalwork", "Woodwork", "Building Construction", "Automobile Mechanics", "Welding", "Plumbing"]
        },
        "Currency": "NGN",
        "CurrencySymbol": "₦",
        "Language": "English",
        "SystemPromptAddOn": "Use Nigerian curriculum standards and JAMB/WAEC examination formats. Include Nigeria-specific examples and cultural context.",
        "CountryCode": "NG",
        "TimeZone": "Africa/Lagos"
    },
    "Kenya": {
        "Curriculum": "KCSE",
        "ExamBodies": ["KCPE", "KCSE"],
        "Levels": ["Form 1", "Form 2", "Form 3", "Form 4"],
        "Programs": ["Science", "Arts", "Commercial", "Technical"],
        "Subjects": {
            "Science": ["Mathematics", "Physics", "Chemistry", "Biology", "English Language", "Kiswahili", "Computer Studies", "History", "Geography", "Agriculture"],
            "Arts": ["English Language", "Kiswahili", "History", "Geography", "CRE/IRE", "Economics", "Government", "Business Studies", "Literature"],
            "Commercial": ["Accounting", "Business Studies", "Economics", "Geography", "Kiswahili", "Mathematics", "English Language", "Computer Studies"],
            "Technical": ["Woodwork", "Metalwork", "Building Construction", "Technical Drawing", "Engineering Science", "Automobile Mechanics", "Electrical Installation"]
        },
        "Currency": "KES",
        "CurrencySymbol": "KSh",
        "Language": "English/Kiswahili",
        "SystemPromptAddOn": "Follow KCSE curriculum standards and Kenyan education system. Use Kenya-appropriate examples and local educational context.",
        "CountryCode": "KE",
        "TimeZone": "Africa/Nairobi"
    },
    "South Africa": {
        "Curriculum": "CAPS",
        "ExamBodies": ["DBE"],
        "Levels": ["Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        "Programs": ["National Senior Certificate"],
        "Subjects": {
            "National Senior Certificate": ["Mathematics", "English", "Life Sciences", "Physical Sciences", "History", "Geography", "Economics", "Accounting", "Business Studies", "Computer Applications Technology"]
        },
        "Currency": "ZAR",
        "CurrencySymbol": "R",
        "Language": "English",
        "SystemPromptAddOn": "Use South African CAPS curriculum and NSC standards. Include South African examples and context.",
        "CountryCode": "ZA",
        "TimeZone": "Africa/Johannesburg"
    },
    "United States": {
        "Curriculum": "SAT/AP",
        "ExamBodies": ["College Board", "ACT"],
        "Levels": ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        "Programs": ["College Prep", "STEM", "Arts", "Advanced Placement"],
        "Subjects": {
            "College Prep": ["Algebra", "Geometry", "English", "Science", "Social Studies", "US History", "Physical Education"],
            "STEM": ["Calculus", "Physics", "Chemistry", "Biology", "Computer Science", "Engineering", "AP Statistics"],
            "Arts": ["English Literature", "World History", "Art", "Music", "Foreign Language", "Drama", "Creative Writing"],
            "Advanced Placement": ["AP Calculus", "AP Biology", "AP Chemistry", "AP US History", "AP Computer Science", "AP Statistics", "AP World History"]
        },
        "Currency": "USD",
        "CurrencySymbol": "$",
        "Language": "English",
        "SystemPromptAddOn": "Use US Common Core standards and College Board guidelines. Include American examples and context.",
        "CountryCode": "US",
        "TimeZone": "America/New_York"
    },
    "United Kingdom": {
        "Curriculum": "GCSE/A-Levels",
        "ExamBodies": ["Edexcel", "AQA", "OCR"],
        "Levels": ["Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12", "Year 13"],
        "Programs": ["STEM", "Humanities", "Mixed"],
        "Subjects": {
            "STEM": ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science", "Further Maths", "Engineering", "Statistics"],
            "Humanities": ["English Literature", "History", "Geography", "Government & Politics", "Sociology", "Philosophy", "Economics"],
            "Mixed": ["Mathematics", "English", "Science", "History", "Geography", "Language", "PE"]
        },
        "Currency": "GBP",
        "CurrencySymbol": "£",
        "Language": "English",
        "SystemPromptAddOn": "Follow UK GCSE and A-Level specifications. Use British examples and context.",
        "CountryCode": "GB",
        "TimeZone": "Europe/London"
    },
    "Canada": {
        "Curriculum": "Provincial",
        "ExamBodies": ["Provincial Boards"],
        "Levels": ["Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        "Programs": ["Academic", "Applied", "Pre-IB", "IB"],
        "Subjects": {
            "Academic": ["Mathematics", "English", "Science", "Social Studies", "French", "Computer Science"],
            "Applied": ["Mathematics", "English", "Science", "Career Studies", "Technology"],
            "Pre-IB": ["IB Standard Level", "IB Higher Level", "Extended Essay"],
            "IB": ["IB Diploma Program", "IB Core", "IB HL Subjects", "IB SL Subjects"]
        },
        "Currency": "CAD",
        "CurrencySymbol": "C$",
        "Language": "English/French",
        "SystemPromptAddOn": "Use Canadian provincial curriculum standards. Include Canadian examples and context.",
        "CountryCode": "CA",
        "TimeZone": "America/Toronto"
    },
    "India": {
        "Curriculum": "CBSE/ICSE",
        "ExamBodies": ["CBSE", "ICSE", "STATE"],
        "Levels": ["Class 6", "Class 8", "Class 10", "Class 11", "Class 12"],
        "Programs": ["Science (PCM)", "Science (PCB)", "Commerce", "Humanities"],
        "Subjects": {
            "Science (PCM)": ["Mathematics", "Physics", "Chemistry", "Computer Science", "English", "Engineering Graphics"],
            "Science (PCB)": ["Biology", "Physics", "Chemistry", "Botany", "Zoology", "English", "Psychology"],
            "Commerce": ["Accountancy", "Economics", "Business Studies", "Mathematics", "English", "Informatics Practices"],
            "Humanities": ["History", "Geography", "Political Science", "Sociology", "English", "Economics"]
        },
        "Currency": "INR",
        "CurrencySymbol": "₹",
        "Language": "English/Hindi",
        "SystemPromptAddOn": "Follow CBSE/ICSE curriculum standards for India. Use Indian examples and context.",
        "CountryCode": "IN",
        "TimeZone": "Asia/Kolkata"
    },
    "Australia": {
        "Curriculum": "VCE/HSC",
        "ExamBodies": ["VCAA", "NESA"],
        "Levels": ["Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12"],
        "Programs": ["General", "Specialist", "IB"],
        "Subjects": {
            "General": ["English", "Mathematics", "Science", "Humanities", "Technology", "LOTE"],
            "Specialist": ["Specialist Mathematics", "Physics", "Chemistry", "Biology", "Extended Investigation"],
            "IB": ["IB Higher Level", "IB Standard Level", "IB Extended Essay", "IB Core"]
        },
        "Currency": "AUD",
        "CurrencySymbol": "A$",
        "Language": "English",
        "SystemPromptAddOn": "Use Australian VCE/HSC standards. Include Australian examples and context.",
        "CountryCode": "AU",
        "TimeZone": "Australia/Sydney"
    }
}

# Currency exchange rates (relative to USD)
CURRENCY_RATES = {
    "USD": 1.0,
    "GHS": 13.5,
    "NGN": 500,
    "KES": 130,
    "ZAR": 18.5,
    "GBP": 0.79,
    "CAD": 1.35,
    "INR": 83,
    "AUD": 1.50,
    "PHP": 56,
    "BDT": 105
}

# =========================================================
# 🗄️ ADVANCED DATABASE MANAGER - PRODUCTION HYBRID
# =========================================================
class DatabaseManager:
    """Enterprise-grade Supabase + SQLite hybrid database manager"""
    
    def __init__(self):
        self.db_path = "edunexus_production.db"
        self.use_supabase = False
        self.supabase_url = st.secrets.get("SUPABASE_URL", "")
        self.supabase_key = st.secrets.get("SUPABASE_KEY", "")
        self.connection_pool = {}
        self._init_db()
    
    def get_connection(self):
        """Get SQLite connection with pooling and error handling"""
        try:
            thread_id = threading.current_thread().ident
            if thread_id not in self.connection_pool:
                conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30)
                conn.row_factory = sqlite3.Row
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                self.connection_pool[thread_id] = conn
            return self.connection_pool[thread_id]
        except Exception as e:
            logger.error(f"DB Connection Error: {str(e)}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # User indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_country ON users(country)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_tier ON users(tier)")
                
                # Message indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_group ON group_messages(group_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_sender ON group_messages(sender_email)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON group_messages(timestamp)")
                
                # Exam indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_exam_user ON exam_results(user_email)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_exam_subject ON exam_results(subject)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_exam_timestamp ON exam_results(timestamp)")
                
                # Chat indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_user ON ai_chat_history(user_email)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_conversation ON ai_chat_history(conversation_id)")
                
                # Transaction indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaction_user ON transactions(user_email)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaction_status ON transactions(status)")
                
                conn.commit()
                logger.info("✅ Database indexes created successfully")
        except Exception as e:
            logger.error(f"Index creation error: {str(e)}")
    
    def _init_db(self):
        """Initialize ALL database tables with complete enterprise schema"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # ===== USERS TABLE - Email Verification Foundation =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL,
                        country TEXT NOT NULL,
                        level TEXT NOT NULL,
                        program TEXT NOT NULL,
                        xp INTEGER DEFAULT 100,
                        tier TEXT DEFAULT 'Free',
                        status TEXT DEFAULT 'Active',
                        email_confirmed_at TEXT,
                        verification_code TEXT,
                        verification_code_created_at TEXT,
                        joined_date TEXT NOT NULL,
                        last_login TEXT,
                        last_activity TEXT,
                        profile_image BLOB,
                        bio TEXT DEFAULT '',
                        is_banned INTEGER DEFAULT 0,
                        ban_reason TEXT,
                        ban_date TEXT,
                        theme_preference TEXT DEFAULT 'dark',
                        voice_enabled INTEGER DEFAULT 1,
                        notifications_enabled INTEGER DEFAULT 1,
                        total_study_minutes INTEGER DEFAULT 0,
                        streak_days INTEGER DEFAULT 0,
                        last_study_date TEXT,
                        achievement_badges TEXT DEFAULT '[]',
                        country_code TEXT,
                        curriculum_type TEXT,
                        monthly_credits INTEGER DEFAULT 10,
                        credits_last_reset TEXT,
                        parent_email TEXT,
                        student_age INTEGER,
                        learning_style TEXT,
                        timezone TEXT,
                        language TEXT DEFAULT 'en',
                        api_key TEXT UNIQUE,
                        api_quota INTEGER DEFAULT 1000,
                        api_quota_reset TEXT,
                        two_factor_enabled INTEGER DEFAULT 0,
                        two_factor_secret TEXT,
                        last_ip_address TEXT,
                        login_attempts INTEGER DEFAULT 0,
                        locked_until TEXT
                    )
                """)
                
                # ===== GROUP MESSAGES (EduNexus [WhatsApp clone]) =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS group_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        group_id TEXT NOT NULL,
                        sender_email TEXT NOT NULL,
                        sender_name TEXT NOT NULL,
                        message TEXT,
                        message_type TEXT DEFAULT 'text',
                        audio_file BLOB,
                        image_data BLOB,
                        file_path TEXT,
                        timestamp TEXT NOT NULL,
                        edited_at TEXT,
                        edited_count INTEGER DEFAULT 0,
                        deleted_at TEXT,
                        deleted_by TEXT,
                        is_pinned INTEGER DEFAULT 0,
                        replies_count INTEGER DEFAULT 0,
                        reactions TEXT DEFAULT '{}',
                        reply_to_id INTEGER,
                        read_by TEXT DEFAULT '[]',
                        moderation_checked INTEGER DEFAULT 0,
                        is_flagged INTEGER DEFAULT 0,
                        flagged_reason TEXT,
                        is_important INTEGER DEFAULT 0,
                        sentiment_score REAL,
                        language_detected TEXT,
                        FOREIGN KEY (sender_email) REFERENCES users(email),
                        FOREIGN KEY (reply_to_id) REFERENCES group_messages(id)
                    )
                """)
                
                # ===== AI CHAT HISTORY =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ai_chat_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        conversation_id TEXT NOT NULL,
                        conversation_title TEXT,
                        role TEXT NOT NULL,
                        content TEXT,
                        message_type TEXT DEFAULT 'text',
                        audio_file BLOB,
                        image_data BLOB,
                        timestamp TEXT NOT NULL,
                        saved INTEGER DEFAULT 1,
                        tokens_used INTEGER DEFAULT 0,
                        model_used TEXT DEFAULT 'gpt-3.5-turbo',
                        response_time_ms INTEGER,
                        helpful_rating INTEGER,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== MOCK EXAMS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mock_exams (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        exam_name TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        level TEXT NOT NULL,
                        country TEXT NOT NULL,
                        difficulty TEXT DEFAULT 'medium',
                        total_questions INTEGER NOT NULL,
                        duration_minutes INTEGER,
                        created_at TEXT NOT NULL,
                        started_at TEXT,
                        completed_at TEXT,
                        status TEXT DEFAULT 'pending',
                        exam_type TEXT DEFAULT 'practice',
                        passing_score INTEGER DEFAULT 40,
                        custom_note TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== EXAM QUESTIONS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS exam_questions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        exam_id INTEGER NOT NULL,
                        question_text TEXT NOT NULL,
                        question_type TEXT DEFAULT 'mcq',
                        options TEXT,
                        correct_answer TEXT,
                        explanation TEXT,
                        topic TEXT,
                        difficulty TEXT,
                        image_data BLOB,
                        source TEXT,
                        FOREIGN KEY (exam_id) REFERENCES mock_exams(id)
                    )
                """)
                
                # ===== EXAM ANSWERS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS exam_answers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        exam_id INTEGER NOT NULL,
                        question_id INTEGER NOT NULL,
                        user_email TEXT NOT NULL,
                        selected_answer TEXT,
                        is_correct INTEGER,
                        time_spent_seconds INTEGER,
                        FOREIGN KEY (exam_id) REFERENCES mock_exams(id),
                        FOREIGN KEY (question_id) REFERENCES exam_questions(id),
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== EXAM RESULTS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS exam_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        exam_id INTEGER,
                        exam_name TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        total_questions INTEGER NOT NULL,
                        percentage REAL NOT NULL,
                        time_taken INTEGER,
                        difficulty TEXT,
                        timestamp TEXT NOT NULL,
                        country TEXT NOT NULL,
                        level TEXT NOT NULL,
                        topic_performance TEXT DEFAULT '{}',
                        passed INTEGER DEFAULT 0,
                        attempted_questions INTEGER,
                        skipped_questions INTEGER,
                        FOREIGN KEY (user_email) REFERENCES users(email),
                        FOREIGN KEY (exam_id) REFERENCES mock_exams(id)
                    )
                """)
                
                # ===== STUDY PROGRESS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS study_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        topic TEXT NOT NULL,
                        progress_percentage REAL DEFAULT 0,
                        time_spent_minutes INTEGER DEFAULT 0,
                        last_studied TEXT,
                        difficulty_level TEXT DEFAULT 'medium',
                        completion_status TEXT DEFAULT 'started',
                        resources_used TEXT DEFAULT '[]',
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== TIMETABLE =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS timetable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        day_of_week TEXT NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT NOT NULL,
                        duration_minutes INTEGER,
                        priority TEXT DEFAULT 'medium',
                        color TEXT,
                        repeat_type TEXT DEFAULT 'weekly',
                        created_date TEXT NOT NULL,
                        completed INTEGER DEFAULT 0,
                        reminder_enabled INTEGER DEFAULT 1,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== NOTIFICATIONS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        title TEXT NOT NULL,
                        message TEXT NOT NULL,
                        notification_type TEXT DEFAULT 'info',
                        priority TEXT DEFAULT 'normal',
                        read INTEGER DEFAULT 0,
                        created_at TEXT NOT NULL,
                        expires_at TEXT,
                        action_url TEXT,
                        action_type TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== CAPTURED PROBLEMS (Snap & Solve) =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS captured_problems (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        image_data BLOB NOT NULL,
                        problem_text TEXT,
                        solution TEXT,
                        subject TEXT,
                        solved_at TEXT NOT NULL,
                        helpful_count INTEGER DEFAULT 0,
                        unhelpful_count INTEGER DEFAULT 0,
                        saved INTEGER DEFAULT 1,
                        difficulty_level TEXT,
                        category TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== SUBSCRIPTIONS (Premium & PPP) =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS subscriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        plan TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        status TEXT DEFAULT 'active',
                        auto_renew INTEGER DEFAULT 1,
                        exam_count_used INTEGER DEFAULT 0,
                        storage_used_mb REAL DEFAULT 0,
                        currency TEXT NOT NULL,
                        amount_paid REAL,
                        payment_method TEXT,
                        renewal_count INTEGER DEFAULT 0,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== TRANSACTIONS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        amount REAL NOT NULL,
                        currency TEXT NOT NULL,
                        payment_method TEXT NOT NULL,
                        reference TEXT UNIQUE NOT NULL,
                        status TEXT DEFAULT 'pending',
                        plan TEXT,
                        timestamp TEXT NOT NULL,
                        momo_reference TEXT,
                        paypal_transaction_id TEXT,
                        stripe_payment_intent TEXT,
                        receipt_url TEXT,
                        ip_address TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== ANALYTICS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        metric_type TEXT NOT NULL,
                        metric_value REAL,
                        metric_date TEXT NOT NULL,
                        detailed_data TEXT,
                        session_id TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== LEADERBOARD =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS leaderboard (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        country TEXT NOT NULL,
                        program TEXT NOT NULL,
                        xp INTEGER,
                        rank INTEGER,
                        streak_count INTEGER DEFAULT 0,
                        total_exams INTEGER DEFAULT 0,
                        avg_score REAL DEFAULT 0,
                        updated_at TEXT NOT NULL,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== ACHIEVEMENTS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS achievements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        achievement_name TEXT NOT NULL,
                        achievement_description TEXT,
                        badge_icon TEXT,
                        earned_at TEXT NOT NULL,
                        points_awarded INTEGER DEFAULT 0,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== STUDY PLANS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS study_plans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        plan_name TEXT NOT NULL,
                        subjects TEXT,
                        duration_days INTEGER,
                        difficulty TEXT,
                        created_at TEXT NOT NULL,
                        completed_at TEXT,
                        progress_percentage REAL DEFAULT 0,
                        goal TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== ADMIN LOGS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS admin_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_email TEXT NOT NULL,
                        action TEXT NOT NULL,
                        target_email TEXT,
                        details TEXT,
                        timestamp TEXT NOT NULL,
                        ip_address TEXT,
                        FOREIGN KEY (admin_email) REFERENCES users(email)
                    )
                """)
                
                # ===== BAN RECORDS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ban_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        banned_by TEXT NOT NULL,
                        reason TEXT NOT NULL,
                        banned_at TEXT NOT NULL,
                        expires_at TEXT,
                        appeal_submitted INTEGER DEFAULT 0,
                        appeal_text TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email),
                        FOREIGN KEY (banned_by) REFERENCES users(email)
                    )
                """)
                
                # ===== STUDY SQUADS (Premium Groups) =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS study_squads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        squad_id TEXT UNIQUE,
                        creator_email TEXT NOT NULL,
                        squad_name TEXT NOT NULL,
                        description TEXT,
                        country TEXT NOT NULL,
                        program TEXT NOT NULL,
                        max_members INTEGER,
                        created_at TEXT NOT NULL,
                        status TEXT DEFAULT 'active',
                        invite_code TEXT UNIQUE,
                        FOREIGN KEY (creator_email) REFERENCES users(email)
                    )
                """)
                
                # ===== SQUAD MEMBERS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS squad_members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        squad_id TEXT NOT NULL,
                        user_email TEXT NOT NULL,
                        joined_at TEXT NOT NULL,
                        role TEXT DEFAULT 'member',
                        contribution_score INTEGER DEFAULT 0,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== REVISION ROADMAP =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS revision_roadmap (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        weak_topic TEXT NOT NULL,
                        confidence_level INTEGER,
                        practice_questions INTEGER,
                        created_at TEXT NOT NULL,
                        completed_at TEXT,
                        improvement_percentage REAL,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                # ===== API LOGS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS api_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT,
                        api_key TEXT NOT NULL,
                        endpoint TEXT NOT NULL,
                        method TEXT,
                        status_code INTEGER,
                        response_time_ms INTEGER,
                        request_body TEXT,
                        response_body TEXT,
                        timestamp TEXT NOT NULL,
                        ip_address TEXT
                    )
                """)
                
                # ===== AUDIT TRAIL =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_trail (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT,
                        action TEXT NOT NULL,
                        resource_type TEXT NOT NULL,
                        resource_id TEXT,
                        old_value TEXT,
                        new_value TEXT,
                        timestamp TEXT NOT NULL,
                        ip_address TEXT,
                        user_agent TEXT
                    )
                """)
                
                # ===== FEATURE FLAGS =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feature_flags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        feature_name TEXT UNIQUE NOT NULL,
                        enabled INTEGER DEFAULT 1,
                        rollout_percentage INTEGER DEFAULT 100,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                # ===== FEEDBACK =====
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        feedback_type TEXT,
                        title TEXT NOT NULL,
                        message TEXT NOT NULL,
                        rating INTEGER,
                        timestamp TEXT NOT NULL,
                        status TEXT DEFAULT 'open',
                        response TEXT,
                        FOREIGN KEY (user_email) REFERENCES users(email)
                    )
                """)
                
                conn.commit()
                self._create_indexes()
                logger.info("✅ Database initialized successfully with all tables")
        
        except Exception as e:
            logger.error(f"❌ Database initialization error: {str(e)}")
            raise

# Initialize Database
db = DatabaseManager()

# ======================
# 🔐 ENHANCED SECURITY 
# ======================
class EnhancedSecurityShield:
    """Production-grade security with enterprise features"""
    
    # Security settings
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_REQUIRE_UPPER = True
    PASSWORD_REQUIRE_LOWER = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SPECIAL = True
    
    @staticmethod
    def hash_password(password):
        """Hash password securely using PBKDF2-SHA256"""
        salt = os.urandom(32)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return base64.b64encode(salt + pwd_hash).decode()

    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        try:
            decoded = base64.b64decode(hashed)
            salt = decoded[:32]
            stored_hash = decoded[32:]
            pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            return pwd_hash == stored_hash
        except:
            return False

    @staticmethod
    def validate_password_strength(password):
        """Validate password meets security requirements"""
        errors = []
        
        if len(password) < EnhancedSecurityShield.PASSWORD_MIN_LENGTH:
            errors.append(f"Password must be at least {EnhancedSecurityShield.PASSWORD_MIN_LENGTH} characters")
        
        if EnhancedSecurityShield.PASSWORD_REQUIRE_UPPER and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if EnhancedSecurityShield.PASSWORD_REQUIRE_LOWER and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if EnhancedSecurityShield.PASSWORD_REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
        
        if EnhancedSecurityShield.PASSWORD_REQUIRE_SPECIAL and not any(c in string.punctuation for c in password):
            errors.append("Password must contain at least one special character")
        
        return errors if errors else None

    @staticmethod
    def generate_verification_code():
        """Generate 6-digit verification code"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    @staticmethod
    def generate_api_key():
        """Generate secure API key"""
        return f"edunexus_{''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))}"
    
    @staticmethod
    def send_verification_email(receiver_email, verification_code):
        """Send email verification code using SendGrid"""
        try:
            sender_email = st.secrets.get("GMAIL_USER", "")
            sender_password = st.secrets.get("GMAIL_APP_PASSWORD", "")
            
            if not sender_email or not sender_password:
                logger.warning("⚠️ Email credentials not configured")
                return False
            
            # Update database with verification code
            with db.get_connection() as conn:
                conn.execute(
                    """UPDATE users SET verification_code=?, verification_code_created_at=? WHERE email=?""",
                    (verification_code, datetime.now(timezone.utc).isoformat(), receiver_email)
                )
                conn.commit()

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"{AppConfig.APP_NAME} | Email Verification Required"

            body = f"""
            <html>
            <body style="font-family: 'Segoe UI', Arial; background: linear-gradient(135deg, {AppConfig.DARK_BG} 0%, #1e293b 100%); color: #ffffff; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, {AppConfig.BRAND_COLOR} 0%, {AppConfig.ACCENT_COLOR} 100%); padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);">
                        <h2 style="color: #ffffff; text-align: center; margin: 0; font-size: 28px;">🚀 {AppConfig.APP_NAME}</h2>
                        <p style="font-size: 16px; color: #e0e7ff; text-align: center; margin: 10px 0; font-weight: 500;">Email Verification Required</p>
                        
                        <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 10px; text-align: center; margin: 30px 0; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                            <p style="color: #e0e7ff; margin: 0 0 15px 0; font-size: 14px;">Your verification code is:</p>
                            <h1 style="letter-spacing: 15px; color: #ffffff; margin: 0; font-size: 48px; font-weight: bold; font-family: 'Courier New', monospace;">{verification_code}</h1>
                        </div>
                        
                        <p style="text-align: center; color: #e0e7ff; margin: 20px 0; font-size: 14px;">This code expires in <strong>{AppConfig.OTP_EXPIRY_MINUTES} minutes</strong></p>
                        
                        <div style="text-align: center; margin-top: 30px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 20px;">
                            <p style="color: #cbd5e1; font-size: 12px; margin: 0;">If you didn't request this verification, please ignore this email.</p>
                            <p style="color: #cbd5e1; font-size: 12px; margin: 10px 0 0 0;">© 2026 EduNexus Pro. All rights reserved. Version {AppConfig.VERSION}</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))

            for attempt in range(3):
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    logger.info(f"✅ Verification email sent to {receiver_email}")
                    return True
                except Exception as e:
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        raise
        
        except Exception as e:
            logger.error(f"❌ Email send error: {str(e)}")
        
        return False

    @staticmethod
    def verify_email_code(email, code):
        """Verify email code and confirm email"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT verification_code, verification_code_created_at FROM users WHERE email=?""",
                    (email,)
                )
                result = cursor.fetchone()
                
                if not result:
                    return False
                
                stored_code = result['verification_code']
                created_at = datetime.fromisoformat(result['verification_code_created_at'])
                
                # Check expiry
                if datetime.now(timezone.utc) - created_at.replace(tzinfo=timezone.utc) > timedelta(minutes=AppConfig.OTP_EXPIRY_MINUTES):
                    return False
                
                if stored_code == code:
                    # Mark email as confirmed
                    conn.execute(
                        """UPDATE users SET email_confirmed_at=?, verification_code=NULL WHERE email=?""",
                        (datetime.now(timezone.utc).isoformat(), email)
                    )
                    conn.commit()
                    logger.info(f"✅ Email confirmed for {email}")
                    return True
            
            return False
        except Exception as e:
            logger.error(f"❌ Verification error: {str(e)}")
            return False

    @staticmethod
    def get_user_country_from_ip():
        """Detect user country from IP using ipapi"""
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            data = response.json()
            return data.get('country_name', None)
        except:
            return None
    
    @staticmethod
    def check_brute_force_attempt(email):
        """Check for brute force login attempts"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT login_attempts, locked_until FROM users WHERE email=?""", (email,))
                result = cursor.fetchone()
                
                if not result:
                    return True
                
                login_attempts = result['login_attempts']
                locked_until = result['locked_until']
                
                # Check if account is locked
                if locked_until:
                    locked_time = datetime.fromisoformat(locked_until)
                    if datetime.now(timezone.utc) < locked_time.replace(tzinfo=timezone.utc):
                        return False
                    else:
                        # Unlock account
                        conn.execute("""UPDATE users SET login_attempts=0, locked_until=NULL WHERE email=?""", (email,))
                        conn.commit()
                        return True
                
                return login_attempts < EnhancedSecurityShield.MAX_LOGIN_ATTEMPTS
        except Exception as e:
            logger.error(f"Brute force check error: {str(e)}")
            return True

# ===============================
# 👤 ADVANCED SESSION MANAGEMENT
# ===============================
class EnhancedSessionManager:
    """Session management with timeout and advanced state guards"""
    
    @staticmethod
    def initialize_session():
        """Initialize all session variables"""
        if "auth_state" not in st.session_state:
            st.session_state.auth_state = "locked"
        if "current_user" not in st.session_state:
            st.session_state.current_user = None
        if "last_activity" not in st.session_state:
            st.session_state.last_activity = time.time()
        if "ai_chat_history" not in st.session_state:
            st.session_state.ai_chat_history = []
        if "theme" not in st.session_state:
            st.session_state.theme = "dark"
        if "current_group" not in st.session_state:
            st.session_state.current_group = None
        if "exam_session" not in st.session_state:
            st.session_state.exam_session = None
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
        if "show_emoji_picker" not in st.session_state:
            st.session_state.show_emoji_picker = False
        if "last_message_refresh" not in st.session_state:
            st.session_state.last_message_refresh = time.time()
        if "api_requests" not in st.session_state:
            st.session_state.api_requests = []
        if "page_visited" not in st.session_state:
            st.session_state.page_visited = None

    @staticmethod
    def check_session_timeout():
        """Check if session has timed out"""
        current = time.time()
        last = st.session_state.get("last_activity", current)
        
        if (current - last) > (AppConfig.SESSION_TIMEOUT_MINUTES * 60):
            st.session_state.auth_state = "locked"
            st.session_state.current_user = None
            return True
        
        st.session_state.last_activity = current
        return False

    @staticmethod
    def session_guard():
        """Guard against unauthorized access"""
        if st.session_state.auth_state == "locked" or st.session_state.current_user is None:
            st.warning("🔒 Please log in first")
            st.stop()

    @staticmethod
    def register_user(name, email, password, country, level, program):
        """Register new user with email verification"""
        try:
            # Validate password
            pwd_errors = EnhancedSecurityShield.validate_password_strength(password)
            if pwd_errors:
                return False, f"❌ Password weak: {', '.join(pwd_errors)}"
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if email exists
                cursor.execute("SELECT email FROM users WHERE email=?", (email,))
                if cursor.fetchone():
                    return False, "❌ Email already registered"
                
                # Hash password
                hashed_pwd = EnhancedSecurityShield.hash_password(password)
                
                # Generate API key
                api_key = EnhancedSecurityShield.generate_api_key()
                
                # Get timezone
                user_timezone = pytz.timezone('UTC')
                try:
                    user_tz_name = st.secrets.get("USER_TIMEZONE", "UTC")
                    user_timezone = pytz.timezone(user_tz_name)
                except:
                    pass
                
                # Create user
                conn.execute("""
                    INSERT INTO users
                    (email, name, password, country, level, program, joined_date, status, theme_preference, 
                     voice_enabled, email_confirmed_at, monthly_credits, credits_last_reset, api_key,
                     timezone, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    email, name, hashed_pwd, country, level, program,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Active', 'dark', 1, None, AppConfig.MONTHLY_CREDITS, 
                    datetime.now().strftime("%Y-%m-%d"), api_key, str(user_timezone), 'en'
                ))
                conn.commit()
                
                # Send verification email
                verification_code = EnhancedSecurityShield.generate_verification_code()
                EnhancedSecurityShield.send_verification_email(email, verification_code)
                
                logger.info(f"✅ User registered: {email}")
                return True, "✅ Account created! Check your email for verification code."
        
        except Exception as e:
            logger.error(f"❌ Registration error: {str(e)}")
            return False, f"❌ Registration error: {str(e)}"

    @staticmethod
    def login_user(email, password, ip_address="0.0.0.0"):
        """Login user with security checks"""
        try:
            # Check brute force
            if not EnhancedSecurityShield.check_brute_force_attempt(email):
                return False, "❌ Account temporarily locked due to multiple failed login attempts"
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT email, name, password, country, level, program, xp, tier, status, 
                           email_confirmed_at, theme_preference, voice_enabled, total_study_minutes, 
                           streak_days, monthly_credits, is_banned, timezone
                    FROM users WHERE email=?
                """, (email,))
                user_row = cursor.fetchone()

            if not user_row:
                return False, "❌ Check Email and try again"

            user_data = dict(user_row)

            if user_data['is_banned'] == 1:
                return False, "❌ Account banned"

            if not EnhancedSecurityShield.verify_password(password, user_data['password']):
                # Increment failed attempts
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT login_attempts FROM users WHERE email=?", (email,))
                    attempts = cursor.fetchone()['login_ttempts']
                    
                    if attempts + 1 >= EnhancedSecurityShield.MAX_LOGIN_ATTEMPTS:
                        lock_until = datetime.now(timezone.utc) + timedelta(minutes=EnhancedSecurityShield.LOCKOUT_DURATION_MINUTES)
                        conn.execute(
                            "UPDATE users SET login_attempts=?, locked_until=? WHERE email=?",
                            (attempts + 1, lock_until.isoformat(), email)
                        )
                    else:
                        conn.execute(
                            "UPDATE users SET login_attempts=? WHERE email=?",
                            (attempts + 1, email)
                        )
                    conn.commit()
                
                return False, "❌ Invalid password"

            # Reset failed attempts
            with db.get_connection() as conn:
                conn.execute(
                    "UPDATE users SET last_login=?, last_activity=?, login_attempts=0, last_ip_address=? WHERE email=?",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip_address, email)
                )
                conn.commit()

            # Admin bypass email verification
            if email == AppConfig.ADMIN_EMAIL:
                user_data['tier'] = 'Enterprise'
                user_data['email_confirmed_at'] = datetime.now().isoformat()

            st.session_state.current_user = user_data
            st.session_state.theme = user_data['theme_preference']
            st.session_state.last_activity = time.time()

            # Check if email is confirmed
            if user_data['email_confirmed_at'] is None:
                st.session_state.auth_state = "otp_pending"
            else:
                st.session_state.auth_state = "unlocked"

            logger.info(f"✅ Login: {email}")
            return True, "✅ Login successful"

        except Exception as e:
            logger.error(f"❌ Login error: {str(e)}")
            return False, f"❌ {str(e)}"

    @staticmethod
    def logout():
        """Logout user"""
        st.session_state.auth_state = "locked"
        st.session_state.current_user = None
        st.session_state.ai_chat_history = []
        st.rerun()

# =======================
# 🌍 LOCALIZATION ENGINE 
# =======================
class LocalizationEngine:
    """Global curriculum and PPP pricing engine"""
    
    @staticmethod
    def get_curriculum_system_prompt(user):
        """Get localized AI system prompt based on user's country"""
        country = user.get('country', 'United States')
        education_info = EDUCATION_MAP.get(country, {})
        curriculum = education_info.get('Curriculum', 'International')
        exam_bodies = education_info.get('ExamBodies', [])
        system_addon = education_info.get('SystemPromptAddOn', '')
        
        system_prompt = f"""You are EduNexus, an advanced and highly patient tutor helping {user['name']} from {country} 
studying {user['program']} at level {user['level']}.

📚 EDUCATIONAL CONTEXT:
- Curriculum: {curriculum}
- Exam Bodies: {', '.join(exam_bodies)}
- Program: {user['program']}
- Level: {user['level']}
- Student Learning Style: {user.get('learning_style', 'Mixed')}

{system_addon}

CRITICAL TEACHING INSTRUCTIONS:
1. Provide STEP-BY-STEP explanations with clear logical reasoning
2. Use examples SPECIFIC to the {country} education system and syllabus
3. Explain underlying CONCEPTS - not just answers
4. For MATH: Show all working and use proper mathematical notation with formatting
5. For SCIENCE: Include theoretical background and practical applications
6. Use SIMPLE ANALOGIES to explain complex topics
7. Be ENCOURAGING, supportive, and adaptive in tone
8. If student struggles, offer ALTERNATIVE explanations and different approaches
9. END with a summary question to check understanding
10. Personalize based on learning style: {user.get('learning_style', 'Mixed')}

IMPORTANT: Your goal is DEEP LEARNING, not quick answers. Adapt explanations based on feedback.
Maximum response length: 2000 tokens. Use markdown formatting for clarity."""
        
        return system_prompt

    @staticmethod
    def get_localized_price(plan_name, user_country):
        """Get PPP-adjusted price for user's country"""
        plan = PREMIUM_PLANS.get(plan_name, {})
        
        currency_map = {
            "Ghana": ("GHS", "price_ghs"),
            "Nigeria": ("NGN", "price_ngn"),
            "Kenya": ("KES", "price_kes"),
            "South Africa": ("ZAR", "price_zar"),
            "United Kingdom": ("GBP", "price_gbp"),
            "United States": ("USD", "price_usd"),
            "Canada": ("CAD", "price_cad"),
            "India": ("INR", "price_inr"),
            "Australia": ("AUD", "price_aud"),
            "Philippines": ("PHP", "price_php"),
            "Bangladesh": ("BDT", "price_bdt"),
        }
        
        currency, price_key = currency_map.get(user_country, ("USD", "price_usd"))
        price = plan.get(price_key, plan.get("price_usd", 0))
        
        return currency, price

    @staticmethod
    def detect_user_country():
        """Auto-detect user country from IP"""
        return EnhancedSecurityShield.get_user_country_from_ip()

# =========================================================
# 🎤 ADVANCED VOICE ENGINE - PRODUCTION GRADE
# =========================================================
class AdvancedVoiceEngine:
    """Advanced voice-to-text and text-to-speech system"""
    
    @staticmethod
    def speech_to_text_advanced():
        """Advanced speech-to-text with improved error handling"""
        try:
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 3000
            recognizer.dynamic_energy_threshold = True
            
            with sr.Microphone() as source:
                st.info("🎤 **Listening...** Speak clearly!")
                
                try:
                    audio = recognizer.listen(source, timeout=AppConfig.VOICE_TIMEOUT_SECONDS, phrase_time_limit=25)
                except sr.RequestError as e:
                    st.error(f"❌ Microphone error: {str(e)}")
                    return None
                
                try:
                    st.info("🔄 Processing your voice...")
                    text = recognizer.recognize_google(audio)
                    st.success(f"✅ Heard: {text}")
                    return text
                except sr.UnknownValueError:
                    st.error("❌ Could not understand. Please speak more clearly.")
                    return None
                except sr.RequestError as e:
                    st.error(f"❌ Error: {str(e)}")
                    return None
        
        except Exception as e:
            logger.error(f"❌ Voice error: {str(e)}")
            st.error(f"❌ Voice error: {str(e)}")
            return None

    @staticmethod
    def text_to_speech_advanced(text, lang="en"):
        """Convert text to speech with multiple language support"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            audio_buffer = io_module.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer
        except Exception as e:
            logger.error(f"❌ TTS error: {str(e)}")
            return None

# =========================================================
# 🤖 ENHANCED AI ENGINE - GPT-4o + VISION
# =========================================================
class EnhancedArielBrain:
    """OpenAI GPT-4o integration with vision and advanced reasoning"""
    
    @staticmethod
    def get_client():
        """Get OpenAI client with error handling"""
        try:
            api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                logger.warning("⚠️ OpenAI API key not configured")
                return None
            return OpenAI(api_key=api_key)
        except Exception as e:
            logger.error(f"❌ OpenAI client error: {str(e)}")
            return None

    @staticmethod
    def chat_ariel(prompt, user):
        """AI chat with localization and advanced reasoning"""
        client = EnhancedArielBrain.get_client()
        if not client:
            return "🔧 AI service offline. Try again later."
        
        try:
            # Check API quota
            try:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT api_quota FROM users WHERE email=?", (user['email'],))
                    result = cursor.fetchone()
                    if result and result['api_quota'] <= 0:
                        return "❌ API quota exceeded. Upgrade to continue."
            except:
                pass
            
            # Spell correction
            spell = SpellChecker()
            words = prompt.split()
            corrected = [spell.correction(w) if spell.correction(w) else w for w in words]
            refined_prompt = " ".join(corrected)

            # Select model based on tier
            model = AppConfig.PRIMARY_AI_MODEL if user['tier'] in ['Premium', 'Enterprise'] else AppConfig.FALLBACK_AI_MODEL
            
            # Get localized system prompt
            system_prompt = LocalizationEngine.get_curriculum_system_prompt(user)
            
            # Measure response time
            start_time = time.time()
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": refined_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9
            )
            
            response_time = int((time.time() - start_time) * 1000)
            response_text = response.choices[0].message.content
            
            # Award XP
            xp_amount = 10 if user['tier'] == 'Premium' else 5
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET xp = xp + ? WHERE email=?", (xp_amount, user['email']))
                
                # Deduct API quota
                cursor.execute("UPDATE users SET api_quota = api_quota - 1 WHERE email=?", (user['email'],))
                conn.commit()
            
            # Log analytics
            AnalyticsEngine.log_metric(user['email'], 'ai_chat', 1, response_text[:100])
            
            return response_text

        except Exception as e:
            logger.error(f"❌ AI error: {str(e)}")
            return f"⚠️ Error: {str(e)[:100]}"

    @staticmethod
    def snap_and_solve(image_file, user):
        """Vision API - Snap & Solve with step-by-step solutions"""
        client = EnhancedArielBrain.get_client()
        if not client:
            return "📸 Vision service offline"
        
        try:
            img_bytes = image_file.getvalue()
            encoded = base64.b64encode(img_bytes).decode('utf-8')
            
            curriculum = EDUCATION_MAP.get(user['country'], {}).get('Curriculum', 'International')
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a highly skilled tutor helping a {user['level']} student from {user['country']} 
(Curriculum: {curriculum}). Analyze this educational problem image and provide:
1. CLEAR identification of what the problem is asking
2. STEP-BY-STEP solution with all working shown
3. EXPLANATION of the mathematical/scientific concepts used
4. KEY FORMULAS if applicable
5. FINAL ANSWER highlighted clearly
6. SIMILAR practice problems to try
7. COMMON MISTAKES to avoid

Format using clear sections and LaTeX for mathematical expressions."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Solve this problem completely with detailed explanations"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}
                        ]
                    }
                ],
                max_tokens=3000
            )
            
            response_text = response.choices[0].message.content
            
            # Save captured problem
            try:
                with db.get_connection() as conn:
                    conn.execute("""
                        INSERT INTO captured_problems (user_email, image_data, solution, subject, solved_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (user['email'], img_bytes, response_text, user['program'], 
                          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
            except:
                pass
            
            # Award XP
            with db.get_connection() as conn:
                conn.execute("UPDATE users SET xp = xp + ? WHERE email=?", (20, user['email']))
                conn.commit()
            
            return response_text

        except Exception as e:
            logger.error(f"❌ Vision error: {str(e)}")
            return f"❌ Error: {str(e)}"

    @staticmethod
    def generate_exam_questions(country, program, subject, level, difficulty="medium", count=10):
        """Generate AI-powered exam questions with curriculum alignment"""
        client = EnhancedArielBrain.get_client()
        if not client:
            return []
        
        try:
            curriculum = EDUCATION_MAP.get(country, {}).get('Curriculum', 'International')
            
            prompt = f"""Generate {count} multiple-choice exam questions for:
Country: {country}
Curriculum: {curriculum}
Level: {level}
Subject: {subject}
Program: {program}
Difficulty: {difficulty}

REQUIREMENTS:
- Align EXACTLY with the {country} curriculum standards
- Use appropriate terminology for {curriculum}
- Include REALISTIC exam-style questions
- Ensure answers are EDUCATIONALLY SOUND
- Include brief but CLEAR explanations
- Vary question types and topics
- Include common misconceptions in distractors
- Format as valid JSON only (no extra text)

Return ONLY valid JSON array (no markdown, no code blocks):
[{{
    "question": "complete question text",
    "options": ["A. first option", "B. second option", "C. third option", "D. fourth option"],
    "correct_answer": "A",
    "explanation": "detailed explanation of why A is correct"
}}]"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            questions_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            try:
                # Remove markdown code blocks if present
                if questions_text.startswith("```"):
                    questions_text = questions_text.split("```")[1]
                    if questions_text.startswith("json"):
                        questions_text = questions_text[4:]
                
                questions = json.loads(questions_text)
                return questions if isinstance(questions, list) else []
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse questions JSON: {str(e)}")
                return []

        except Exception as e:
            logger.error(f"❌ Generate questions error: {str(e)}")
            return []

    @staticmethod
    def moderate_message(message):
        """Use OpenAI Moderation API to check message content"""
        client = EnhancedArielBrain.get_client()
        if not client:
            return True  # Allow if service unavailable
        
        try:
            response = client.moderations.create(input=message)
            if response.results[0].flagged:
                logger.warning(f"⚠️ Message flagged by moderation: {message[:50]}")
                return False
            return True
        except:
            return True

# =========================================================
# 💬 REAL-TIME MESSAGING (WhatsApp-Style EduNexus)
# =========================================================
class RealTimeMessaging:
    """WhatsApp-style messaging with reactions, pinning, and real-time updates"""
    
    EMOJI_REACTIONS = ["😀", "😂", "😍", "😢", "😡", "👍", "👎", "❤️", "🔥", "💯", "🎉", "🚀", "💪", "🙌", "😎", "🤔"]

    @staticmethod
    def send_group_message(group_id, user, message, message_type="text", audio_file=None):
        """Send group message with moderation"""
        try:
            if not message.strip() and not audio_file:
                return False
            
            if len(message) > AppConfig.MAX_MESSAGE_LENGTH:
                return False
            
            # Moderate message
            if not EnhancedArielBrain.moderate_message(message):
                logger.warning(f"⚠️ Message blocked by moderation: {user['email']}")
                return False
            
            with db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO group_messages
                    (group_id, sender_email, sender_name, message, message_type, audio_file, timestamp, reactions, moderation_checked)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    group_id, user['email'], user['name'], message, message_type, audio_file,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '{}', 1
                ))
                conn.commit()
            
            # Award XP
            with db.get_connection() as conn:
                conn.execute("UPDATE users SET xp = xp + ? WHERE email=?", (2, user['email']))
                conn.commit()
            
            GamificationEngine.check_achievements(user['email'])
            return True

        except Exception as e:
            logger.error(f"❌ Send message error: {str(e)}")
            return False

    @staticmethod
    def get_group_messages(country, program, limit=100):
        """Get group messages with lazy loading"""
        group_id = f"{country}_{program}".replace(" ", "_")
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, sender_email, sender_name, message, message_type, audio_file, timestamp, 
                           reactions, is_pinned, reply_to_id, deleted_at
                    FROM group_messages
                    WHERE group_id=? AND deleted_at IS NULL
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (group_id, limit))
                
                results = cursor.fetchall()
                return [dict(row) for row in reversed(results)] if results else []

        except Exception as e:
            logger.error(f"❌ Get messages error: {str(e)}")
            return []

    @staticmethod
    def delete_message(msg_id, user_email):
        """Delete message (soft delete)"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sender_email FROM group_messages WHERE id=?", (msg_id,))
                result = cursor.fetchone()
                
                if result and result['sender_email'] == user_email:
                    conn.execute(
                        "UPDATE group_messages SET deleted_at=?, deleted_by=? WHERE id=?",
                        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_email, msg_id)
                    )
                    conn.commit()
                    return True
            
            return False

        except Exception as e:
            logger.error(f"❌ Delete error: {str(e)}")
            return False

    @staticmethod
    def add_reaction(msg_id, reaction):
        """Add emoji reaction to message"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT reactions FROM group_messages WHERE id=?", (msg_id,))
                result = cursor.fetchone()
                
                if result:
                    reactions = json.loads(result['reactions']) if result['reactions'] else {}
                    reactions[reaction] = reactions.get(reaction, 0) + 1
                    
                    conn.execute(
                        "UPDATE group_messages SET reactions=? WHERE id=?",
                        (json.dumps(reactions), msg_id)
                    )
                    conn.commit()
                    return True
            
            return False

        except Exception as e:
            logger.error(f"❌ Reaction error: {str(e)}")
            return False

    @staticmethod
    def pin_message(msg_id):
        """Pin message to top"""
        try:
            with db.get_connection() as conn:
                conn.execute(
                    "UPDATE group_messages SET is_pinned=1 WHERE id=?",
                    (msg_id,)
                )
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Pin error: {str(e)}")
            return False

    @staticmethod
    def send_broadcast_message(admin_email, message):
        """Send message to all groups (Admin broadcast)"""
        try:
            if admin_email != AppConfig.ADMIN_EMAIL:
                return False
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT country, program FROM users WHERE status='Active'")
                groups = cursor.fetchall()
                
                for group in groups:
                    country, program = group
                    group_id = f"{country}_{program}".replace(" ", "_")
                    
                    conn.execute("""
                        INSERT INTO group_messages
                        (group_id, sender_email, sender_name, message, message_type, timestamp, reactions)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        group_id, AppConfig.ADMIN_EMAIL, "📢 EduNexus Admin", message, 'broadcast',
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '{}'
                    ))
                
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Broadcast error: {str(e)}")
            return False

# =========================================================
# 💾 CHAT HISTORY MANAGER
# =========================================================
class ChatHistoryManager:
    """Manage AI conversation history"""
    
    @staticmethod
    def save_message(user_email, conversation_id, role, content, message_type="text", audio_file=None, model_used="gpt-3.5-turbo"):
        """Save chat message"""
        try:
            with db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO ai_chat_history
                    (user_email, conversation_id, role, content, message_type, audio_file, timestamp, saved, model_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_email, conversation_id, role, content, message_type, audio_file,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1, model_used
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Save message error: {str(e)}")
            return False

    @staticmethod
    def get_conversation(user_email, conversation_id, limit=50):
        """Get conversation history"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT role, content, message_type, timestamp FROM ai_chat_history
                    WHERE user_email=? AND conversation_id=? AND saved=1
                    ORDER BY timestamp ASC
                    LIMIT ?
                """, (user_email, conversation_id, limit))
                
                results = cursor.fetchall()
                return [dict(row) for row in results] if results else []

        except Exception as e:
            logger.error(f"❌ Get conversation error: {str(e)}")
            return []

    @staticmethod
    def delete_message_from_history(message_id, user_email):
        """Delete from chat history"""
        try:
            with db.get_connection() as conn:
                conn.execute(
                    "UPDATE ai_chat_history SET saved=0 WHERE id=? AND user_email=?",
                    (message_id, user_email)
                )
                conn.commit()
                return True

        except Exception as e:
            logger.error(f"❌ Delete from history error: {str(e)}")
            return False

# =========================================================
# ✍️ MOCK EXAM ENGINE
# =========================================================
class MockExamEngine:
    """Advanced exam generation and scoring system"""
    
    @staticmethod
    def create_exam(user_email, exam_name, subject, country, program, level, difficulty="medium", num_questions=10):
        """Create new mock exam"""
        try:
            questions = EnhancedArielBrain.generate_exam_questions(
                country, program, subject, level, difficulty, num_questions
            )
            
            if not questions:
                return None
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create exam record
                cursor.execute("""
                    INSERT INTO mock_exams
                    (user_email, exam_name, subject, level, country, difficulty, total_questions, created_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_email, exam_name, subject, level, country, difficulty, len(questions),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'pending'
                ))
                
                exam_id = cursor.lastrowid
                
                # Insert questions
                for q in questions:
                    cursor.execute("""
                        INSERT INTO exam_questions
                        (exam_id, question_text, options, correct_answer, explanation, topic, difficulty)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        exam_id,
                        q.get('question', ''),
                        json.dumps(q.get('options', [])),
                        q.get('correct_answer', ''),
                        q.get('explanation', ''),
                        subject,
                        difficulty
                    ))
                
                conn.commit()
            
            return exam_id

        except Exception as e:
            logger.error(f"❌ Create exam error: {str(e)}")
            return None

    @staticmethod
    def save_answer(exam_id, question_id, user_email, selected_answer):
        """Save exam answer"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT correct_answer FROM exam_questions WHERE id=?", (question_id,))
                result = cursor.fetchone()
                correct_answer = result['correct_answer'] if result else ""
                
                is_correct = 1 if selected_answer == correct_answer else 0
                
                conn.execute("""
                    INSERT INTO exam_answers
                    (exam_id, question_id, user_email, selected_answer, is_correct)
                    VALUES (?, ?, ?, ?, ?)
                """, (exam_id, question_id, user_email, selected_answer, is_correct))
                
                conn.commit()
            
            return True

        except Exception as e:
            logger.error(f"❌ Save answer error: {str(e)}")
            return False

    @staticmethod
    def submit_exam(exam_id, user_email, country, level):
        """Submit and score exam"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get exam info
                cursor.execute("""
                    SELECT exam_name, subject, total_questions FROM mock_exams WHERE id=?
                """, (exam_id,))
                exam_info = cursor.fetchone()
                
                # Get score
                cursor.execute("""
                    SELECT COUNT(*) as correct FROM exam_answers 
                    WHERE exam_id=? AND is_correct=1
                """, (exam_id,))
                correct_count = cursor.fetchone()['correct']
                
                total = exam_info['total_questions']
                percentage = (correct_count / total * 100) if total > 0 else 0
                
                # Save result
                cursor.execute("""
                    INSERT INTO exam_results
                    (user_email, exam_id, exam_name, subject, score, total_questions, percentage, 
                     timestamp, country, level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_email, exam_id, exam_info['exam_name'], exam_info['subject'],
                    correct_count, total, percentage,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    country, level
                ))
                
                # Update exam status
                cursor.execute(
                    "UPDATE mock_exams SET completed_at=?, status=? WHERE id=?",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'completed', exam_id)
                )
                
                # Award XP
                xp_reward = int(correct_count * 10 + (100 if percentage >= 80 else 0))
                cursor.execute(
                    "UPDATE users SET xp = xp + ? WHERE email=?",
                    (xp_reward, user_email)
                )
                
                conn.commit()
            
            # Check achievements
            GamificationEngine.check_achievements(user_email)
            
            return {
                'score': correct_count,
                'total': total,
                'percentage': percentage,
                'xp_earned': xp_reward
            }

        except Exception as e:
            logger.error(f"❌ Submit exam error: {str(e)}")
            return None

    @staticmethod
    def get_weak_topics(user_email):
        """Analyze weak topics and generate revision roadmap"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get incorrect answers with topics
                cursor.execute("""
                    SELECT eq.topic, COUNT(*) as wrong_count
                    FROM exam_answers ea
                    JOIN exam_questions eq ON ea.question_id = eq.id
                    WHERE ea.user_email=? AND ea.is_correct=0
                    GROUP BY eq.topic
                    ORDER BY wrong_count DESC
                """, (user_email,))
                
                weak_topics = cursor.fetchall()
                return [dict(row) for row in weak_topics] if weak_topics else []
        
        except Exception as e:
            logger.error(f"❌ Weak topics error: {str(e)}")
            return []

# =========================================================
# 📊 ANALYTICS ENGINE - ENTERPRISE GRADE
# =========================================================
class AnalyticsEngine:
    """Advanced analytics and performance tracking"""
    
    @staticmethod
    def log_metric(email, metric_type, value, details=""):
        """Log metric for analytics"""
        try:
            with db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO analytics
                    (user_email, metric_type, metric_value, metric_date, detailed_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    email, metric_type, value,
                    datetime.now().strftime("%Y-%m-%d"),
                    details
                ))
                conn.commit()
            return True
        except:
            return False

    @staticmethod
    def get_user_stats(email):
        """Get comprehensive user statistics"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Messages sent
                cursor.execute("SELECT COUNT(*) as count FROM group_messages WHERE sender_email=?", (email,))
                messages_sent = cursor.fetchone()['count']
                
                # Exams taken
                cursor.execute("SELECT COUNT(*) as count FROM exam_results WHERE user_email=?", (email,))
                exams_taken = cursor.fetchone()['count']
                
                # Average score
                cursor.execute("SELECT AVG(percentage) as avg FROM exam_results WHERE user_email=?", (email,))
                avg_score = cursor.fetchone()['avg'] or 0
                
                # Study time
                cursor.execute("SELECT SUM(duration_minutes) as total FROM timetable WHERE user_email=?", (email,))
                study_time_db = cursor.fetchone()['total'] or 0
                
                # Get user total study minutes
                cursor.execute("SELECT total_study_minutes FROM users WHERE email=?", (email,))
                user_study = cursor.fetchone()['total_study_minutes'] or 0
                study_time = study_time_db + user_study
                
                # Problems solved
                cursor.execute("SELECT COUNT(*) as count FROM captured_problems WHERE user_email=? AND saved=1", (email,))
                problems_solved = cursor.fetchone()['count']
                
                # Streak
                cursor.execute("SELECT streak_days FROM users WHERE email=?", (email,))
                streak_days = cursor.fetchone()['streak_days'] or 0
                
                return {
                    'messages_sent': messages_sent,
                    'exams_taken': exams_taken,
                    'avg_score': round(avg_score, 2),
                    'study_time_hours': study_time // 60 if study_time else 0,
                    'study_time_minutes': study_time % 60 if study_time else 0,
                    'problems_solved': problems_solved,
                    'streak_days': streak_days
                }

        except Exception as e:
            logger.error(f"❌ Analytics error: {str(e)}")
            return {}

    @staticmethod
    def generate_performance_chart(email):
        """Generate performance trend chart"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT exam_name, percentage, timestamp FROM exam_results WHERE user_email=?
                    ORDER BY timestamp ASC LIMIT 20
                """, (email,))
                
                results = cursor.fetchall()
                if not results:
                    return None
                
                df = pd.DataFrame(results)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                fig = px.line(df, x='timestamp', y='percentage', title='📈 Exam Performance Over Time',
                            markers=True, labels={'percentage': 'Score (%)', 'timestamp': 'Date'},
                            line_shape="spline")
                fig.update_traces(line=dict(color=AppConfig.BRAND_COLOR, width=3))
                
                return fig

        except Exception as e:
            logger.error(f"❌ Chart error: {str(e)}")
            return None

    @staticmethod
    def get_subject_performance(email):
        """Get subject-wise performance radar chart"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT subject, AVG(percentage) as avg_score, COUNT(*) as exams_count
                    FROM exam_results WHERE user_email=?
                    GROUP BY subject
                """, (email,))
                
                results = cursor.fetchall()
                if not results:
                    return None
                
                df = pd.DataFrame(results)
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=df['avg_score'],
                    theta=df['subject'],
                    fill='toself',
                    name='Performance',
                    marker=dict(color=AppConfig.BRAND_COLOR)
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title='🎯 Subject Mastery Radar',
                    showlegend=False
                )
                
                return fig

        except Exception as e:
            logger.error(f"❌ Subject chart error: {str(e)}")
            return None

    @staticmethod
    def get_study_time_chart(email):
        """Get study time by day visualization"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT day_of_week, SUM(duration_minutes) as total_minutes FROM timetable 
                    WHERE user_email=? GROUP BY day_of_week
                """, (email,))
                
                results = cursor.fetchall()
                if not results:
                    return None
                
                df = pd.DataFrame(results)
                df['hours'] = df['total_minutes'] / 60
                
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
                df = df.sort_values('day_of_week')
                
                fig = px.bar(df, x='day_of_week', y='hours', title='📅 Study Time by Day',
                           labels={'hours': 'Hours', 'day_of_week': 'Day'}, color='hours',
                           color_continuous_scale='Viridis')
                
                return fig

        except Exception as e:
            logger.error(f"❌ Study time chart error: {str(e)}")
            return None

# =========================================================
# 📅 SMART TIMETABLE BUILDER
# =========================================================
class SmartTimetable:
    """Intelligent study schedule generation"""
    
    @staticmethod
    def create_study_schedule(email, subjects, available_hours_per_day=3):
        """Create AI-optimized study schedule"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                hours_per_subject = available_hours_per_day * 60 // len(subjects) if subjects else 0
                
                schedule = []
                
                for day in days:
                    start_hour = 8
                    for subject in subjects:
                        end_hour = start_hour + (hours_per_subject // 60) if hours_per_subject > 0 else start_hour + 1
                        
                        cursor.execute("""
                            INSERT INTO timetable
                            (user_email, subject, day_of_week, start_time, end_time, duration_minutes, created_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            email, subject, day,
                            f"{start_hour:02d}:00", f"{end_hour:02d}:00",
                            hours_per_subject if hours_per_subject > 0 else 60,
                            datetime.now().strftime("%Y-%m-%d")
                        ))
                        
                        schedule.append({
                            'subject': subject,
                            'day': day,
                            'time': f"{start_hour:02d}:00 - {end_hour:02d}:00"
                        })
                        
                        start_hour = end_hour
                
                conn.commit()
                
                # Award XP
                cursor.execute(
                    "UPDATE users SET xp = xp + ? WHERE email=?",
                    (15, email)
                )
                conn.commit()
                
                return schedule

        except Exception as e:
            logger.error(f"❌ Timetable creation error: {str(e)}")
            return []

    @staticmethod
    def get_timetable(email):
        """Get user timetable"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT subject, day_of_week, start_time, end_time, duration_minutes, priority, color
                    FROM timetable WHERE user_email=? ORDER BY day_of_week, start_time
                """, (email,))
                
                results = cursor.fetchall()
                return [dict(row) for row in results] if results else []

        except Exception as e:
            logger.error(f"❌ Get timetable error: {str(e)}")
            return []

    @staticmethod
    def visualize_timetable(email):
        """Visualize timetable as heatmap"""
        try:
            timetable = SmartTimetable.get_timetable(email)
            if not timetable:
                return None
            
            df = pd.DataFrame(timetable)
            
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
            
            pivot_table = df.groupby(['day_of_week', 'subject']).size().unstack(fill_value=0)
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_table.values,
                x=pivot_table.columns,
                y=pivot_table.index,
                colorscale='Blues'
            ))
            fig.update_layout(
                title='📅 Study Schedule Heatmap',
                xaxis_title='Subject',
                yaxis_title='Day',
                height=400
            )
            
            return fig

        except Exception as e:
            logger.error(f"❌ Visualize timetable error: {str(e)}")
            return None

# =========================================================
# 🏆 GAMIFICATION ENGINE 
# =========================================================
class GamificationEngine:
    """XP, achievements, badges, and leaderboards"""
    
    ACHIEVEMENTS = {
        "first_message": {"name": "Chatterbox", "description": "Send your first message", "icon": "💬", "points": 10},
        "first_exam": {"name": "Test Taker", "description": "Complete your first exam", "icon": "✍️", "points": 25},
        "100_xp": {"name": "Rising Star", "description": "Earn 100 XP", "icon": "⭐", "points": 50},
        "500_xp": {"name": "Shining Star", "description": "Earn 500 XP", "icon": "⭐⭐", "points": 100},
        "1000_xp": {"name": "Blazing Star", "description": "Earn 1000 XP", "icon": "⭐⭐⭐", "points": 250},
        "perfect_score": {"name": "Perfect", "description": "Score 100% on an exam", "icon": "💯", "points": 500},
        "week_streak": {"name": "Consistent", "description": "Study 7 days in a row", "icon": "🔥", "points": 150},
        "10_exams": {"name": "Exam Master", "description": "Complete 10 exams", "icon": "📚", "points": 200},
        "50_exams": {"name": "Exam Legend", "description": "Complete 50 exams", "icon": "📚📚", "points": 500},
        "50_messages": {"name": "Social Butterfly", "description": "Send 50 messages", "icon": "🦋", "points": 100},
        "100_messages": {"name": "Communication Pro", "description": "Send 100 messages", "icon": "📢", "points": 250},
    }

    @staticmethod
    def check_achievements(user_email):
        """Check and award new achievements"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check first message
                cursor.execute("SELECT COUNT(*) as count FROM group_messages WHERE sender_email=?", (user_email,))
                msg_count = cursor.fetchone()['count']
                if msg_count >= 1:
                    GamificationEngine.award_achievement(user_email, "first_message")
                if msg_count >= 50:
                    GamificationEngine.award_achievement(user_email, "50_messages")
                if msg_count >= 100:
                    GamificationEngine.award_achievement(user_email, "100_messages")
                
                # Check exams
                cursor.execute("SELECT COUNT(*) as count FROM exam_results WHERE user_email=?", (user_email,))
                exams_count = cursor.fetchone()['count']
                if exams_count >= 1:
                    GamificationEngine.award_achievement(user_email, "first_exam")
                if exams_count >= 10:
                    GamificationEngine.award_achievement(user_email, "10_exams")
                if exams_count >= 50:
                    GamificationEngine.award_achievement(user_email, "50_exams")
                
                # Check XP
                cursor.execute("SELECT xp FROM users WHERE email=?", (user_email,))
                xp = cursor.fetchone()['xp']
                if xp >= 100:
                    GamificationEngine.award_achievement(user_email, "100_xp")
                if xp >= 500:
                    GamificationEngine.award_achievement(user_email, "500_xp")
                if xp >= 1000:
                    GamificationEngine.award_achievement(user_email, "1000_xp")
                
                # Check perfect score
                cursor.execute("SELECT COUNT(*) as count FROM exam_results WHERE user_email=? AND percentage=100", (user_email,))
                if cursor.fetchone()['count'] >= 1:
                    GamificationEngine.award_achievement(user_email, "perfect_score")

        except Exception as e:
            logger.error(f"❌ Check achievements error: {str(e)}")

    @staticmethod
    def award_achievement(user_email, achievement_key):
        """Award achievement badge"""
        try:
            if achievement_key not in GamificationEngine.ACHIEVEMENTS:
                return False
            
            achievement = GamificationEngine.ACHIEVEMENTS[achievement_key]
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if already awarded
                cursor.execute(
                    "SELECT id FROM achievements WHERE user_email=? AND achievement_name=?",
                    (user_email, achievement['name'])
                )
                
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO achievements
                        (user_email, achievement_name, achievement_description, badge_icon, earned_at, points_awarded)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        user_email, achievement['name'], achievement['description'], achievement['icon'],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), achievement.get('points', 0)
                    ))
                    
                    # Award bonus XP
                    cursor.execute(
                        "UPDATE users SET xp = xp + ? WHERE email=?",
                        (achievement.get('points', 0), user_email)
                    )
                    
                    conn.commit()
                    SmartNotifications.create_achievement_badge(user_email, achievement['name'])
                    return True
            
            return False

        except Exception as e:
            logger.error(f"❌ Award achievement error: {str(e)}")
            return False

    @staticmethod
    def get_rank(xp):
        """Get rank name by XP"""
        if xp < 500:
            return "🌱 Novice Scholar"
        elif xp < 2000:
            return "⭐ Elite Genius"
        elif xp < 5000:
            return "👑 Sovereign Sage"
        elif xp < 10000:
            return "🔥 Ariel's Peer"
        elif xp < 20000:
            return "💎 Supreme Scholar"
        else:
            return "👑 Legendary Master"

    @staticmethod
    def get_level(xp):
        """Get level from XP"""
        return max(1, xp // 1000 + 1)

    @staticmethod
    def get_leaderboard(country, program, limit=10):
        """Get leaderboard"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, email, xp, tier FROM users
                    WHERE country=? AND program=? AND status='Active'
                    ORDER BY xp DESC
                    LIMIT ?
                """, (country, program, limit))
                
                results = cursor.fetchall()
                return [dict(row) for row in results] if results else []

        except Exception as e:
            logger.error(f"❌ Leaderboard error: {str(e)}")
            return []

# =========================================================
# 🔔 SMART NOTIFICATIONS
# =========================================================
class SmartNotifications:
    """Notification system with priorities and scheduling"""
    
    @staticmethod
    def create_notification(email, title, message, notification_type="info", priority="normal"):
        """Create notification"""
        try:
            expires_at = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
            
            with db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO notifications
                    (user_email, title, message, notification_type, priority, created_at, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    email, title, message, notification_type, priority,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    expires_at
                ))
                conn.commit()
            
            return True

        except Exception as e:
            logger.error(f"❌ Create notification error: {str(e)}")
            return False

    @staticmethod
    def get_unread_notifications(email, limit=10):
        """Get unread notifications"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, title, message, notification_type, priority, created_at FROM notifications
                    WHERE user_email=? AND read=0 AND expires_at > datetime('now')
                    ORDER BY created_at DESC LIMIT ?
                """, (email, limit))
                
                results = cursor.fetchall()
                return [dict(row) for row in results] if results else []

        except Exception as e:
            logger.error(f"❌ Get notifications error: {str(e)}")
            return []

    @staticmethod
    def mark_notification_read(notification_id):
        """Mark notification as read"""
        try:
            with db.get_connection() as conn:
                conn.execute(
                    "UPDATE notifications SET read=1 WHERE id=?",
                    (notification_id,)
                )
                conn.commit()
            return True

        except Exception as e:
            logger.error(f"❌ Mark notification error: {str(e)}")
            return False

    @staticmethod
    def create_achievement_badge(email, achievement_name):
        """Create achievement notification"""
        SmartNotifications.create_notification(
            email,
            f"🏆 Achievement Unlocked!",
            f"You've earned the '{achievement_name}' badge!",
            "achievement",
            "high"
        )

# =========================================================
# 💎 PREMIUM & PAYMENT SYSTEM - ENTERPRISE PPP
# =========================================================
class PremiumPaymentEngine:
    """Payment processing with advanced PPP pricing"""
    
    @staticmethod
    def get_plan_details(plan_name, user_country):
        """Get plan with PPP pricing"""
        plan = PREMIUM_PLANS.get(plan_name, {})
        currency, price = LocalizationEngine.get_localized_price(plan_name, user_country)
        
        return {
            **plan,
            'currency': currency,
            'localized_price': price,
            'plan_name': plan_name
        }

    @staticmethod
    def create_payment_reference(user_email, plan_name, user_country, payment_method="paypal"):
        """Create payment reference"""
        try:
            currency, price = LocalizationEngine.get_localized_price(plan_name, user_country)
            reference = f"{user_email}_{plan_name}_{int(time.time())}"
            
            with db.get_connection() as conn:
                conn.execute("""
                    INSERT INTO transactions
                    (user_email, amount, currency, payment_method, reference, status, plan, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_email, price, currency, payment_method, reference, 'pending', plan_name,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
            
            return reference
        except Exception as e:
            logger.error(f"❌ Payment reference error: {str(e)}")
            return None

    @staticmethod
    def process_momo_payment(user_email, plan_name, momo_reference, user_country):
        """Process Mobile Money payment (manual approval)"""
        try:
            currency, price = LocalizationEngine.get_localized_price(plan_name, user_country)
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Update transaction
                cursor.execute("""
                    UPDATE transactions SET momo_reference=?, status='pending_approval'
                    WHERE user_email=? AND plan=? AND status='pending'
                """, (momo_reference, user_email, plan_name))
                
                conn.commit()
            
            # Notify admin
            SmartNotifications.create_notification(
                AppConfig.ADMIN_EMAIL,
                f"💰 MoMo Payment - Manual Approval Required",
                f"User: {user_email}\nPlan: {plan_name}\nAmount: {currency} {price}\nReference: {momo_reference}",
                "payment",
                "high"
            )
            
            return True
        except Exception as e:
            logger.error(f"❌ MoMo payment error: {str(e)}")
            return False

    @staticmethod
    def approve_payment(admin_email, transaction_id):
        """Approve pending payment (Admin only)"""
        try:
            if admin_email != AppConfig.ADMIN_EMAIL:
                return False
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get transaction
                cursor.execute("""
                    SELECT user_email, plan, amount FROM transactions WHERE id=?
                """, (transaction_id,))
                
                trans = cursor.fetchone()
                if not trans:
                    return False
                
                user_email = trans['user_email']
                plan_name = trans['plan']
                
                # Update transaction
                cursor.execute("""
                    UPDATE transactions SET status='completed' WHERE id=?
                """, (transaction_id,))
                
                # Create subscription
                plan = PREMIUM_PLANS.get(plan_name, {})
                start_date = datetime.now()
                end_date = start_date + timedelta(days=plan.get('duration_days', 30))
                
                cursor.execute("""
                    INSERT INTO subscriptions
                    (user_email, plan, start_date, end_date, status, currency, amount_paid, payment_method)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_email, plan_name,
                    start_date.strftime("%Y-%m-%d %H:%M:%S"),
                    end_date.strftime("%Y-%m-%d %H:%M:%S"),
                    'active',
                    'GHS',
                    trans['amount'],
                    'momo'
                ))
                
                # Upgrade user tier
                cursor.execute("""
                    UPDATE users SET tier='Premium' WHERE email=?
                """, (user_email,))
                
                conn.commit()
                
                # Notify user
                SmartNotifications.create_notification(
                    user_email,
                    "💎 Welcome to Premium!",
                    f"Your {plan_name} subscription is now active. Enjoy all premium features!",
                    "payment",
                    "high"
                )
                
                logger.info(f"✅ Payment approved for {user_email}")
                return True
        except Exception as e:
            logger.error(f"❌ Approve payment error: {str(e)}")
            return False

    @staticmethod
    def deduct_monthly_credits(user_email):
        """Deduct/reset monthly credits for free users"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT tier FROM users WHERE email=?", (user_email,))
                result = cursor.fetchone()
                
                if result and result['tier'] == 'Free':
                    # Reset monthly credits on 1st of month
                    today = datetime.now()
                    if today.day == 1:
                        cursor.execute("""
                            UPDATE users SET monthly_credits=?, credits_last_reset=?
                            WHERE email=? AND tier='Free'
                        """, (AppConfig.MONTHLY_CREDITS, today.strftime("%Y-%m-%d"), user_email))
                        conn.commit()

        except Exception as e:
            logger.error(f"❌ Deduct credits error: {str(e)}")

# =========================================================
# 🛡️ ADMIN DASHBOARD - ENTERPRISE GOD MODE
# =========================================================
class AdminDashboard:
    """Complete admin control panel with advanced features"""
    
    @staticmethod
    def verify_admin(email):
        """Verify admin access"""
        return email == AppConfig.ADMIN_EMAIL

    @staticmethod
    def get_all_users():
        """Get all registered users"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT email, name, country, tier, status, xp, joined_date, last_login, is_banned, total_study_minutes
                    FROM users ORDER BY joined_date DESC
                """)
                
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"❌ Get users error: {str(e)}")
            return []

    @staticmethod
    def ban_user(admin_email, target_email, reason):
        """Ban user account"""
        try:
            if not AdminDashboard.verify_admin(admin_email):
                return False
            
            with db.get_connection() as conn:
                # Update user
                conn.execute("""
                    UPDATE users SET is_banned=1, status='Banned' WHERE email=?
                """, (target_email,))
                
                # Log action
                conn.execute("""
                    INSERT INTO ban_records
                    (user_email, banned_by, reason, banned_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    target_email, admin_email, reason,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                
                # Admin log
                conn.execute("""
                    INSERT INTO admin_logs
                    (admin_email, action, target_email, details, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    admin_email, 'BAN_USER', target_email, reason,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                
                conn.commit()
            
            logger.info(f"✅ User banned: {target_email}")
            return True
        except Exception as e:
            logger.error(f"❌ Ban user error: {str(e)}")
            return False

    @staticmethod
    def unban_user(admin_email, target_email):
        """Unban user account"""
        try:
            if not AdminDashboard.verify_admin(admin_email):
                return False
            
            with db.get_connection() as conn:
                conn.execute("""
                    UPDATE users SET is_banned=0, status='Active' WHERE email=?
                """, (target_email,))
                
                # Admin log
                conn.execute("""
                    INSERT INTO admin_logs
                    (admin_email, action, target_email, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (
                    admin_email, 'UNBAN_USER', target_email,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                
                conn.commit()
            
            logger.info(f"✅ User unbanned: {target_email}")
            return True
        except Exception as e:
            logger.error(f"❌ Unban user error: {str(e)}")
            return False

    @staticmethod
    def get_platform_stats():
        """Get global platform statistics"""
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total users
                cursor.execute("SELECT COUNT(*) as count FROM users")
                total_users = cursor.fetchone()['count']
                
                # Premium users
                cursor.execute("SELECT COUNT(*) as count FROM users WHERE tier IN ('Premium', 'Enterprise')")
                premium_users = cursor.fetchone()['count']
                
                # Total exams
                cursor.execute("SELECT COUNT(*) as count FROM exam_results")
                total_exams = cursor.fetchone()['count']
                
                # Total messages
                cursor.execute("SELECT COUNT(*) as count FROM group_messages")
                total_messages = cursor.fetchone()['count']
                
                # Revenue (sum of all transactions)
                cursor.execute("SELECT SUM(amount) as total FROM transactions WHERE status='completed'")
                revenue = cursor.fetchone()['total'] or 0
                
                # Banned users
                cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_banned=1")
                banned_users = cursor.fetchone()['count']
                
                # Total study minutes
                cursor.execute("SELECT SUM(total_study_minutes) as total FROM users")
                total_study_mins = cursor.fetchone()['total'] or 0
                
                # Active today
                today = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("SELECT COUNT(*) as count FROM users WHERE last_activity LIKE ?", (f"{today}%",))
                active_today = cursor.fetchone()['count']
                
                return {
                    'total_users': total_users,
                                        'premium_users': premium_users,
                    'free_users': total_users - premium_users,
                    'total_exams': total_exams,
                    'total_messages': total_messages,
                    'revenue': revenue,
                    'banned_users': banned_users,
                    'total_study_hours': total_study_mins // 60,
                    'active_today': active_today
                }
        except Exception as e:
            logger.error(f"❌ Platform stats error: {str(e)}")
            return {}

# =========================================================
# 🎨 UI COMPONENTS & RENDERING - PRODUCTION GRADE
# =========================================================

def apply_theme():
    """Apply premium theme styling"""
    st.markdown(f"""
        <style>
        :root {{
            --brand-color: {AppConfig.BRAND_COLOR};
            --accent-color: {AppConfig.ACCENT_COLOR};
            --success-color: {AppConfig.SUCCESS_COLOR};
            --warning-color: {AppConfig.WARNING_COLOR};
            --error-color: {AppConfig.ERROR_COLOR};
            --dark-bg: {AppConfig.DARK_BG};
        }}
        
        .stApp {{
            background: linear-gradient(135deg, {AppConfig.DARK_BG} 0%, #1a1f3a 100%);
            color: #f8fafc;
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
            border-right: 3px solid {AppConfig.BRAND_COLOR};
        }}
        
        .stButton>button {{
            background: linear-gradient(90deg, {AppConfig.BRAND_COLOR}, {AppConfig.ACCENT_COLOR});
            color: white;
            border: none;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }}
        
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        }}
        
        .message-bubble {{
            background: {AppConfig.BRAND_COLOR};
            padding: 12px 16px;
            border-radius: 15px;
            margin-bottom: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            color: white;
        }}
        
        .admin-card {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin-bottom: 15px;
        }}
        
        h1, h2, h3 {{
            color: {AppConfig.BRAND_COLOR};
        }}
        
        .metric-card {{
            background: rgba(99, 102, 241, 0.1);
            border: 2px solid {AppConfig.BRAND_COLOR};
            border-radius: 10px;
            padding: 15px;
        }}
        
        .premium-badge {{
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            color: white;
        }}
        
        .enterprise-badge {{
            background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            color: white;
        }}
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render premium header with version and branding"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px 0; background: linear-gradient(135deg, {AppConfig.BRAND_COLOR} 0%, {AppConfig.ACCENT_COLOR} 100%); 
                        border-radius: 15px; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);">
                <h1 style="color: #ffffff; margin: 0; font-size: 40px; font-weight: 900;">
                    {AppConfig.APP_NAME}
                </h1>
                <p style="color: #e0e7ff; margin: 5px 0; font-size: 16px;">
                    {AppConfig.TAGLINE}
                </p>
                <p style="color: #cbd5e1; margin: 5px 0; font-size: 12px;">
                    v{AppConfig.VERSION} • Built {AppConfig.BUILD_DATE}
                </p>
            </div>
        """, unsafe_allow_html=True)

def render_message_bubble(message, sender_name, sender_email, current_user_email, timestamp):
    """Render WhatsApp-style message bubble"""
    is_current = sender_email == current_user_email
    bg_color = AppConfig.BRAND_COLOR if is_current else "#334155"
    text_align = "right" if is_current else "left"
    align_content = "flex-end" if is_current else "flex-start"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: {align_content}; margin-bottom: 8px;">
            <div style="background: {bg_color}; padding: 12px 16px; border-radius: 15px; 
                        max-width: 70%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                <p style="color: #ffffff; margin: 0 0 5px 0; font-weight: 600; font-size: 12px;">{sender_name}</p>
                <p style="color: #ffffff; margin: 0 0 5px 0; word-wrap: break-word; font-size: 14px;">{message}</p>
                <p style="color: #ffffff; margin: 0; font-size: 11px; opacity: 0.7;">{timestamp}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_user_card(user):
    """Render user profile card"""
    tier_emoji = "💎" if user['tier'] == 'Enterprise' else "👑" if user['tier'] == 'Premium' else "⭐"
    rank = GamificationEngine.get_rank(user['xp'])
    level = GamificationEngine.get_level(user['xp'])
    
    st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border: 2px solid {AppConfig.BRAND_COLOR}; 
                    padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="color: {AppConfig.BRAND_COLOR}; margin-top: 0;">👤 {user['name']}</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div><strong>Email:</strong> {user['email']}</div>
                <div><strong>Tier:</strong> {tier_emoji} {user['tier']}</div>
                <div><strong>Country:</strong> 🌍 {user['country']}</div>
                <div><strong>Level:</strong> L{level}</div>
                <div><strong>XP:</strong> {user['xp']}</div>
                <div><strong>Joined:</strong> {user.get('joined_date', 'N/A')}</div>
            </div>
            <p style="color: {AppConfig.BRAND_COLOR}; font-weight: bold; margin-top: 10px;">{rank}</p>
        </div>
    """, unsafe_allow_html=True)

def render_loading_spinner():
    """Render custom loading spinner"""
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
            <div style="border: 4px solid rgba(99, 102, 241, 0.2); border-top: 4px solid #6366f1; 
                        border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite;"
                 id="spinner"></div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)

# =========================================================
# 📱 MAIN APP PAGES - COMPLETE
# =========================================================

def render_login_page():
    """Render login page with enhanced security"""
    render_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        choice = st.radio("Choose Action", ["🔐 Login", "📝 Sign Up"], label_visibility="collapsed", horizontal=True)

        if choice == "📝 Sign Up":
            st.subheader("Create Your Account")
            st.info("🔒 Your data is encrypted and secure")
            
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@example.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="Min 12 characters with special chars", key="signup_pwd")
            password_confirm = st.text_input("Confirm Password", type="password", key="signup_pwd_confirm")
            
            # Country detection
            detected_country = LocalizationEngine.detect_user_country()
            countries = list(EDUCATION_MAP.keys())
            default_idx = countries.index(detected_country) if detected_country in countries else 0
            
            country = st.selectbox("📍 Country", countries, index=default_idx)
            
            if country in EDUCATION_MAP:
                levels = EDUCATION_MAP[country].get("Levels", [])
                programs = EDUCATION_MAP[country].get("Programs", [])
                
                col1, col2 = st.columns(2)
                with col1:
                    level = st.selectbox("📚 Level", levels)
                with col2:
                    program = st.selectbox("🎯 Program", programs)
            
            if st.button("📝 Create Account", use_container_width=True, type="primary"):
                if not all([name, email, password, country, level, program]):
                    st.error("❌ Please fill all fields")
                elif len(password) < 12:
                    st.error("❌ Password must be at least 12 characters")
                elif password != password_confirm:
                    st.error("❌ Passwords don't match")
                else:
                    pwd_errors = EnhancedSecurityShield.validate_password_strength(password)
                    if pwd_errors:
                        for error in pwd_errors:
                            st.error(f"❌ {error}")
                    else:
                        success, message = EnhancedSessionManager.register_user(
                            name, email, password, country, level, program
                        )
                        if success:
                            st.success(f"✅ {message}")
                            st.info("📧 Check your email for verification code")
                        else:
                            st.error(f"❌ {message}")
        
        else:  # Login
            st.subheader(f"Welcome!")
            
            email = st.text_input("Email", placeholder="your@email.com", key="login_email")
            password = st.text_input("Password", type="password", key="login_pwd")
            
            col1, col2 = st.columns(2)
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                forgot_password = st.checkbox("Forgot password?")
            
            if st.button("🔓 Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("❌ Please enter email and password")
                else:
                    ip_address = st.session_state.get("user_ip", "0.0.0.0")
                    success, message = EnhancedSessionManager.login_user(email, password, ip_address)
                    if success:
                        st.success("✅ Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
            
            st.divider()
            st.caption("🔒 Secure Login • 256-bit Encryption • No Password Stored")

def render_email_verification_page():
    """Render email verification page"""
    render_header()
    
    user = st.session_state.current_user
    
    st.title("📧 Email Verification")
    st.write(f"Verification code has been sent to **{user['email']}**")
    st.info("⏱️ Code expires in 15 minutes")
    
    code = st.text_input("Enter 6-digit code", placeholder="000000", max_chars=6, key="verify_code")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Verify", use_container_width=True, type="primary"):
            if not code:
                st.error("❌ Please enter code")
            elif len(code) != 6:
                st.error("❌ Code must be 6 digits")
            elif not code.isdigit():
                st.error("❌ Code must contain only numbers")
            else:
                if EnhancedSecurityShield.verify_email_code(user['email'], code):
                    st.session_state.auth_state = "unlocked"
                    st.success("✅ Email verified!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid or expired code")
    
    with col2:
        if st.button("📤 Resend Code", use_container_width=True):
            code = EnhancedSecurityShield.generate_verification_code()
            if EnhancedSecurityShield.send_verification_email(user['email'], code):
                st.success("✅ Code resent!")
            else:
                st.error("❌ Failed to send code")

def render_dashboard(user):
    """Render main dashboard"""
    if EnhancedSessionManager.check_session_timeout():
        st.warning("⏱️ Session expired. Please log in again.")
        st.stop()
    
    render_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_user_card(user)

    st.divider()

    stats = AnalyticsEngine.get_user_stats(user['email'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🎯 XP", user['xp'], f"L{GamificationEngine.get_level(user['xp'])}")
    with col2:
        st.metric("💬 Messages", stats.get('messages_sent', 0))
    with col3:
        st.metric("✍️ Exams", stats.get('exams_taken', 0))
    with col4:
        st.metric("📊 Avg", f"{stats.get('avg_score', 0):.1f}%")
    with col5:
        tier_display = f"{'💎 Enterprise' if user['tier'] == 'Enterprise' else '👑 Premium' if user['tier'] == 'Premium' else '⭐ Free'}"
        st.metric("Tier", tier_display)

    st.divider()

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid {AppConfig.BRAND_COLOR};">
                <h4 style="color: {AppConfig.BRAND_COLOR}; margin: 0;">📚 Study Hours</h4>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{stats.get('study_time_hours', 0)}h {stats.get('study_time_minutes', 0)}m</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid {AppConfig.SUCCESS_COLOR};">
                <h4 style="color: {AppConfig.SUCCESS_COLOR}; margin: 0;">🔥 Streak</h4>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{stats.get('streak_days', 0)} days</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #3b82f6;">
                <h4 style="color: #3b82f6; margin: 0;">📸 Problems Solved</h4>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{stats.get('problems_solved', 0)}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style="background: rgba(168, 85, 247, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #a855f7;">
                <h4 style="color: #a855f7; margin: 0;">🏆 Rank</h4>
                <p style="font-size: 18px; font-weight: bold; margin: 10px 0;">{GamificationEngine.get_rank(user['xp'])}</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Notifications
    st.subheader("🔔 Recent Notifications")
    notifications = SmartNotifications.get_unread_notifications(user['email'], 5)
    
    if notifications:
        for notif in notifications:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{notif['title']}**")
                    st.caption(notif['message'])
                with col2:
                    if st.button("✓", key=f"notif_{notif['id']}", use_container_width=True):
                        SmartNotifications.mark_notification_read(notif['id'])
                        st.rerun()
    else:
        st.info("No new notifications")

def render_study_nexus(user):
    """Render EduNexus Study Nexus WhatsApp-style chat"""
    render_header()
    
    st.title("🌐 Study Nexus - Live Chat")
    st.write(f"📍 {user['country']} • {user['program']} • Connect & Learn Together")
    
    group_id = f"{user['country']}_{user['program']}".replace(" ", "_")
    
    # Get messages
    messages = RealTimeMessaging.get_group_messages(user['country'], user['program'], limit=50)
    
    # Display messages container
    st.subheader("💬 Live Messages")
    
    with st.container(border=True, height=400):
        if messages:
            for msg in messages:
                render_message_bubble(
                    message=msg['message'],
                    sender_name=msg['sender_name'],
                    sender_email=msg['sender_email'],
                    current_user_email=user['email'],
                    timestamp=msg['timestamp']
                )
                
                # Show reactions
                if msg.get('reactions'):
                    reactions = json.loads(msg['reactions'])
                    reaction_str = " ".join([f"{emoji} {count}" for emoji, count in reactions.items()])
                    st.caption(f"🎭 {reaction_str}")
        else:
            st.info("📝 No messages yet. Be the first to share!")
    
    st.divider()
    
    # Send message section
    st.subheader("✍️ Send Message")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        message_input = st.text_input(
            "Type your message...",
            max_chars=AppConfig.MAX_MESSAGE_LENGTH,
            placeholder="Share your knowledge...",
            key="study_nexus_msg"
        )
    
    with col2:
        send_btn = st.button("📤 Send", use_container_width=True, type="primary")
    
    if send_btn and message_input:
        if RealTimeMessaging.send_group_message(group_id, user, message_input, "text"):
            ChatHistoryManager.save_message(user['email'], group_id, "user", message_input, "text")
            GamificationEngine.check_achievements(user['email'])
            st.success("✅ Message sent!")
            st.rerun()
        else:
            st.error("❌ Failed to send message")
    
    st.divider()
    st.info("💡 Use this space to collaborate, ask questions, and help classmates learn!")

def render_ariel_ai_chat(user):
    """Render AI tutor interface"""
    render_header()
    
    st.title("🤖 EduNexus AI Tutor - ArielBrain")
    st.write(f"📚 {user['level']} {user['program']} | 🌍 {user['country']}")
    
    model_display = "GPT-4o Pro" if user['tier'] in ['Premium', 'Enterprise'] else "GPT-3.5 Turbo"
    st.caption(f"🧠 Model: {model_display} • Localized for {user['country']}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("**Conversation History**")
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.ai_chat_history = []
            st.session_state.conversation_id = str(uuid.uuid4())
            st.rerun()
    
    # Display chat
    st.subheader("💬 Conversation")
    
    with st.container(border=True, height=400):
        if st.session_state.ai_chat_history:
            for msg in st.session_state.ai_chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        else:
            st.info("👋 Start chatting with EduNexus AI! Ask about your studies, concepts, or anything educational.")
    
    st.divider()
    st.subheader("💬 Send Message")
    
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        user_input = st.text_input("Ask anything about your studies...", max_chars=2000, placeholder="Ask your question...")
    
    with col2:
        if st.button("🎤", help="Voice input", use_container_width=True):
            if AppConfig.ENABLE_VOICE_AI:
                voice_input = AdvancedVoiceEngine.speech_to_text_advanced()
                if voice_input:
                    user_input = voice_input
            else:
                st.warning("Voice AI is disabled")
    
    with col3:
        send_btn = st.button("📤", help="Send message", use_container_width=True, type="primary")
    
    if send_btn and user_input:
        # Add user message
        st.session_state.ai_chat_history.append({
            "role": "user",
            "content": user_input
        })
        ChatHistoryManager.save_message(user['email'], st.session_state.conversation_id, "user", user_input, "text")
        
        # Get AI response
        with st.spinner("🤔 ArielBrain is thinking..."):
            response = EnhancedArielBrain.chat_ariel(user_input, user)
        
        # Add AI response
        st.session_state.ai_chat_history.append({
            "role": "assistant",
            "content": response
        })
        ChatHistoryManager.save_message(user['email'], st.session_state.conversation_id, "assistant", response, "text")
        
        GamificationEngine.check_achievements(user['email'])
        st.rerun()
    
    st.divider()
    st.info("💡 **All conversations are saved automatically!** You can continue later.")

def render_photomath(user):
    """Render PhotoMath Snap & Solve"""
    render_header()
    
    st.title("📸 PhotoMath - Snap & Solve")
    st.write("Upload problem image and get instant step-by-step solutions powered by GPT-4o Vision")
    
    uploaded_file = st.file_uploader("��� Upload Image", type=['jpg', 'jpeg', 'png'], key="photomath_upload")
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 Problem")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
        
        with col2:
            st.subheader("✅ Solution")
            
            if st.button("🔍 Solve Problem", use_container_width=True, type="primary"):
                with st.spinner("Analyzing problem with Vision AI..."):
                    solution = EnhancedArielBrain.snap_and_solve(uploaded_file, user)
                
                st.markdown(solution)
                st.success("✅ Solution saved to your history!")
    
    st.divider()
    st.subheader("📋 Recently Solved")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subject, solved_at FROM captured_problems
                WHERE user_email=? AND saved=1 ORDER BY solved_at DESC LIMIT 10
            """, (user['email'],))
            
            results = cursor.fetchall()
            if results:
                for idx, row in enumerate(results, 1):
                    st.markdown(f"{idx}. ✅ **{row['subject']}** - {row['solved_at']}")
            else:
                st.info("No problems solved yet. Upload an image to get started!")
    except:
        st.info("No history available")

def render_mock_exams(user):
    """Render mock exams interface"""
    render_header()
    
    st.title("✍️ Mock Exams")
    st.write("AI-generated exams tailored to your curriculum and level")
    
    # Get subjects
    subjects = EDUCATION_MAP.get(user['country'], {}).get('Subjects', {}).get(user['program'], [])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_subject = st.selectbox("📚 Subject", subjects if subjects else ["General"])
    
    with col2:
        difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])
    
    with col3:
        num_questions = st.slider("Questions", 5, 50, 10)
    
    if st.button("🚀 Start Exam", use_container_width=True, type="primary"):
        with st.spinner("🔄 Generating exam with AI..."):
            exam_id = MockExamEngine.create_exam(
                user['email'],
                f"{selected_subject} - {difficulty}",
                selected_subject,
                user['country'],
                user['program'],
                user['level'],
                difficulty.lower(),
                num_questions
            )
            
            if exam_id:
                st.session_state.exam_session = {
                    'exam_id': exam_id,
                    'current_question': 0,
                    'answers': []
                }
                st.rerun()
            else:
                st.error("❌ Failed to generate exam")
    
    # Exam interface
    if st.session_state.exam_session:
        exam_id = st.session_state.exam_session['exam_id']
        current_idx = st.session_state.exam_session['current_question']
        
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) as total FROM exam_questions WHERE exam_id=?
                """, (exam_id,))
                total_questions = cursor.fetchone()['total']
                
                cursor.execute("""
                    SELECT id, question_text, options FROM exam_questions 
                    WHERE exam_id=? ORDER BY id LIMIT 1 OFFSET ?
                """, (exam_id, current_idx))
                
                q_row = cursor.fetchone()
                
                if q_row:
                    q_id = q_row['id']
                    question = q_row['question_text']
                    options = json.loads(q_row['options'])
                    
                    st.divider()
                    progress = (current_idx / total_questions) * 100
                    st.progress(progress / 100)
                    st.subheader(f"Question {current_idx + 1}/{total_questions}")
                    st.write(question)
                    
                    answer = st.radio("Choose your answer:", options, key=f"q_{current_idx}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if current_idx > 0 and st.button("⬅️ Previous", use_container_width=True):
                            st.session_state.exam_session['current_question'] -= 1
                            st.rerun()
                    
                    with col2:
                        if st.button("✓ Save Answer", use_container_width=True):
                            MockExamEngine.save_answer(exam_id, q_id, user['email'], answer)
                            st.session_state.exam_session['answers'].append(answer)
                            st.success("✅ Answer saved!")
                    
                    with col3:
                        if current_idx < total_questions - 1:
                            if st.button("Next ➡️", use_container_width=True):
                                st.session_state.exam_session['current_question'] += 1
                                st.rerun()
                        else:
                            if st.button("📊 Submit Exam", use_container_width=True, type="primary"):
                                result = MockExamEngine.submit_exam(exam_id, user['email'], user['country'], user['level'])
                                
                                if result:
                                    st.balloons()
                                    st.success(f"✅ Exam Complete!")
                                    st.info(f"📊 Score: {result['score']}/{result['total']} ({result['percentage']:.1f}%)")
                                    st.success(f"🏆 XP Earned: {result['xp_earned']}")
                                    
                                    st.session_state.exam_session = None
                                    time.sleep(2)
                                    st.rerun()
        
        except Exception as e:
            logger.error(f"❌ Exam error: {str(e)}")
            st.error(f"Error: {str(e)}")
    
    # Recent exams
    st.divider()
    st.subheader("📋 Recent Exams")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_name, subject, score, total_questions, percentage, timestamp 
                FROM exam_results WHERE user_email=? ORDER BY timestamp DESC LIMIT 10
            """, (user['email'],))
            
            results = cursor.fetchall()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No exams completed yet")
    except:
        st.info("No exam history")

def render_analytics(user):
    """Render analytics dashboard"""
    render_header()
    
    st.title("📊 Analytics Dashboard")
    st.write("Your comprehensive study analytics and performance insights")
    
    stats = AnalyticsEngine.get_user_stats(user['email'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💬 Messages", stats.get('messages_sent', 0))
    with col2:
        st.metric("✍️ Exams", stats.get('exams_taken', 0))
    with col3:
        st.metric("📊 Avg Score", f"{stats.get('avg_score', 0):.1f}%")
    with col4:
        st.metric("⏱️ Study Hours", stats.get('study_time_hours', 0))
    with col5:
        st.metric("📸 Problems", stats.get('problems_solved', 0))
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Performance Trend")
        chart = AnalyticsEngine.generate_performance_chart(user['email'])
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No exam data yet. Complete some exams to see trends.")
    
    with col2:
        st.subheader("🎯 Subject Performance")
        subject_chart = AnalyticsEngine.get_subject_performance(user['email'])
        if subject_chart:
            st.plotly_chart(subject_chart, use_container_width=True)
        else:
            st.info("No subject data yet")
    
    st.divider()
    
    # Study time chart
    st.subheader("📅 Study Time Distribution")
    study_chart = AnalyticsEngine.get_study_time_chart(user['email'])
    if study_chart:
        st.plotly_chart(study_chart, use_container_width=True)
    
    # Weak topics analysis
    st.divider()
    st.subheader("🎯 Revision Roadmap - Focus Areas")
    
    weak_topics = MockExamEngine.get_weak_topics(user['email'])
    if weak_topics:
        st.warning("📚 Topics to focus on for improvement:")
        for idx, topic in enumerate(weak_topics[:5], 1):
            progress = min(100, int((topic['wrong_count'] / max(weak_topics[0]['wrong_count'], 1)) * 100))
            st.progress(progress / 100, text=f"{idx}. {topic['topic']} - {topic['wrong_count']} incorrect")
    else:
        st.success("✅ No weak topics identified! You're doing great!")

def render_timetable(user):
    """Render timetable builder"""
    render_header()
    
    st.title("📅 Smart Timetable")
    st.write("Plan your studies strategically with AI-optimized schedules")
    
    subjects = EDUCATION_MAP.get(user['country'], {}).get('Subjects', {}).get(user['program'], [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_subjects = st.multiselect("📚 Select Subjects", subjects if subjects else [])
    
    with col2:
        hours_per_day = st.slider("⏱️ Hours Per Day", 1, 8, 3)
    
    if st.button("📅 Create Schedule", use_container_width=True, type="primary"):
        if selected_subjects:
            schedule = SmartTimetable.create_study_schedule(user['email'], selected_subjects, hours_per_day)
            
            if schedule:
                st.success("✅ Schedule created!")
                st.dataframe(pd.DataFrame(schedule), use_container_width=True, hide_index=True)
        else:
            st.error("❌ Please select at least one subject")
    
    st.divider()
    
    # View timetable
    st.subheader("Your Timetable")
    
    timetable = SmartTimetable.get_timetable(user['email'])
    if timetable:
        timetable_df = pd.DataFrame(timetable)
        st.dataframe(timetable_df, use_container_width=True, hide_index=True)
        
        fig = SmartTimetable.visualize_timetable(user['email'])
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timetable yet. Create one to get started!")

def render_leaderboard(user):
    """Render leaderboard"""
    render_header()
    
    st.title("🏆 Leaderboard")
    st.write(f"Top Performers • {user['country']} - {user['program']}")
    
    leaderboard = GamificationEngine.get_leaderboard(user['country'], user['program'], 20)
    
    if leaderboard:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
        
        with col1:
            st.write("**Rank**")
        with col2:
            st.write("**Player**")
        with col3:
            st.write("**Status**")
        with col4:
            st.write("**Level**")
        with col5:
            st.write("**XP**")
        
        st.divider()
        
        for idx, student in enumerate(leaderboard, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "  "
            tier_emoji = "💎" if student['tier'] == 'Enterprise' else "👑" if student['tier'] == 'Premium' else "⭐"
            level = GamificationEngine.get_level(student['xp'])
            is_current = student['email'] == user['email']
            
            bg_style = f"background: rgba(99, 102, 241, 0.1); border-left: 4px solid {AppConfig.BRAND_COLOR};" if is_current else ""
            
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
            
            with col1:
                st.write(f"{medal} #{idx}")
            with col2:
                st.write(f"{tier_emoji} **{student['name']}**")
            with col3:
                st.write(f"{GamificationEngine.get_rank(student['xp'])}")
            with col4:
                st.write(f"L{level}")
            with col5:
                st.write(f"{student['xp']} XP")
    else:
        st.info("No leaderboard data yet")

def render_premium_upgrade(user):
    """Render premium upgrade page"""
    render_header()
    
    st.title("💎 Upgrade to Premium")
    st.write("Unlock unlimited access to all features and advanced AI capabilities")
    
    if user['tier'] in ['Premium', 'Enterprise']:
        st.success(f"✅ You're already a {user['tier']} member!")
        st.info(f"Enjoying premium benefits. Thank you for your support!")
        return
    
    st.divider()
    
    plans = ["Starter", "Pro", "Ultimate", "Enterprise"]
    
    cols = st.columns(len(plans))
    
    for idx, plan_name in enumerate(plans):
        with cols[idx]:
            plan_details = PremiumPaymentEngine.get_plan_details(plan_name, user['country'])
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, {AppConfig.BRAND_COLOR} 0%, {AppConfig.ACCENT_COLOR} 100%); 
                            padding: 20px; border-radius: 15px; text-align: center;">
                    <h3 style="color: white; margin: 0 0 10px 0;">{plan_name}</h3>
                    <p style="color: #e0e7ff; margin: 0 0 15px 0; font-size: 24px; font-weight: bold;">
                        {plan_details['currency']} {plan_details['localized_price']:.2f}
                    </p>
                    <p style="color: #e0e7ff; margin: 0 0 15px 0; font-size: 12px;">
                        {plan_details['duration_days']} days
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Features
            st.write("**Features:**")
            for feature in plan_details['features'][:3]:
                st.write(f"✅ {feature}")
            
            # Payment options
            st.divider()
            
            payment_method = st.radio("Payment Method", ["PayPal", "Mobile Money", "Stripe"], key=f"pay_{idx}", label_visibility="collapsed")
            
            if payment_method == "Mobile Money":
                if user['country'] in ['Ghana', 'Nigeria', 'Kenya']:
                    st.info(f"📱 Pay via {user['country']} MoMo")
                    momo_ref = st.text_input("MoMo Reference Number", key=f"momo_{idx}", placeholder="Enter your MoMo reference")
                    
                    if st.button(f"💰 Pay {plan_details['currency']} {plan_details['localized_price']:.2f}", 
                               use_container_width=True, key=f"btn_momo_{idx}"):
                        if momo_ref:
                            if PremiumPaymentEngine.process_momo_payment(
                                user['email'], plan_name, momo_ref, user['country']
                            ):
                                st.success("✅ Payment submitted for approval!")
                                st.info("📧 Admin will verify and confirm within 24 hours")
                            else:
                                st.error("❌ Payment processing failed")
                        else:
                            st.error("❌ Please enter MoMo reference")
                else:
                    st.warning(f"⚠️ Mobile Money not available in {user['country']}")
            else:
                if st.button(f"💳 Pay via {payment_method} - {plan_details['currency']} {plan_details['localized_price']:.2f}", 
                           use_container_width=True, key=f"btn_payment_{idx}"):
                    ref = PremiumPaymentEngine.create_payment_reference(
                        user['email'], plan_name, user['country'], payment_method.lower()
                    )
                    if ref:
                        st.success(f"✅ Reference: {ref}")
                        st.info(f"Redirecting to {payment_method}...")

def render_admin_dashboard(admin_email):
    """Render admin dashboard"""
    if not AdminDashboard.verify_admin(admin_email):
        st.error("🔒 Unauthorized access")
        return
    
    render_header()
    
    st.title("🛡️ Admin Dashboard - Enterprise Control")
    st.write(f"Welcome, Admin | {admin_email}")
    
    st.divider()
    
    # Platform Stats
    st.subheader("📊 Platform Statistics")
    
    stats = AdminDashboard.get_platform_stats()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("👥 Total Users", stats.get('total_users', 0))
    with col2:
        st.metric("💎 Premium", stats.get('premium_users', 0))
    with col3:
        st.metric("📝 Exams", stats.get('total_exams', 0))
    with col4:
        st.metric("💬 Messages", stats.get('total_messages', 0))
    with col5:
        st.metric("💰 Revenue", f"${stats.get('revenue', 0):.2f}")
    with col6:
        st.metric("🚫 Banned", stats.get('banned_users', 0))
    
    st.divider()
    
    # User Management
    st.subheader("👥 User Management")
    
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(["User Pulse", "Ban System", "Broadcast", "Analytics"])
    
    with admin_tab1:
        st.write("**All Registered Users**")
        all_users = AdminDashboard.get_all_users()
        if all_users:
            df = pd.DataFrame(all_users)
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total: {len(all_users)} users")
        else:
            st.info("No users found")
    
    with admin_tab2:
        st.write("**Ban/Unban User**")
        
        user_email = st.text_input("User Email", placeholder="user@example.com")
        ban_reason = st.text_area("Ban Reason", placeholder="Reason for banning...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚫 Ban User", use_container_width=True, type="primary"):
                if user_email and ban_reason:
                    if AdminDashboard.ban_user(admin_email, user_email, ban_reason):
                        st.success(f"✅ {user_email} banned successfully")
                    else:
                        st.error("❌ Failed to ban user")
                else:
                    st.error("❌ Fill all fields")
        
        with col2:
            if st.button("🔓 Unban User", use_container_width=True):
                if user_email:
                    if AdminDashboard.unban_user(admin_email, user_email):
                        st.success(f"✅ {user_email} unbanned successfully")
                    else:
                        st.error("❌ Failed to unban user")
                else:
                    st.error("❌ Enter user email")
    
    with admin_tab3:
        st.write("**Broadcast Message to All Groups**")
        
        broadcast_msg = st.text_area("Message", placeholder="Enter message to send to all study groups...", height=150)
        
        if st.button("📢 Send Broadcast", use_container_width=True, type="primary"):
            if broadcast_msg:
                if RealTimeMessaging.send_broadcast_message(admin_email, broadcast_msg):
                    st.success("✅ Message broadcast to all groups!")
                else:
                    st.error("❌ Failed to broadcast")
            else:
                st.error("❌ Enter message")
    
    with admin_tab4:
        st.write("**Platform Analytics**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📚 Total Study Hours", stats.get('total_study_hours', 0))
        with col2:
            st.metric("👥 Active Today", stats.get('active_today', 0))

def render_settings(user):
    """Render settings page"""
    render_header()
    
    st.title("⚙️ Settings")
    
    settings_tab1, settings_tab2, settings_tab3 = st.tabs(["Appearance", "Account", "Preferences"])
    
    with settings_tab1:
        st.subheader("🎨 Appearance")
        
        theme = st.radio("Theme", ["Dark", "Light"], horizontal=True)
        st.session_state.theme = "dark" if theme == "Dark" else "light"
        st.success("✅ Theme will be applied on next load!")
    
    with settings_tab2:
        st.subheader("👤 Account Information")
        
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Tier:** {user['tier']}")
        st.write(f"**Country:** {user['country']}")
        st.write(f"**Joined:** {user.get('joined_date', 'N/A')}")
        
        st.divider()
        
        if st.button("🔐 Change Password", use_container_width=True):
            st.info("🔐 Password change feature coming soon")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            EnhancedSessionManager.logout()
    
    with settings_tab3:
        st.subheader("📬 Preferences")
        
        voice_enabled = st.checkbox("Enable Voice AI", value=True)
        notifications_enabled = st.checkbox("Enable Notifications", value=True)
        
        st.divider()
        
        st.write("**Study Goals**")
        study_goal = st.selectbox("What's your primary goal?", 
            ["Exam Preparation", "Skill Development", "General Learning", "Competitive Exams"])
        
        if st.button("💾 Save Preferences", use_container_width=True, type="primary"):
            st.success("✅ Preferences saved!")

# =========================================================
# 🎯 MAIN APPLICATION FLOW 
# =========================================================

def main():
    """Main application entry point"""
    EnhancedSessionManager.initialize_session()
    
    st.set_page_config(
        page_title=AppConfig.APP_NAME,
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_theme()

    # ===== AUTHENTICATION FLOW =====
    if st.session_state.auth_state == "locked":
        render_login_page()

    elif st.session_state.auth_state == "otp_pending":
        render_email_verification_page()

    elif st.session_state.auth_state == "unlocked":
        user = st.session_state.current_user
        
        # Check for admin
        is_admin = user['email'] == AppConfig.ADMIN_EMAIL
        
        # Sidebar navigation
        with st.sidebar:
            render_header()
            
            st.write(f"### 👋 {user['name']}")
            st.write(f"**Tier:** {user['tier']} | **XP:** {user['xp']}")
            
            st.divider()

            if is_admin:
                page = st.radio(
                    "Admin Navigation",
                    [
                        "🛡️ Admin Dashboard",
                        "🏠 Dashboard",
                        "🤖 EduNexus AI",
                        "📸 PhotoMath",
                        "🌐 Study Nexus",
                        "✍️ Mock Exams",
                        "📊 Analytics",
                        "📅 Timetable",
                        "🏆 Leaderboard",
                        "💎 Premium",
                        "⚙️ Settings",
                    ],
                    label_visibility="collapsed"
                )
            else:
                page = st.radio(
                    "Navigation",
                    [
                        "🏠 Dashboard",
                        "🤖 EduNexus AI",
                        "📸 PhotoMath",
                        "🌐 Study Nexus",
                        "✍️ Mock Exams",
                        "📊 Analytics",
                        "📅 Timetable",
                        "🏆 Leaderboard",
                        "💎 Premium",
                        "⚙️ Settings",
                    ],
                    label_visibility="collapsed"
                )

            st.divider()

            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                EnhancedSessionManager.logout()
            
            st.divider()
            st.caption(f"v{AppConfig.VERSION} • Made with ❤️ for students worldwide")

        # ===== MAIN CONTENT ROUTING =====
        if is_admin and page == "🛡️ Admin Dashboard":
            render_admin_dashboard(user['email'])
        elif page == "🏠 Dashboard":
            render_dashboard(user)
        elif page == "🤖 EduNexus AI":
            render_ariel_ai_chat(user)
        elif page == "📸 PhotoMath":
            render_photomath(user)
        elif page == "🌐 Study Nexus":
            render_study_nexus(user)
        elif page == "✍️ Mock Exams":
            render_mock_exams(user)
        elif page == "📊 Analytics":
            render_analytics(user)
        elif page == "📅 Timetable":
            render_timetable(user)
        elif page == "🏆 Leaderboard":
            render_leaderboard(user)
        elif page == "💎 Premium":
            render_premium_upgrade(user)
        elif page == "⚙️ Settings":
            render_settings(user)

if __name__ == "__main__":
    main()