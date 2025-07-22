#SmartFreezeAI
#Authors: Rohan Senapati and Sai Utkarsh Choudarypally
#License: Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)

#Description:
#This Python program simulates a smart refrigerator system that adjusts ice production 
#based on simulated user behavior and environmental conditions. It includes sensor-driven 
#logic, adaptive control flow, and real-time data visualization.

#Collaboration Note:
#This project was co-developed by Rohan and Sai. Both collaborated on design and testing.


import random, time, matplotlib.pyplot as plt

Weight = [round(i * 0.1, 1) for i in range(41)]
Temperature = list(range(-10, 1))
Usage_Pattern = list(range(1, 21))

class IceBinSensor:
    def __init__(self): self.weight = random.choice(Weight)
    def get_weight(self): return self.weight
    def update_weight(self, change): self.weight = min(4, max(0, self.weight + change))

class TemperatureSensor:
    def __init__(self): self.temperature = random.choice(Temperature)
    def get_temperature(self): return self.temperature

class UsagePatternSensor:
    def __init__(self): self.usage = random.choice(Usage_Pattern)
    def get_usage(self): return self.usage

def adjust_production_rate(usage, weight):
    thresholds = [(20,10,2.5),(18,9,2.25),(16,8,2.0),(14,7,1.75),(12,6,1.5),(10,5,1.25),(8,4,1.0),(6,3,0.75),(4,2,0.5),(2,1,0.25)]
    for i, j, delta in thresholds:
        if usage >= i: 
            return j, weight + delta
    return 0, weight

def adjust_temperature(usage): return max(-10, -((usage + 1) // 2))

def adjust_sensors(usage, sensor):
    rate, new_weight = adjust_production_rate(usage, sensor.get_weight())
    sensor.update_weight(new_weight - sensor.get_weight())
    if usage > 0: 
        sensor.update_weight(-0.2)
    for i in range(3): 
        print(f"Sensor check {i + 1}")
    new_temp = adjust_temperature(usage)
    time.sleep(1)
    print("                _________                   ")
    print(f"Adjusted Temperature: {round(new_temp, 2)} Fahrenheit")
    print(f"Production Rate: {rate}")
    print(f"New Weight: {round(sensor.get_weight(), 2)} lbs")
    time.sleep(1)
    return new_temp

time_data, usage_data, weight_data, temp_data = [], [], [], []
start = time.time()

for _ in range(10):
    ice_bin = IceBinSensor()
    temp_sensor = TemperatureSensor()
    usage_sensor = UsagePatternSensor()
    usage = usage_sensor.get_usage()
    current_temp = temp_sensor.get_temperature()
    print("____________________________________________________")
    print(f"Current State:\nCurrent Weight: {round(ice_bin.get_weight(), 2)} lbs")
    print(f"Current Temperature: {current_temp} Fahrenheit")
    print(f"Current Usage: {usage} times")
    new_temp = adjust_sensors(usage, ice_bin)
    t = time.time() - start
    time_data.append(t)
    usage_data.append(usage)
    weight_data.append(ice_bin.get_weight())
    temp_data.append(new_temp)

print("Which graphs would you like to see?")
print("1. Usage vs Time\n2. Weight vs Time\n3. Temperature vs Time\n4. All of them")
user_input = input("Enter the numbers separated by commas (e.g., 1,2,3): ").strip().split(',')

def plot_graph(x, y, title, ylabel, color):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', color=color)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xlim(0, max(x) + 10)
    plt.ylim(min(y) - 1, max(y) + 1)
    plt.show()

if '1' in user_input: 
    plot_graph(time_data, usage_data, "Time vs Usage", "Usage", 'b')
if '2' in user_input: 
    plot_graph(time_data, weight_data, "Time vs Weight", "Weight (lbs)", 'g')
if '3' in user_input: 
    plot_graph(time_data, temp_data, "Time vs Temperature", "Temperature (°F)", 'r')
if '4' in user_input:
    plt.figure(figsize=(10, 5))
    plt.plot(time_data, usage_data, 'bo-', label='Usage')
    plt.plot(time_data, weight_data, 'go-', label='Weight')
    plt.plot(time_data, temp_data, 'ro-', label='Temperature')
    plt.title('Time vs Usage, Weight, and Temperature')
    plt.xlabel('Time (s)')
    plt.ylabel('Values')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, max(time_data) + 10)
    plt.ylim(min(min(usage_data), min(weight_data), min(temp_data)) - 1, max(max(usage_data), max(weight_data), max(temp_data)) + 1)
    plt.show()
