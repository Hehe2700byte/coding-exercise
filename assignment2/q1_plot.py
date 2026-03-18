import matplotlib.pyplot as plt
from q1 import *
from statistics import mean


def scatterplot1(data: dict[str, list]) -> None:
    colors = plt.get_cmap('tab20')
    plt.figure(figsize=(10, 6))
    for i, (district, carparks) in enumerate(data.items()):
        lats = [carpark.latitude for carpark in carparks]
        longs = [carpark.longitude for carpark in carparks]
        plt.scatter(lats, longs, label=district, color=colors(i), s=30)
        plt.scatter(mean(lats), mean(longs), color="black", alpha=0.75, s=100,
                    marker='X')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Car Park Locations by District in Hong Kong')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()


def scatterplot2(points: list[Point], centroids: list[Point],
                 labels: list[int]) -> None:
    colors = plt.get_cmap('tab20')
    plt.figure(figsize=(8, 6))
    plt.scatter([p[0] for p in points], [p[1] for p in points],
                c=labels, s=30, cmap=colors)
    plt.scatter([p[0] for p in centroids], [p[1] for p in centroids],
                c='black', s=100, alpha=0.75, marker='X')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('K-means Clustering Results of Car Park Locations')
    plt.grid(True)
    plt.tight_layout()


if __name__ == "__main__":
    # Retrieve the raw data about car parks
    json_data = get_json_data()

    # Group the data and plot the points in each district
    grouped_data = group_by_district(json_data)
    scatterplot1(grouped_data)

    # Prepare the data points for clustering
    data_points = []
    for carpark in json_data:
        cp = Carpark(carpark)
        data_points.append((cp.latitude, cp.longitude))

    # Run the k-means clustering algorithm
    random.seed(42)  # Fix the seed for deterministic result
    kmeans = KMeans(n_clusters=18)
    kmeans.fit(data_points)

    # Plot the clustering result
    labels = kmeans.predict(data_points)
    scatterplot2(data_points, kmeans.centroids, labels)

    plt.show()
