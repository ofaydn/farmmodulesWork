//Omer Faruk Aydin 18/09/2024
#include <SoftwareSerial.h>

#define rs485_pin 2             // Pin to control RS485 direction
#define atlas_ph_rx 10          // RX pin for pH sensor (Atlas sensor)
#define atlas_ph_tx 9           // TX pin for pH sensor (Atlas sensor)
#define atlas_do_rx 12          // RX pin for DO sensor (Atlas sensor)
#define atlas_do_tx 11          // TX pin for DO sensor (Atlas sensor)

SoftwareSerial atlasph(atlas_ph_tx, atlas_ph_rx);    // SoftwareSerial object for pH sensor
SoftwareSerial atlasdo(atlas_do_tx, atlas_do_rx);    // SoftwareSerial object for DO sensor

String request = "";
String sensorData = "";

void setup() {
  pinMode(rs485_pin, OUTPUT);    // Set RS485 control pin as OUTPUT
  digitalWrite(rs485_pin, LOW);  // Initially set to receive mode (LOW)

  Serial.begin(19200);           // RS485 communication at 19200 baud
  Serial.println("Setup completed. Ready to receive commands.");

  // Initialize the sensors but start with them disabled
  atlasph.begin(9600);           // pH sensor (Atlas)
  atlasdo.begin(9600);           // DO sensor (Atlas)
  atlasph.listen();              // Enable listening on pH sensor first
}

void loop() {
  // Receive command from RS485 (master)
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();      // Read incoming byte from RS485
    request += incomingByte;                // Append byte to request string
    String remainder = "";

    if (incomingByte == '\n') {             // Check for end of command
      if (request.startsWith("do")) {
        remainder = request.substring(2);   // Command for DO sensor
        atlasdo.listen();                   // Switch to DO sensor
        atlasdo.print(remainder + "\r");    // Send command to DO sensor
      }
      if (request.startsWith("ph")) {
        remainder = request.substring(2);   // Command for pH sensor
        atlasph.listen();                   // Switch to pH sensor
        atlasph.print(remainder + "\r");    // Send command to pH sensor
      }

      // Clear the request for the next command
      request = "";
      remainder = "";
      delay(50);  // Allow time for the sensor to process the command
    }
  }

  // Check for data from the sensors
  if (atlasdo.isListening() && atlasdo.available() > 0) {
    sensorData = atlasdo.readStringUntil('\r');  // Read DO sensor data

    digitalWrite(rs485_pin, HIGH);               // Switch to transmit mode for RS485
    delay(50);
    Serial.println(sensorData);                  // Send the data to RS485
    delay(50);
    digitalWrite(rs485_pin, LOW);                // Switch back to receive mode
    sensorData = "";
  }

  if (atlasph.isListening() && atlasph.available() > 0) {
    sensorData = atlasph.readStringUntil('\r');  // Read pH sensor data

    digitalWrite(rs485_pin, HIGH);               // Switch to transmit mode for RS485
    delay(50);
    Serial.println(sensorData);                  // Send the data to RS485
    delay(50);
    digitalWrite(rs485_pin, LOW);                // Switch back to receive mode
    sensorData = "";
  }
}
