#define RS485_PIN 2

String request = "";

void setup() {
  pinMode(RS485_PIN, OUTPUT);
  digitalWrite(RS485_PIN, LOW);
  Serial.begin(19200);
  //dht11.begin();

}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    request += incomingByte;
    
    if (incomingByte == '\n') {  // End of the command
      Serial.print("Received full request: ");
      Serial.println(request);

      if (request.startsWith("s1")) {
        digitalWrite(RS485_PIN, HIGH);  // Enable RS485 transmit mode
        delay(50);  // Short delay for mode switch
        Serial.println("c,0\r");  // Send the response
        delay(50);  // Ensure the response is fully sent
        digitalWrite(RS485_PIN, LOW);  // Disable RS485 transmit mode
      }

      request = "";  // Clear the request for the next command
    }
  }
}
