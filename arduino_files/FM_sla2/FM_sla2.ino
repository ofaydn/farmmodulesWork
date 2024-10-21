#define RS485_PIN 3
#include <SoftwareSerial.h>

SoftwareSerial mySerial(7, 6); // RX, TX

char request[100];  
int index = 0;

void setup() {
    mySerial.begin(9600);
    Serial.begin(9600);
    pinMode(RS485_PIN, OUTPUT);
    digitalWrite(RS485_PIN, LOW); // Start in receive mode
    Serial.println("SLA2 Ready.");
    randomSeed(analogRead(A0)); 
}


void loop() {
    if (mySerial.available() > 0) {
        char incomingByte = mySerial.read();
        request[index++] = incomingByte;
        request[index] = '\0';  // Null-terminate the string

        if (incomingByte == '\n') {
            processRequest(request);
            index = 0;  // Reset index for next request
        }
    }
}

void processRequest(char* request) {
    Serial.println("Received full request: " + String(request)); // Convert to String for printing

    if (strncmp(request, "sla2", 4) == 0) {
        char* remainingRequest = request + 4;  // Skip "sla1"

        if (strncmp(remainingRequest, "_do", 3) == 0) {
            manageAtlasDO(remainingRequest + 3);
        } else if (strncmp(remainingRequest, "_ph", 3) == 0) {
            manageAtlasPH(remainingRequest + 3);
        } else if (strncmp(remainingRequest, "_ammonia", 8) == 0) {
            manageAmmonia(remainingRequest + 8);
        } else if (strncmp(remainingRequest, "_nitrates", 9) == 0) {
            manageNitrates(remainingRequest + 9);
        } else if (strncmp(remainingRequest, "_temp", 5) == 0) {
            manageTemp(remainingRequest + 5);
        } else {
            sendRSData("SLA2 unrecognized sub-command.");
        }
      request[0] = '\0';
    }
}

void manageAtlasDO(char* request) {
  if (strncmp(request, "_r", 2) == 0) {
    String cdata =  generateRandomData(0,1);  // Call the nested function to generate random data
    const char* data = cdata.c_str();
    sendRSData(data);
  } else {
    sendRSData("{\"*Error\":\"Invalid request from SLA2-DO\"}");
  }
}

void manageAtlasPH(char* request) {
  if (strncmp(request, "_r", 2) == 0) {
    String cdata =  generateRandomData(0,14);  // Call the nested function to generate random data
    const char* data = cdata.c_str();
    sendRSData(data);
  } else {
    sendRSData("{\"*Error\":\"Invalid request from SLA2-PH\"}");
  }
}

void manageAmmonia(char* request) {
  if (strncmp(request, "_r", 2) == 0) {
    String cdata =  generateRandomData(0,10);  // Call the nested function to generate random data
    const char* data = cdata.c_str();
    sendRSData(data);
  } else {
    sendRSData("{\"*Error\":\"Invalid request from SLA2-Ammonia\"}");
  }
}

void manageNitrates(char* request) {
  if (strncmp(request, "_r", 2) == 0) {
    String cdata =  generateRandomData(0,50);  // Call the nested function to generate random data
    const char* data = cdata.c_str();
    sendRSData(data);
  } else {
    sendRSData("{\"*Error\":\"Invalid request from SLA2-Nitrates\"}");
  }
}

void manageTemp(char* request) {
  if (strncmp(request, "_r", 2) == 0) {
    String cdata =  generateRandomData(0,50);  // Call the nested function to generate random data
    const char* data = cdata.c_str();
    sendRSData(data);
  } else {
    sendRSData("{\"*Error\":\"Invalid request from SLA2-Temp\"}");
  }
}

String generateRandomData(float lowerLimit, float upperLimit) {
    float randomValue = random(lowerLimit * 1000, upperLimit * 1000 + 1) / 1000.0;  // Generate a random value within limits with 3 decimal places
    String response = "{\"*OK\":\"";
    response += String(randomValue, 3);  // Add the random value with 3 decimal places
    response += "\"}";
    return response;
}



void sendRSData(const char* data) {
    digitalWrite(RS485_PIN, HIGH);  // Switch to transmit mode
    delay(150);  // Wait for mode switch
    mySerial.println(data);  // Send the actual data
    delay(150);  // Wait for data transmission
    digitalWrite(RS485_PIN, LOW);  // Switch back to receive mode
    Serial.println("Sent response: " + String(data));
}
