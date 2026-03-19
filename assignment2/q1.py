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
        self.longitude = data["longitude"]
    
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
    midlas = [sum([car_park.latitude for car_park in data[dist]])/len(data[dist]) for dist in data.keys()]
    midlongs = [sum([car_park.longitude for car_park in data[dist]])/len(data[dist]) for dist in data.keys()]
    for midla, midlong, dist in zip(midlas, midlongs, data.keys()):
        print(f"{dist:21}({midla:>9.5f}, {midlong:>9.5f})    {len(data[dist]):11}")


class KMeans:
    """A class that implements the k-means clustering algorithm."""
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-5):
        # TODO: Add your code for part (e) and remove this line
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = []

    def fit(self, data: list[Point]) -> None:
        # TODO: Add your code for part (e) and remove this line
        self.centroids = random.sample(data, self.n_clusters)
        for i in range(self.max_iter):
            clusters = [[] for _ in range(self.n_clusters)]
            new_centroids = []
            for point in data:
                clusters[self._closest_centroid(point)].append(point)
            for j in range(self.n_clusters):
                new_centroids.append(self._mean(clusters[j]))
            if self._has_converged(self.centroids, new_centroids):
                self.centroids = new_centroids
                break
            else:
                self.centroids = new_centroids

            
    def _closest_centroid(self, point: Point) -> int:
        distances = [self._euclidean_distance(point, centriod) for centriod in self.centroids]
        return distances.index(min(distances))

    def _euclidean_distance(self, point1: Point, point2: Point) -> float:
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def _mean(self, cluster: list[Point]) -> Point:
        if len(cluster) == 0:
            return [0.0, 0.0]
        else:
            mean_x = sum([point[0] for point in cluster])/len(cluster)
            mean_y = sum([point[1] for point in cluster])/len(cluster)
            return [mean_x, mean_y]
        

    def _has_converged(self, old_centroids: list[Point],
                       new_centroids: list[Point]) -> bool:
        for i in range(len(old_centroids)):
            if self._euclidean_distance(old_centroids[i], new_centroids[i]) >= self.tol:
                return False
        return True

    def predict(self, data: list[Point]) -> list[int]:
        return [self._closest_centroid(point) for point in data]


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
