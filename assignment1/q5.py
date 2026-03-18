import random

type Vector = list[float | int]


def manhattan_distance(point1: Vector, point2: Vector) -> float | int:
    distance = 0
    for v1, v2 in zip(point1, point2):
        distance += abs(v1 - v2)

    return distance


def assign_clusters(data: list[Vector],
                    medoids: list[Vector]) -> list[list[Vector]]:
    clusters = [[] for _ in range(len(medoids))]
    for point in data:
        distances = [manhattan_distance(point, medoids[i])
                     for i in range(len(medoids))]
        clusters[distances.index(min(distances))].append(point)

    return clusters


def update_medoids(clusters: list[list[Vector]]) -> list[Vector]:
    new_medoids = []
    for cluster in clusters:
        total_distance = [
            sum(
                [
                    manhattan_distance(cluster[i], cluster[j])
                    for j in range(len(cluster))
                ]
            )
            for i in range(len(cluster))
        ]
        new_medoids.append(cluster[total_distance.index(min(total_distance))])

    return new_medoids


def k_medoids(
    data: list[Vector], k: int = 3, max_iterations: int = 100, seed: int = 42
) -> tuple[list[Vector], list[list[Vector]]]:
    assert k > 0 and max_iterations > 0

    random.seed(seed)
    medoids = random.sample(data, k)
    clusters = [[] for _ in range(len(medoids))]
    for i in range(max_iterations):
        last_clusters = clusters
        last_medoids = medoids
        clusters = assign_clusters(data, medoids)
        medoids = update_medoids(clusters)
        if medoids == last_medoids:
            break

    return medoids, clusters


# Sample client
if __name__ == "__main__":
    # Sample data 1
    data = [
        (1, 2),
        (1, 4),  # Cluster 1
        (10, 2),
        (10, 4),  # Cluster 2
        (2, 3),
        (3, 4),  # Cluster 1
        (12, 3),
        (11, 2),  # Cluster 2
        (5, 8),
        (6, 9),
        (7, 7),
        (6, 8),  # Cluster 3
        (90, 50),
        (68, 47),  # Cluster 4 (Outliners)
    ]
    medoids, clusters = k_medoids(data, k=4, seed=99)
    print("Final Medoids:", medoids)
    for index, cluster in enumerate(clusters):
        print(f"Cluster {index + 1}: {cluster}")

    # Sample data 2
    data = [
        [1.0, 2.0, 3.0],  # Cluster 1
        [1.5, 1.8, 2.5],  # Cluster 1
        [5.5, 6.5, 7.0],  # Cluster 2
        [1.0, 0.5, 1.5],  # Cluster 1
        [6.0, 7.0, 6.5],  # Cluster 2
        [99.9, 89.0, 79.5],  # Cluster 3 (Outliner)
        [4.5, 5.0, 5.5],  # Cluster 2
        [1.8, 2.2, 2.0],  # Cluster 1
    ]
    medoids, clusters = k_medoids(data, k=3, seed=13)
    print("Final Medoids:", medoids)
    for index, cluster in enumerate(clusters):
        print(f"Cluster {index + 1}: {cluster}")
