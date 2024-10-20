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
    randomSeed(analogRead(A0)); 
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
                  else if (remainingRequest.startsWith("_ph")) {
                      
                      String req_substring = remainingRequest.substring(3);
                      manageAtlasPH(req_substring);

                  }
                  else if (remainingRequest.startsWith("_ammonia")) {
                      
                      String req_substring = remainingRequest.substring(8);
                      manageAmmonia(req_substring);

                  }
                  else if (remainingRequest.startsWith("_nitrates")) {
                      
                      String req_substring = remainingRequest.substring(9);
                      manageNitrates(req_substring);

                  }
                  else if (remainingRequest.startsWith("_temp")) {
                      
                      String req_substring = remainingRequest.substring(5);
                      manageTemp(req_substring);
                      
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

  // Check if the request starts with "r"
  if (request.startsWith("_r")) {
    String data =  generateRandomData(0,1);  // Call the nested function to generate random data
    sendRSData(data);
  } else {
    // Default response if the request doesn't start with "r"
    sendRSData("{\"*Error\":\"Invalid request from SLA1-DO\"}");
  }
}

String manageAtlasPH(String request){

  if (request.startsWith("_r")) {
    String data =  generateRandomData(0,14);  // Call the nested function to generate random data
    sendRSData(data);
  } else {
    // Default response if the request doesn't start with "r"
    sendRSData("{\"*Error\":\"Invalid request from SLA1-DO\"}");
  }

}

String manageAmmonia(String request){

  if (request.startsWith("_r")) {
    String data =  generateRandomData(0,10);  // Call the nested function to generate random data
    sendRSData(data);
  } else {
    // Default response if the request doesn't start with "r"
    sendRSData("{\"*Error\":\"Invalid request from SLA1-DO\"}");
  }

}

String manageNitrates(String request){

  if (request.startsWith("_r")) {
    String data =  generateRandomData(0,50);  // Call the nested function to generate random data
    sendRSData(data);
  } else {
    // Default response if the request doesn't start with "r"
    sendRSData("{\"*Error\":\"Invalid request from SLA1-DO\"}");
  }
}

String manageTemp(String request){
  if (request.startsWith("_r")) {
    String data =  generateRandomData(0,50);  // Call the nested function to generate random data
    sendRSData(data);
  } else {
    // Default response if the request doesn't start with "r"
    sendRSData("{\"*Error\":\"Invalid request from SLA1-DO\"}");
  }
}

String generateRandomData(float lowerLimit, float upperLimit) {
    float randomValue = random(lowerLimit * 1000, upperLimit * 1000 + 1) / 1000.0;  // Generate a random value within limits with 3 decimal places
    String response = "{\"*OK\":\"";
    response += String(randomValue, 3);  // Add the random value with 3 decimal places
    response += "\"}";
    return response;
}

void sendRSData(String data) {
    digitalWrite(RS485_PIN, HIGH); // Switch to transmit mode
    delay(50); // Give time to switch modes
    mySerial.println(data); // Send the actual data
    delay(50); // Allow time for data transmission
    digitalWrite(RS485_PIN, LOW); // Switch back to receive mode
    Serial.println("Sent response " + data + "!");
}


