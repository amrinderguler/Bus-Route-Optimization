from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import folium
import os
import requests
from geopy.geocoders import Nominatim
from collections import defaultdict
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

# Constants
JECRC_LOCATION = (26.78218919094841, 75.82251239614644)  # JECRC College Lat/Lon
BUS_CAPACITY = 42
RESULTS_FOLDER = "results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

OSRM_URL = "http://router.project-osrm.org"

# Constants for fuel cost
DEFAULT_FUEL_COST_PER_KM = 5  # Adjust based on real value
DEFAULT_MILEAGE = 10  # Kilometers per liter

def haversine_distance(coord1, coord2):
    """Calculate the Haversine distance between two lat/lon coordinates."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km

    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lat2 - lon1)
    a = np.sin(dlat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

def get_route(start, end, timeout=10):
    """Get the route between start and end using OSRM."""
    try:
        coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
        response = requests.get(f"{OSRM_URL}/route/v1/driving/{coords}?overview=full&geometries=geojson", timeout=timeout)
        response.raise_for_status()
        routes = response.json()
        if routes and routes['routes']:
            route_coords = [(coord[1], coord[0]) for coord in routes['routes'][0]['geometry']['coordinates']]
            distance = routes['routes'][0]['distance'] / 1000  # Convert to km
            return route_coords, distance
        else:
            print(f"No route found from {start} to {end}. Using haversine distance.")
            route_coords = [start, end]
            distance = haversine_distance(start, end)
            return route_coords, distance
    except Exception as e:
        print(f"Error occurred while fetching route from OSRM: {e}")
        print(f"Using haversine distance as fallback for {start} to {end}.")
        route_coords = [start, end]
        distance = haversine_distance(start, end)
        return route_coords, distance

def calculate_fuel_cost(distance, fuel_cost_per_km=DEFAULT_FUEL_COST_PER_KM, mileage=DEFAULT_MILEAGE):
    """Calculate the fuel cost for a given distance."""
    fuel_needed = distance / mileage  # Calculate fuel consumption
    return fuel_needed * fuel_cost_per_km  # Calculate total cost

def create_routes_from_college_to_start(driver_locations):
    """Create routes starting from the college to the driver's starting location."""
    routes = {}
    for bus, driver_loc in driver_locations.items():
        # Validate driver location
        if not isinstance(driver_loc, tuple) or not len(driver_loc) == 2 or not isinstance(driver_loc[0], (float, int)) or not isinstance(driver_loc[1], (float, int)):
            print(f"Invalid driver location for bus {bus}: {driver_loc}")
            continue

        route_coords, distance = get_route(JECRC_LOCATION, driver_loc)
        routes[bus] = {'route_coords': route_coords, 'distance': distance}
    return routes

def assign_students_to_routes(students, routes, fuel_cost_per_km, mileage):
    """Assign students to the closest route considering bus capacity and fuel cost optimization."""
    bus_assignments = {bus: [] for bus in routes}
    updated_routes = {bus: routes[bus]['route_coords'] for bus in routes}
    total_cost = {bus: 0 for bus in routes}  # Store total cost for each bus route

    unassigned_students = students[:]  # Create a list of unassigned students

    # Assign students to buses in an optimized way
    while unassigned_students:
        student = unassigned_students.pop(0)
        name, lat, lon = student
        student_coords = (lat, lon)
        
        # Calculate the cost of assigning the student to each bus
        bus_costs = []
        for bus in routes:
            if len(bus_assignments[bus]) < BUS_CAPACITY:
                # Calculate additional cost for adding this student to the bus
                additional_distance = min(haversine_distance(student_coords, stop) for stop in updated_routes[bus])
                additional_fuel_cost = calculate_fuel_cost(additional_distance, fuel_cost_per_km, mileage)
                new_total_cost = total_cost[bus] + additional_fuel_cost
                bus_costs.append((bus, new_total_cost, additional_distance))

        # Sort buses based on the minimum cost and assign the student to the best bus
        bus_costs.sort(key=lambda x: x[1])  # Sort by the total cost (fuel cost)

        # Choose the bus with the least total cost (first bus in the sorted list)
        best_bus = bus_costs[0][0]
        bus_assignments[best_bus].append(student)

        # Update the route for the chosen bus
        updated_routes[best_bus].insert(min(range(len(updated_routes[best_bus])), key=lambda i: haversine_distance(student_coords, updated_routes[best_bus][i])) + 1, student_coords)
        total_cost[best_bus] = bus_costs[0][1]  # Update total cost for the bus

    return bus_assignments, updated_routes, total_cost

