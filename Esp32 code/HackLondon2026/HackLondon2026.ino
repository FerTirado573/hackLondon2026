#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

// ==============================
// 🔹 USER CONFIG
// ==============================

const char* ssid = "wifi_ssid";
const char* password = "wifi_password";
const char* serverUrl = "https://hacklondon2026.onrender.com/update_occupancy/1/";

// ==============================
// 🔹 DEMO TUNABLES (EDIT THESE)
// ==============================

const unsigned long PIR_SAMPLE_MS = 200;        // how often PIR is read
const unsigned long INACTIVITY_TIMEOUT = 15000; // time to mark EMPTY
const unsigned long MIN_POST_INTERVAL = 3000;   // anti-spam protection

// ==============================
// 🔹 PINS
// ==============================

const int pirPin = 14;
const int ledPin = 2;

// ==============================
// 🔹 STATE
// ==============================

bool occupiedState = false;
unsigned long lastMotionTime = 0;
unsigned long lastPirSample = 0;
unsigned long lastPostTime = 0;

// ==============================
// 🔹 WIFI CONNECT
// ==============================

void connectWiFi() {
  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[SUCCESS] WiFi Connected");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[ERROR] WiFi failed!");
  }
}

// ==============================
// 🔹 SEND TO DJANGO API
// ==============================

void sendOccupancy(bool occupied) {
  if (WiFi.status() != WL_CONNECTED) return;

  // prevent rapid spam
  if (millis() - lastPostTime < MIN_POST_INTERVAL) return;
  lastPostTime = millis();

  String jsonBody = "{\"occupied\": " + String(occupied ? 1 : 0) + "}";

  WiFiClientSecure client;
  client.setInsecure(); // OK for Render / demo

  HTTPClient http;

  Serial.println("\n>>>>> SENDING TO API >>>>>");
  Serial.println(jsonBody);

  if (http.begin(client, serverUrl)) {
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(60000); // Render cold start safety

    int httpCode = http.POST(jsonBody);

    if (httpCode > 0) {
      Serial.printf("Status: %d\n", httpCode);
      Serial.println(http.getString());

      // success blink
      digitalWrite(ledPin, HIGH);
      delay(120);
      digitalWrite(ledPin, LOW);
    } else {
      Serial.printf("HTTP Error: %s\n",
                    http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}

// ==============================
// 🔹 SETUP
// ==============================

void setup() {
  Serial.begin(115200);

  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.println("Booting...");
  connectWiFi();

  Serial.println("PIR warming up...");
  delay(30000); // PIR stabilization (important)
  Serial.println("System ready.");
}

// ==============================
// 🔹 MAIN LOOP
// ==============================

void loop() {
  unsigned long now = millis();

  // ------------------------------
  // Read PIR periodically
  // ------------------------------
  if (now - lastPirSample >= PIR_SAMPLE_MS) {
    lastPirSample = now;

    int pirState = digitalRead(pirPin);

    if (pirState == HIGH) {
      Serial.println("Motion detected");

      lastMotionTime = now;
      digitalWrite(ledPin, HIGH);

      // EMPTY → OCCUPIED (instant wake)
      if (!occupiedState) {
        occupiedState = true;
        Serial.println("STATE → OCCUPIED");
        sendOccupancy(true);
      }

    } else {
      digitalWrite(ledPin, LOW);
    }
  }

  // ------------------------------
  // OCCUPIED → EMPTY after inactivity
  // ------------------------------
  if (occupiedState &&
      (now - lastMotionTime > INACTIVITY_TIMEOUT)) {

    occupiedState = false;
    Serial.println("STATE → EMPTY");
    sendOccupancy(false);
  }
}
