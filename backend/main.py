from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import requests
from collections import defaultdict
import time

app = Flask(__name__)
CORS(app)

# Constants
JECRC_LOCATION = (26.78218919094841, 75.82251239614644)  # JECRC College Lat/Lon
BUS_CAPACITY = 42
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
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
    dlon = np.radians(lon2 - lon1)
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
    total_distance = {bus: routes[bus]['distance'] for bus in routes}  # Store total distance for each bus route

    unassigned_students = students[:]  # Create a list of unassigned students

    # Assign students to buses in an optimized way
    while unassigned_students:
        student = unassigned_students.pop(0)
        # Extract student data (now including pickup point)
        name, lat, lon, pickup_point = student
        student_coords = (lat, lon)
        
        # Calculate the cost of assigning the student to each bus
        bus_costs = []
        for bus in routes:
            if len(bus_assignments[bus]) < BUS_CAPACITY:
                # Calculate additional cost for adding this student to the bus
                additional_distance = min(haversine_distance(student_coords, stop) for stop in updated_routes[bus])
                additional_fuel_cost = calculate_fuel_cost(additional_distance, fuel_cost_per_km, mileage)
                new_total_cost = total_cost[bus] + additional_fuel_cost
                new_total_distance = total_distance[bus] + additional_distance
                bus_costs.append((bus, new_total_cost, new_total_distance))

        # Sort buses based on the minimum cost and assign the student to the best bus
        bus_costs.sort(key=lambda x: x[1])  # Sort by the total cost (fuel cost)

        # Choose the bus with the least total cost (first bus in the sorted list)
        if bus_costs:
            best_bus = bus_costs[0][0]
            bus_assignments[best_bus].append(student)

            # Update the route for the chosen bus
            updated_routes[best_bus].insert(min(range(len(updated_routes[best_bus])), key=lambda i: haversine_distance(student_coords, updated_routes[best_bus][i])) + 1, student_coords)
            total_cost[best_bus] = bus_costs[0][1]  # Update total cost for the bus
            total_distance[best_bus] = bus_costs[0][2]  # Update total distance for the bus
        else:
            print(f"Could not assign student {name}, all buses are at capacity")

    return bus_assignments, updated_routes, total_cost, total_distance

def generate_student_allocation_csv(bus, students):
    """Generate CSV file for student allocation per bus with pickup points."""
    # Create DataFrame for student allocation
    allocation_data = []
    for student in students:
        name, lat, lon, pickup_point = student  # Now includes pickup point
        allocation_data.append([name, lat, lon, pickup_point])

    df = pd.DataFrame(allocation_data, columns=["Name", "Latitude", "Longitude", "Pickup Point"])
    file_path_csv = os.path.join(RESULTS_FOLDER, f"{bus}_student_allocation.csv")
    df.to_csv(file_path_csv, index=False)
    print(f"Saved CSV for {bus}")
    return file_path_csv

def generate_bus_summary_csv(bus_distances, bus_costs):
    """Generate a summary CSV with distance and cost information for all buses."""
    summary_data = []
    for bus_no in bus_distances:
        summary_data.append({
            "Bus No": bus_no,
            "Total Distance (km)": round(bus_distances[bus_no], 2),
            "Fuel Cost (Rs)": round(bus_costs[bus_no], 2)
        })
    
    df = pd.DataFrame(summary_data)
    summary_csv_path = os.path.join(RESULTS_FOLDER, "bus_summary.csv")
    df.to_csv(summary_csv_path, index=False)
    print(f"Saved bus summary CSV file")
    return summary_csv_path

