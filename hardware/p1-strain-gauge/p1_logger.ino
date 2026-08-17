// Vyldor P1 — strain-gauge logger.
//
// Reads a half-bridge (active gauge on the strap + dummy gauge on unloaded leather,
// completed by two 0.1% 350R resistors) through an HX711 and prints timestamped CSV.
//
// The HX711 is bit-banged rather than driven by a library on purpose: the library
// versions differ in how they handle the 80 SPS rate pin and in whether they block,
// and this test is worthless if samples are silently dropped or unevenly spaced.
// Everything here is explicit so the timing can be checked against the output.
//
// Wiring (ESP32):  DT -> GPIO16,  SCK -> GPIO4,  VCC -> 3V3,  GND -> GND
// Set the HX711 RATE pad to HIGH (80 SPS) if your board exposes it. At 10 SPS you
// can still see breathing, but walking cadence (~2 Hz) aliases badly.

const int PIN_DT  = 16;
const int PIN_SCK = 4;

// Channel A, gain 128 — the highest gain, which is what a strain gauge bridge needs.
// 25 clock pulses selects it. (26 = A/64, 27 = B/32.)
const int GAIN_PULSES = 25;

// Label the block you are recording so analyse.py can split the file without you
// having to cut it by hand. Type a new label into the serial monitor at any time.
String block = "klid";

bool ready() { return digitalRead(PIN_DT) == LOW; }

long readRaw() {
  while (!ready()) { delay(1); }

  long value = 0;
  noInterrupts();                 // a 24-bit shift-in that gets interrupted is garbage
  for (int i = 0; i < 24; i++) {
    digitalWrite(PIN_SCK, HIGH);
    delayMicroseconds(1);
    value = (value << 1) | digitalRead(PIN_DT);
    digitalWrite(PIN_SCK, LOW);
    delayMicroseconds(1);
  }
  for (int i = 24; i < GAIN_PULSES; i++) {
    digitalWrite(PIN_SCK, HIGH);
    delayMicroseconds(1);
    digitalWrite(PIN_SCK, LOW);
    delayMicroseconds(1);
  }
  interrupts();

  // 24-bit two's complement -> signed long
  if (value & 0x800000L) value |= ~0xFFFFFFL;
  return value;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_SCK, OUTPUT);
  pinMode(PIN_DT, INPUT);
  digitalWrite(PIN_SCK, LOW);
  delay(500);

  // A saturated reading means the bridge is not a bridge. Say so here rather than
  // letting someone record twenty minutes of 8388607 and analyse it later.
  long probe = readRaw();
  if (probe >= 8388600L || probe <= -8388600L) {
    Serial.println("# CHYBA: HX711 je v saturaci (" + String(probe) + ").");
    Serial.println("# Skoro jiste mas na vstupu jeden tenzometr misto mustku.");
    Serial.println("# Zkontroluj, ze A+ i A- sedi na delicich mezi E+ a E-.");
  }

  Serial.println("# vyldor-p1 v1");
  Serial.println("ms,block,raw");
}

void loop() {
  if (Serial.available()) {
    String incoming = Serial.readStringUntil('\n');
    incoming.trim();
    if (incoming.length() > 0) {
      block = incoming;
      Serial.println("# block -> " + block);
    }
  }

  long raw = readRaw();
  Serial.print(millis());
  Serial.print(',');
  Serial.print(block);
  Serial.print(',');
  Serial.println(raw);
}
