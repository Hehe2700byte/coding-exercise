import json
import math
import random
import requests
from typing import Any
# Optional TODO: Add more standard Python modules if needed (remove this line)
...

# Type alias
Point = list[float]  # [latitude, longtitude]

# Data source URL
URL = "https://resource.data.one.gov.hk/td/carpark/basic_info_all.json"


def get_json_data(no_cache: bool = False) -> list[dict[str, Any]]:
    """
    Load the data about car parks from the locally cached JSON file.
    If cache is not used or the cached file is not found, download the data in
    JSON format from the web.
    """
    if not no_cache:
        try:
            with open("carparks.json", "r") as f:
                parks_info = json.load(f)
            print("Retrieving data from cached file ...")
            return parks_info["car_park"]
        except FileNotFoundError:
            pass
    print("Retrieving data from the web ...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        json_string = response.content.decode("utf-8-sig")
        parks_info = json.loads(json_string)
        with open("carparks.json", "w", encoding = "utf-8") as f:
            json.dump(parks_info, f, indent = 4, ensure_ascii = False)
        return parks_info["car_park"]
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ambiguous error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")


class Carpark:
    """A class that represents a car park."""
    def __init__(self, data: dict):
        self.park_id = data["park_id"]
        self.name = data["name_en"]
        self.district = data["district_en"]
        self.latitude = data["latitude"]
        self.longtitude = data["longtitude"]
    
    def __repr__(self):
        return str(self.park_id)
    
    def __str__(self):
        return f"{self.name} ({self.park_id})"


def group_by_district(
    json_data: list[dict[str, Any]]
) -> dict[str, list[Carpark]]:
    """Create and group the car park objects by district."""
    result = {}
    for item in json_data:
        car_park = Carpark(item)
        if car_park.district not in result.keys():
            result[car_park.district] = []
        result[car_park.district].append(car_park)
    
    return result


def print_summary(data: dict[str, list[Carpark]]) -> None:
    """Print a summary table showing car park statistics."""
    print(f"{"District":21}{"Midpoint of car parks":26}{"# Car parks":11}")
    midlas = {dist: sum([car_park.latitude for car_park in data[dist]])/len(data[dist]) for dist in str}
    midlongs = {dist: sum([car_park.longtitude for car_park in data[dist]]/len(data[dist])) for dist in str}
    for midla, midlong, dist in midlas, midlongs, data.keys():
        print(f"{dist:21}({midla:>9.5}, {midlong:>9.5})    {len(data[dist]):11}")


class KMeans:
    """A class that implements the k-means clustering algorithm."""
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-5):
        # TODO: Add your code for part (e) and remove this line
        ...

    def fit(self, data: list[Point]) -> None:
        # TODO: Add your code for part (e) and remove this line
        ...

    def _closest_centroid(self, point: Point) -> int:
        # TODO: Add your code for part (e) and remove this line
        ...

    def _euclidean_distance(self, point1: Point, point2: Point) -> float:
        # TODO: Add your code for part (e) and remove this line
        ...

    def _mean(self, cluster: list[Point]) -> Point:
        # TODO: Add your code for part (e) and remove this line
        ...

    def _has_converged(self, old_centroids: list[Point],
                       new_centroids: list[Point]) -> bool:
        # TODO: Add your code for part (e) and remove this line
        ...

    def predict(self, data: list[Point]) -> list[int]:
        # TODO: Add your code for part (e) and remove this line
        ...


if __name__ == "__main__":
    # Retrieve the raw data about car parks
    json_data = get_json_data()

    # Group the data and print a summary
    grouped_data = group_by_district(json_data)
    print_summary(grouped_data)

    # Print some example car parks
    print("Example Car Parks:\n" + "-" * 18)
    for district in ['Eastern', 'Islands', 'Sha Tin']:
        print(f"First 5 car parks in {district}:", grouped_data[district][:5])
        for i, carpark in enumerate(grouped_data[district][:5]):
            print(i + 1, carpark)

    # Prepare the data points for clustering
    data_points = []
    for carpark in json_data:
        cp = Carpark(carpark)
        data_points.append([cp.latitude, cp.longitude])

    # Run the k-means clustering algorithm
    random.seed(42)  # Fix the seed for deterministic result
    kmeans = KMeans(n_clusters=18)
    kmeans.fit(data_points)

    # Print the clustering result
    print("Clustering Result:\n" + "-" * 18)
    print("Label     Centroid")
    for i, (latitude, longitude) in enumerate(sorted(kmeans.centroids)):
        print(f"{i:<10d}({latitude:9.5f}, {longitude:9.5f})")

    labels = kmeans.predict(data_points[:10])
    print("Predicted clusters:", labels)  # Print labels for the 1st 10 points
