#define RS485_PIN 3
#include <SoftwareSerial.h>

SoftwareSerial mySerial(7, 6); // RX, TX
String request = "";

void setup() {
    mySerial.begin(9600);
    Serial.begin(9600);
    pinMode(RS485_PIN, OUTPUT);
    digitalWrite(RS485_PIN, LOW); // Start in receive mode
    Serial.println("Arduino RS485 Ready.");
}

void loop() {
    if (mySerial.available() > 0) {
        char incomingByte = mySerial.read();
        request += incomingByte;
        if (incomingByte == '\n') {
            Serial.println("Received full request: " + request);
            if (request.startsWith("s2")) {
                digitalWrite(RS485_PIN, HIGH); // Switch to transmit mode
                delay(50);
                mySerial.println("slave 2 XD"); // Replace with actual data to send
                delay(50);
                digitalWrite(RS485_PIN, LOW); // Switch back to receive mode
                Serial.println("Sent response!");
            }
            request = "";
        }
    }
}