@app.route("/api/optimize_routes", methods=["POST"])
def optimize_routes():
    """Main API route for optimizing bus routes."""
    bus_file = request.files.get("busFile")
    student_file = request.files.get("studentFile")

    if not bus_file or not student_file:
        return jsonify({"error": "Both bus and student files are required"}), 400

    try:
        # Parse input files
        bus_data = pd.read_csv(bus_file)
        student_data = pd.read_csv(student_file)
        
        # Check if required columns exist in student data
        required_columns = ["Name", "Latitude", "Longitude"]
        if not all(col in student_data.columns for col in required_columns):
            return jsonify({"error": "Student data must contain Name, Latitude, and Longitude columns"}), 400
            
        # Check if Pickup Point column exists, otherwise create it from location
        if "Pickup Point" not in student_data.columns:
            return jsonify({"error": "Student data must contain a 'Pickup Point' column"}), 400
        
        # Ensure numeric data types for coordinates
        student_data["Latitude"] = pd.to_numeric(student_data["Latitude"], errors="coerce")
        student_data["Longitude"] = pd.to_numeric(student_data["Longitude"], errors="coerce")
        
        # Check if required columns exist in bus data
        required_bus_columns = ["Bus No", "Latitude", "Longitude"]
        if not all(col in bus_data.columns for col in required_bus_columns):
            return jsonify({"error": "Bus data must contain Bus No, Latitude, and Longitude columns"}), 400
        
        # Ensure numeric data types for bus coordinates and mileage
        bus_data["Latitude"] = pd.to_numeric(bus_data["Latitude"], errors="coerce")
        bus_data["Longitude"] = pd.to_numeric(bus_data["Longitude"], errors="coerce")
        
        # Set default mileage if not present or convert to numeric if present
        if "Mileage" in bus_data.columns:
            bus_data["Mileage"] = pd.to_numeric(bus_data["Mileage"], errors="coerce")
            # Replace NaN values with default mileage
            bus_data["Mileage"].fillna(DEFAULT_MILEAGE, inplace=True)
        else:
            bus_data["Mileage"] = DEFAULT_MILEAGE
            
        # Fixed fuel price (Rs/liter)
        fuel_cost = 100

        # Prepare data for optimization
        driver_locations = {str(bus['Bus No']): (float(bus['Latitude']), float(bus['Longitude'])) 
                          for _, bus in bus_data.iterrows() 
                          if pd.notna(bus['Latitude']) and pd.notna(bus['Longitude'])}
        
        # Filter out students with invalid coordinates
        valid_students = student_data.dropna(subset=["Latitude", "Longitude"])
        
        students_data = [(
            str(student['Name']), 
            float(student['Latitude']), 
            float(student['Longitude']),
            str(student['Pickup Point'])  # Use the pickup point directly from the CSV
        ) for _, student in valid_students.iterrows()]

        # Create initial routes from college to bus starting points
        routes = create_routes_from_college_to_start(driver_locations)
        
        # Skip optimization if no valid routes
        if not routes:
            return jsonify({"error": "No valid bus routes could be created"}), 400
            
        # Use mean mileage as default for all routes
        default_mileage = float(bus_data["Mileage"].mean())
        
        # Assign students to routes optimally
        bus_assignments, updated_routes, total_cost, total_distance = assign_students_to_routes(
            students_data, 
            routes, 
            fuel_cost,
            default_mileage
        )

        # Generate output files and response data
        routes_output = {}
        bus_costs = {}
        
        for index, bus_row in bus_data.iterrows():
            bus_no = str(bus_row['Bus No'])  # Convert to string for consistency
            # Use bus-specific mileage if available
            mileage = float(bus_row['Mileage'])
            
            if bus_no in bus_assignments:
                # Generate student allocation CSV
                csv_file = generate_student_allocation_csv(bus_no, bus_assignments[bus_no])
                
                # Calculate cost based on bus-specific mileage
                fuel_cost_value = calculate_fuel_cost(total_distance[bus_no], fuel_cost, mileage)
                bus_costs[bus_no] = fuel_cost_value
                
                # Add to output
                routes_output[bus_no] = {
                    "csv_file": os.path.basename(csv_file),
                    "students_assigned": len(bus_assignments[bus_no]),
                    "distance": round(total_distance[bus_no], 2),
                    "fuel_cost": round(fuel_cost_value, 2)
                }

        # Generate summary CSV
        summary_csv = generate_bus_summary_csv(total_distance, bus_costs)
        
        # Add summary CSV to output
        routes_output["summary"] = {
            "csv_file": os.path.basename(summary_csv)
        }

        return jsonify(routes_output)
        
    except Exception as e:
        import traceback
        print(f"Error in route optimization: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": f"Route optimization failed: {str(e)}"}), 500

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