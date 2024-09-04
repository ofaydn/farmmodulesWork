#include <SoftwareSerial.h>  // Include the SoftwareSerial library

#define rx 5                 // Define the RX pin
#define tx 4                 // Define the TX pin

SoftwareSerial mySerial(rx, tx);  // Create a software serial port

void setup() {
  Serial.begin(9600);        // Start the serial communication with the computer
  mySerial.begin(9600);      // Start the serial communication with the sensor
  
  Serial.println("Starting communication with sensor...");
}

void loop() {
  // Check if data is available from the sensor
 /*if (mySerial.available() > 0) {
    String sensorData = mySerial.readStringUntil('\r');  // Read data until carriage return
    Serial.print("Sensor Data: "); 
    Serial.println(sensorData);  // Print the sensor data to the Serial Monitor
  }*/
  
  // Check if data is available from the Serial Monitor (PC)
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the command from the Serial Monitor
    mySerial.print(command + "\r");  // Send the command to the sensor
    //THIS SERIES OF LINE ADDED LATER
    String sensorData = mySerial.readStringUntil('\r');  // Read data until carriage return
    Serial.print("Sensor Data: "); 
    Serial.println(sensorData);
  }
}
