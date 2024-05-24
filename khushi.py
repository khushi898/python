import serial
import time
import pandas as pd
import matplotlib.pyplot as plt

# Configure the serial connection
ser = serial.Serial('COM3', 9600)  # Update 'COM3' to the appropriate port for your system
time.sleep(2)  # Wait for connection to establish



# Lists to store data
data = {
    "time": [],
    "heart_rate": [],
    "spo2": [],
    "calories_burned": [],
    "steps": [],
    "sleep_stage": []
}

# Current time and start of the day (midnight)
current_time = time.localtime()
start_of_day = time.strptime(f"{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} 00:00:00", "%Y-%m-%d %H:%M:%S")
current_timestamp = time.mktime(current_time)
start_timestamp = time.mktime(start_of_day)

# Read data from Arduino
index = 0
try:
    while start_timestamp < current_timestamp:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            heart_rate, spo2, calories_burned, steps, sleep_stage = line.split(',')
            formatted_time = time.strftime("%H:%M", time.gmtime(start_timestamp - time.mktime(start_of_day)))

            # Append data to lists
            data["time"].append(formatted_time)
            data["heart_rate"].append(int(heart_rate))
            data["spo2"].append(int(spo2))
            data["calories_burned"].append(int(calories_burned))
            data["steps"].append(int(steps))
            data["sleep_stage"].append(sleep_stage)

            # Print to console (optional)
            print(f"Time: {formatted_time}, Heart Rate: {heart_rate}, SpO2: {spo2}, Calories Burned: {calories_burned}, Steps: {steps}, Sleep Stage: {sleep_stage}")

            start_timestamp += 3600  # Increment by 1 hour
            index += 1
            
except KeyboardInterrupt:
    print("Exiting program")

# Convert data to DataFrame
df = pd.DataFrame(data)

# # Save to CSV
# df.to_csv('health_data.csv', index=False)

# Visualize data
# plt.figure(figsize=(10, 6))
# plt.plot(df["time"], df["heart_rate"], label="Heart Rate")
# plt.plot(df["time"], df["spo2"], label="SpO2")
# plt.plot(df["time"], df["calories_burned"], label="Calories Burned")
# plt.plot(df["time"], df["steps"], label="Steps")
# plt.xlabel("Time")
# plt.xticks(rotation=45)
# plt.ylabel("Values")
# plt.title("Health Data Over Time")
# plt.legend()
# plt.tight_layout()
# plt.show()

# Plot data
plt.clf()  # Clear the previous plot
# plt.figure(figsize=(10,6))
plt.subplot(5, 1, 1)
plt.plot(df["time"], df["heart_rate"], label='Heart Rate')
plt.title('Heart Rate')

plt.subplot(5, 1, 2)
plt.plot(df["time"], df["spo2"], label='SpO2')
plt.title('SpO2')

plt.subplot(5, 1, 3)
plt.plot(df["time"], df["calories_burned"], label='Calories')
plt.title('Calories Burned')

plt.subplot(5, 1, 4)
plt.plot(df["time"], df["steps"], label='Steps')
plt.title('Steps')

plt.subplot(5, 1, 5)
plt.plot(df["time"], df["steps"], label='Sleep')
plt.title('Sleep Hours')


plt.legend()
plt.tight_layout()

plt.ioff()  # Turn off interactive mode
plt.show()

ser.close()


def provide_recommendations(df):
    recommendations = []

    if df["heart_rate"].mean() > 100:
        recommendations.append("Your average heart rate is high. Consider relaxing activities.")
    if df["spo2"].mean() < 95:
        recommendations.append("Your SpO2 levels are low. Ensure proper ventilation and consult a doctor if necessary.")
    if df["calories_burned"].sum() < 2000:
        recommendations.append("You need to burn more calories. Consider increasing your physical activity.")
    if df["steps"].sum() < 10000:
        recommendations.append("Try to walk more. Aim for at least 10,000 steps a day.")
    if df["sleep_stage"].value_counts().get("Deep Sleep", 0) < 2:
        recommendations.append("You need more deep sleep. Maintain a regular sleep schedule.")

    return recommendations

# Provide recommendations based on the data
recommendations = provide_recommendations(df)
for rec in recommendations:
    print(rec)
