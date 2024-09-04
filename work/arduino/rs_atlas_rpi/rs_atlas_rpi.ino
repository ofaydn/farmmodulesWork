#include <SoftwareSerial.h>

#define RS485_PIN 2
#define DO_RX 5
#define DO_TX 4

String request = "";
SoftwareSerial doSerial(DO_RX, DO_TX);

void setup() {
  pinMode(RS485_PIN, OUTPUT);
  digitalWrite(RS485_PIN, LOW);
  Serial.begin(19200);
  doSerial.begin(9600);

}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    request += incomingByte;
    
    if (incomingByte == '\n') {  // End of the command
      Serial.print("Received full request: ");
      Serial.println(request);
      String command = request;  // Read the command from the Serial Monitor
      doSerial.print(command + "\r");  // Send the command to the sensor
      //THIS SERIES OF LINE ADDED LATER
      String sensorData = "";
      digitalWrite(RS485_PIN, HIGH);
        // Short delay for mode switch
        delay(50);
      if(doSerial.available()>0){
        sensorData = doSerial.readStringUntil('\r');// Read data until carriage return  
      }else{
        sensorData = "Unable to read data\n";
      }
      Serial.println(sensorData);
      
      //Serial.println("slave1");  // Send the response
      delay(50);  // Ensure the response is fully sent
      digitalWrite(RS485_PIN, LOW);  // Disable RS485 transmit mode  
      }

      request = "";  // Clear the request for the next command
    
  }
}
