# 🚀 Smart Space: Real-Time Study Analytics & Booking

**HackLondon 2026 Submission** *Optimizing campus resources through IoT-driven presence detection.*



---

## 💡 The Problem
Students often wander campus for 20+ minutes looking for a free desk, only to find "Ghost Bookings"—desks reserved online but physically empty. Existing systems rely on trust; **Smart Space** relies on data.

## 🛠️ The Solution
A full-stack ecosystem that bridges the gap between digital reservations and physical reality.
* **The Web App:** A Django-powered dashboard for students to find, book, and manage study spaces.
* **The Hardware:** Wall-mounted ESP32 units with PIR (Passive Infrared) sensors that monitor physical occupancy in real-time.
* **The Brain:** An automated "Inactivity Guardian" that releases bookings if a student hasn't shown up within 10 minutes.

---

## 🧠 Features & Logic

### 📡 IoT Presence Monitoring
The hardware isn't just a motion sensor; it's a smart client. It monitors infrared signatures and sends encrypted POST requests to our cloud API.
* **Instant Feedback:** The built-in LED on the ESP32 provides immediate visual confirmation of detection.
* **Smart Debouncing:** Logic-level filtering to ensure that a student simply sitting still for a second doesn't trigger a "false empty" state.

### ⏳ The "Auto-Release" Feature
The highlight of our system's efficiency.
1. **Booking Initialized:** A student reserves a space.
2. **Monitoring:** The ESP32 tracks activity.
3. **The 10-Min Rule:** If the hardware reports **0 motion** for a continuous 10-minute window during a reservation, the system intelligently cancels the booking and notifies the community that the desk is free.



---

## 🏗️ Tech Stack

**Hardware:**
* **ESP32 Microcontroller** (C++/Arduino)
* **HC-SR501 PIR Sensor** (Physical Presence detection)
* **Secure HTTPS Communication** (WiFiClientSecure)

**Software:**
* **Backend:** Django (Python)
* **Database:** SQLite
* **Infrastructure:** Render Cloud (Deployed Web Service)
* **Frontend:** Responsive Web Dashboard

---

## 📸 Project Gallery
*Showcasing the intersection of hardware and software.*



> **Wall-Mount Setup:** Our final product is designed to be hung at a 45-degree angle to provide a "conic" detection field over study desks.

---

## 🏆 Hackathon Achievements
* Successfully implemented **End-to-End Encryption** between IoT hardware and Cloud API.
* Reduced potential "dead space" time by implementing the **10-minute automated release cycle**.
* Built and deployed a fully functional live product in under 24 hours.

---
*Developed with ❤️ at HackLondon 2026*
