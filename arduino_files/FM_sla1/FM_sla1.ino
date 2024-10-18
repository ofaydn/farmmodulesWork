#define RS485_PIN 3
#include <SoftwareSerial.h>

SoftwareSerial mySerial(7, 6); // RX, TX
String request = "";

void setup() {
    mySerial.begin(9600);
    Serial.begin(9600);
    pinMode(RS485_PIN, OUTPUT);
    digitalWrite(RS485_PIN, LOW); // Start in receive mode
    Serial.println("SLA1 Ready.");
}

void loop() {
    if (mySerial.available() > 0) {
        char incomingByte = mySerial.read();
        request += incomingByte;
        if (incomingByte == '\n') {
            Serial.println("Received full request: " + request);
            if (request.startsWith("sla1")) {
            // Remove "sla1" from the request to analyze the remaining part
                String remainingRequest = request.substring(4);

                  // Further parse the remaining part
                if (remainingRequest.startsWith("_do")) {
                      // Perform action for "sla1_do"
                      String req_substring = remainingRequest.substring(3);
                      manageAtlasDO(req_substring);    
                  }
                  else if (remainingRequest.startsWith("_temp")) {
                      // Perform action for "sla1_temp"
                      sendRSData("SLA1 temperature sensor data.");
                  }
                  else {
                      // If no specific sub-command matches
                      sendRSData("SLA1 unrecognized sub-command.");
                  }
        }
            request = "";
        }
    }
}

String manageAtlasDO(String request) {

  // Nested function to generate random data
  auto generateRandomData = []() {
    float randomValue = random(0, 14001) / 1000.0;  // Random value with 3 decimal places
    String response = "{\"*OK\":\"";
    response += String(randomValue, 3);  // Add the random value with 3 decimal places
    response += "\"}";
    return response;
  };

  // Check if the request starts with "r"
  if (request.startsWith("_cal")) {
    String data =  generateRandomData();  // Call the nested function to generate random data
    sendRSData(data);
  } else {
    // Default response if the request doesn't start with "r"
    sendRSData("{\"*Error\":\"Invalid request from SLA2\"}");
  }
}


void sendRSData(String data) {
    digitalWrite(RS485_PIN, HIGH); // Switch to transmit mode
    delay(50); // Give time to switch modes
    mySerial.println(data); // Send the actual data
    delay(50); // Allow time for data transmission
    digitalWrite(RS485_PIN, LOW); // Switch back to receive mode
    Serial.println("Sent response " + data + "!");
}


