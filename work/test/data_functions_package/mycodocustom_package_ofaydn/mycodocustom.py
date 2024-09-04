
import os
import random

def extract_measurements(measurements, measurement_type, unit, measurements_dict):
    """This function gets specific data from measurements dictionary.

    Meanwhile it structures the data.
    """
    for index, details in measurements_dict.items():
        if details["measurement"] == measurement_type and details["unit"] == unit:
            key = details["unit"]
            return measurements.get(key)
    return None

def read_file_content(file_path):
    """Reads measurements from a given file path using (:) delimiters."""
    measurements_dict = {}
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")
        with open(file_path) as file:
            for line in file:
                key, value = line.strip().split(":")
                measurements_dict[key] = float(value)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    return measurements_dict


def write_file_content(file_path, data):
    """Write the dictionary data to the file."""
    with open(file_path, "w") as file:
        for key, value in data.items():
            file.write(f"{key}:{value}\n")

def generate_random_measurements():
    """Generate random measurements for C, F, and K."""
    return {
        "C": round(random.uniform(-100.0, 100.0), 2),
        "F": round(random.uniform(-148.0, 212.0), 2),
        "K": round(random.uniform(173.15, 373.15), 2),
        "dissolved_oxygen_mg_L": round(random.uniform(0.0, 14.6), 2)
    }            