def create_map_and_image(bus, students, driver_location, route_coords):
    """Generate HTML map for each bus route."""
    route_map = folium.Map(location=JECRC_LOCATION, zoom_start=12)
    folium.Marker(JECRC_LOCATION, popup='JECRC College', icon=folium.Icon(color='red')).add_to(route_map)
    folium.Marker(driver_location, popup=f'Start {bus}', icon=folium.Icon(color='green')).add_to(route_map)

    # Track duplicate locations and apply small offsets
    location_counts = defaultdict(int)

    for student in students:
        name, lat, lon = student
        key = (lat, lon)  # Convert location to a hashable key
        location_counts[key] += 1

        # Apply a small offset if there are multiple students at the same location
        lat_offset = (location_counts[key] - 1) * 0.0001
        lon_offset = (location_counts[key] - 1) * 0.0001

        folium.Marker((lat + lat_offset, lon + lon_offset),
                      popup=f"{name}",
                      icon=folium.Icon(color='blue')).add_to(route_map)

    # Add polyline for the real road-based route
    for i in range(len(route_coords) - 1):
        segment_coords, _ = get_route(route_coords[i], route_coords[i + 1])
        folium.PolyLine(segment_coords, color='blue', weight=2.5, opacity=1).add_to(route_map)

    file_path_html = os.path.join(RESULTS_FOLDER, f"{bus}_route.html")
    route_map.save(file_path_html)
    print(f"Saved HTML map for {bus}")
    return file_path_html

def generate_student_allocation_csv(bus, students):
    """Generate CSV file for student allocation per bus."""
    # Create DataFrame for student allocation
    allocation_data = []
    for student in students:
        name, lat, lon = student
        allocation_data.append([name, lat, lon])

    df = pd.DataFrame(allocation_data, columns=["Name", "Latitude", "Longitude"])
    file_path_csv = os.path.join(RESULTS_FOLDER, f"{bus}_student_allocation.csv")
    df.to_csv(file_path_csv, index=False)
    print(f"Saved CSV for {bus}")
    return file_path_csv

def save_html_as_png(html_file, bus_index):
    """Convert the HTML file to a PNG image using Selenium."""
    png_path = os.path.join(RESULTS_FOLDER, f"Route{bus_index + 1}.png")

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1200x800")  # Set window size

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"file://{os.path.abspath(html_file)}")

    # Allow time for the page to load
    time.sleep(2)

    # Capture screenshot
    driver.save_screenshot(png_path)
    driver.quit()
    return png_path

@app.route("/api/optimize_routes", methods=["POST"])
def optimize_routes():
    """Main API route for optimizing bus routes."""
    bus_file = request.files.get("busFile")
    student_file = request.files.get("studentFile")

    if not bus_file or not student_file:
        return jsonify({"error": "Both bus and student files are required"}), 400

    bus_data = pd.read_csv(bus_file)
    student_data = pd.read_csv(student_file)

    buses = bus_data.to_dict(orient="records")
    students = student_data.to_dict(orient="records")
    
    driver_locations = {bus['Bus No']: (bus['Latitude'], bus['Longitude']) for bus in buses}
    students_data = [(student['Name'], student['Latitude'], student['Longitude']) for student in students]

    routes = create_routes_from_college_to_start(driver_locations)
    bus_assignments, updated_routes, total_cost = assign_students_to_routes(students_data, routes, DEFAULT_FUEL_COST_PER_KM, DEFAULT_MILEAGE)

    routes_output = {}
    for bus, students in bus_assignments.items():
        route_coords = updated_routes[bus]
        html_file = create_map_and_image(bus, students, driver_locations[bus], route_coords)
        csv_file = generate_student_allocation_csv(bus, students)
        png_file = save_html_as_png(html_file, bus)
        routes_output[bus] = {
            "route": route_coords,
            "csv_file": os.path.basename(csv_file),
            "html_file": os.path.basename(html_file),
            "png_file": os.path.basename(png_file),
        }

    return jsonify(routes_output)

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Endpoint to download a file."""
    file_path = os.path.join(RESULTS_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
