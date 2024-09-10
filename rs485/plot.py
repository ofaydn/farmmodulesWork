import matplotlib.pyplot as plt
import pandas as pd

# Load data from the log file
log_file_path = 'sensor_data_log.csv'
data = pd.read_csv(log_file_path, names=['Timestamp', 'Temperature'])

# Convert Timestamp to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Plot the temperature data
plt.figure(figsize=(10, 5))
plt.plot(data['Timestamp'], data['Temperature'], marker='o', linestyle='-')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Trends Over Time')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as an image
plt.savefig('temperature_trends.png')
plt.show()
