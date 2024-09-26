import matplotlib.pyplot as plt
import json

# Load the JSON data
with open(r'Testing\Gradioy\response.json', 'r') as file:
    data = json.load(file)

# Get the number of appliances
appliances = list(data['data'].keys())
num_appliances = len(appliances)

# Define the parameters to plot
parameters = ['freq', 'phAngle', 'power', 'reacPower', 'rmsCur', 'rmsVolt']
param_names = ['Frequency', 'Phase Angle', 'Power', 'Reactive Power', 'RMS Current', 'RMS Voltage']
units = ['Hz', 'degrees', 'W', 'VAR', 'A', 'V']

# Create a figure with subplots for each appliance and parameter
fig, axs = plt.subplots(num_appliances, len(parameters), figsize=(20, 5*num_appliances))
fig.suptitle('Electrical Parameters for Various Appliances', fontsize=16)

# Plot data for each appliance and parameter
for i, appliance in enumerate(appliances):
    for j, (param, name, unit) in enumerate(zip(parameters, param_names, units)):
        ax = axs[i, j] if num_appliances > 1 else axs[j]
        values = data['data'][appliance][param]
        time = range(len(values))
        
        ax.bar(time, values)  # Change plot type to bar plot
        ax.set_title(f'{appliance}: {name}')
        ax.set_xlabel('Time')
        ax.set_ylabel(f'{name} ({unit})')
        ax.grid(True)

# Adjust layout and display the plot
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()