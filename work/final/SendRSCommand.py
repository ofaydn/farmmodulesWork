import serial
import RPi.GPIO as GPIO
import time

# RS485 Direction Control Pin
RS485_DE_RE_PIN = 4  # Pin used to control the transmit/receive mode of RS485

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode to BCM (Broadcom)
GPIO.setup(RS485_DE_RE_PIN, GPIO.OUT)   # Set RS485 control pin as output
GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)  # Start in listening (receive) mode

# Setup serial connection
try:
    ser = serial.Serial(
        port='/dev/serial0',            # Specify the correct serial port    #
        baudrate=19200,                 # Set baud rate
        parity=serial.PARITY_NONE,      # No parity bit
        stopbits=serial.STOPBITS_ONE,   # One stop bit
        bytesize=serial.EIGHTBITS,      # 8 data bits
        timeout=1                       # Timeout for read operations
    )
except serial.SerialException as e:
    # If there's an issue connecting to the serial port, exit
    print(f"Failed to connect to serial port: {e}")
    exit(1)

# Function to send a command via RS485
def send_request(command):
    full_command = f'{command}\n'            # Append newline to the command 
    GPIO.output(RS485_DE_RE_PIN, GPIO.HIGH)  # Switch GPIO to HIGH to transmit 
    time.sleep(0.05)                         # Short delay before transmission
    ser.write(full_command.encode('utf-8'))  # Send the command as bytes
    print(f"Request sent: '{full_command.strip()}'")  # Print the confirmation
    time.sleep(0.05)                         # Short delay after transmission
    GPIO.output(RS485_DE_RE_PIN, GPIO.LOW)   # Switch GPIO to LOW for receive 

# Function to receive a response via RS485
def receive_response():
    responses = []             # List to collect all valid responses
    timeout = time.time() + 2  # 2-second window to collect responses
    while True:
        if ser.in_waiting > 0:  # Check if there is data available to read 
            try:
                # Read a line of data from the serial port and decode it
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if data.isprintable():  
                    responses.append(data) # Append data to the responses list
            except UnicodeDecodeError:
                # If there is an error in decoding, skip this data
                print("Received non-UTF-8 data, skipping...")
                continue
        if time.time() > timeout:  # Break the loop if the timeout has passed
            break
    return responses  # Return the list of responses received

# Main function to handle user input and send/receive commands via RS485
def main():
    print("Welcome!")  # Greet the user
    while True:
        command = input("Enter command to send (or type 'exit' to quit): ")

        if command.lower() == 'exit':   # Check if the user wants to exit 
            print("Exiting.")           
            ser.close()                 # Close the serial connection
            GPIO.cleanup()              # Clean up GPIO settings
            exit(0)                     

        send_request(command)           # Send the command entered by the user
        responses = receive_response()  # Get the response from the device
        if responses:                   # If any responses were received
            for response in responses:  # Print each response
                print(f"Received response: {response}")
        else:
            print("No valid response received.") 

# If this script is run directly, start the main loop
if __name__ == "__main__":
    try:
        main()  # Start the main function
    except KeyboardInterrupt:
        # Handle program termination via Ctrl+C
        ser.close()                             # Close the serial connection
        GPIO.cleanup()                          # Clean up GPIO settings
        print("\nProgram terminated by user.")  # Print the program has ended
