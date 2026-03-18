from math import exp, log

type Vector = list[float | int]


def sigmoid(z: float) -> float:
    """Computes the sigmoid or logistic function."""
    return 1 / (1 + exp(-z))


def binary_cross_entropy(Y: Vector, Y_pred: Vector) -> float:
    sum = 0
    m = len(Y)
    for i in range(m):
        sum += Y[i] * log(Y_pred[i]) + (1 - Y[i]) * log(1 - Y_pred[i])
    return -sum / m


def fit(
    X: list[Vector], Y: Vector, epochs: int,
    learning_rate: float, tolerance: float
) -> tuple[Vector, float]:
    n = len(X[0])
    m = len(Y)
    W: Vector = [0.0] * n
    b = 0.0
    cost = 0.0
    for epoch in range(1, epochs + 1):
        Z = []
        for i in range(m):
            temp = zip(W, X[i])
            Z.append(sum([wj * xj for wj, xj in temp]) + b)
        Y_pred = [sigmoid(z) for z in Z]
        cost = binary_cross_entropy(Y, Y_pred)
        if cost < tolerance:
            break
        pw = []
        pb = 0
        errors = [y_pred - y for y_pred, y in zip(Y_pred, Y)]
        for i in range(n):
            total_error = sum([errors[j] * X[j][i] for j in range(m)])
            pw.append(total_error / m)
        for i in range(n):
            W[i] -= learning_rate * pw[i]
        pb = sum(errors) / m
        b -= learning_rate * pb

    print(f"Training stopped at epoch {epoch}, Cost: {cost:.5f}")
    return W, b


def predict(X: list[Vector], W: Vector, b: float) -> Vector:
    m = len(X)
    n = len(X[0])
    labels = []
    for i in range(m):
        z = 0
        for j in range(n):
            z += W[j] * X[i][j]
        z += b
        sigma = sigmoid(z)
        if sigma >= 0.5:
            labels.append(1)
        else:
            labels.append(0)

    return list(labels)


# Sample client
if __name__ == "__main__":
    # Example dataset
    X = [[1, 2], [2, 3], [3, 3], [5, 6], [8, 9], [1, 1]]
    Y = [0, 0, 0, 1, 1, 0]  # Corresponding labels

    # Create a logistic regression model
    W, b = fit(X, Y, learning_rate=0.05, epochs=5000, tolerance=0.05)

    # Predictions
    predictions = predict(X, W, b)

    print("Weights: [" + ", ".join(f"{w:.5f}" for w in W) + "]")
    print(f"Bias: {b:.5f}")
    print("Predictions:", predictions)

    # Another example dataset
    X = [[1, 2, 1], [8, 7, 9], [5, 1, 2], [2, 4, 3], [9, 9, 7], [1, 1, 0]]
    Y = [0, 1, 0, 0, 1, 0]  # Corresponding labels

    # Create another logistic regression model
    W, b = fit(X, Y, learning_rate=0.05, epochs=3000, tolerance=0.03)

    # Predictions
    predictions = predict(X, W, b)

    print("Weights: [" + ", ".join(f"{w:.5f}" for w in W) + "]")
    print(f"Bias: {b:.5f}")
    print("Predictions:", predictions)
