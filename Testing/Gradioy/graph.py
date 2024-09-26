import json
import numpy as np
import matplotlib.pyplot as plt

# Load JSON data (replace with actual file loading logic)
file_path = r'Testing\Gradioy\response.json'
with open(file_path, 'r') as file:
    data = json.load(file)['data']

def get_average_per_day(values, points_per_day=24):
    """
    Get average daily values for a list of values.
    We assume each day has `points_per_day` data points.
    """
    averages = []
    for i in range(0, len(values), points_per_day):
        day_values = values[i:i + points_per_day]
        avg = np.mean(day_values)
        averages.append(avg)
    return averages

def plot_data_per_device(data):
    # Measurement types to be plotted
    measurement_types = ['freq', 'phAngle', 'power', 'reacPower', 'rmsCur', 'rmsVolt']
    devices = list(data.keys())  # Get device names
    
    # Create subplots
    fig, axs = plt.subplots(len(devices), len(measurement_types), figsize=(25, 4 * len(devices)))
    
    # Loop through devices and measurements
    for device_index, device in enumerate(devices):
        for measure_index, measure in enumerate(measurement_types):
            if measure in data[device]:
                # Calculate average per day for this measurement
                avg_data = get_average_per_day(data[device][measure])
                
                # Plot data
                axs[device_index, measure_index].plot(avg_data)
                axs[device_index, measure_index].set_title(f'{device} - {measure}')
                axs[device_index, measure_index].set_xlabel('Time (hours)')
                axs[device_index, measure_index].set_ylabel(measure.capitalize())
                axs[device_index, measure_index].grid(True)
            else:
                # If the device doesn't have this measurement, leave the plot blank
                axs[device_index, measure_index].axis('off')

    plt.tight_layout()
    plt.show()

# Call the plotting function
plot_data_per_device(data)
