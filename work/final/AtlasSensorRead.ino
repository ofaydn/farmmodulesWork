#include <SoftwareSerial.h>  // Include the SoftwareSerial library

#define tx 3                 // Define the TX pin
#define rx 4                 // Define the RX pin

SoftwareSerial atlasSensor(tx, rx);  // Create a software serial port

void setup() {
  Serial.begin(9600);           // Start the serial communication with the computer
  atlasSensor.begin(9600);      // Start the serial communication with the sensor
  atlasSensor.write("c,0");     // Sets sensor read interval to 0
  atlasSensor.write("\r");      // Sends the command to the sensor
  Serial.println("Starting communication with sensor...");
}

void loop() {
  // Check if data is available from the sensor
  if (atlasSensor.available() > 0) {
    String sensorData = atlasSensor.readStringUntil('\r');  // Read data until carriage return
    Serial.print("Sensor Data: "); 
    Serial.println(sensorData); // Print the sensor data to the Serial Monitor
  }
  
  // Check if data is available from the Serial Monitor (PC)
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');          // Read the command from the Serial Monitor
    atlasSensor.print(command + "\r");                      // Send the command to the sensor
  }
}
