import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def collatz(n: int) -> list[int]:
    """
    Generates the Collatz sequence for a positive integer n using recursion.
    """
    if n == 1:
        return [1]

    if n % 2 == 0:
        next_n = n // 2
    else:
        next_n = 3 * n + 1
    return [n] + collatz(next_n)


def plot_collatz_stats(limit: int) -> Figure:
    """
    Generates a 2x2 grid of plots analyzing Collatz metrics for 1 to limit.
    """
    series_sums = []
    max_terms = []
    stopping_times = []
    for i in range(1, limit + 1):
        collatz_seq = collatz(i)
        series_sum = sum(collatz_seq)
        max_term = max(collatz_seq)
        stopping_time = len(collatz_seq) - 1
        series_sums.append(series_sum)
        max_terms.append(max_term)
        stopping_times.append(stopping_time)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    axes[0, 0].set_title("Series Sum")
    axes[0, 0].scatter(
        range(1, limit + 1), series_sums, alpha=0.7, s=1, c="tab:red")
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_xlabel("Starting Number (n)")
    axes[0, 0].set_ylabel("Sum (Log Scale)")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    axes[0, 1].set_title("Maximum Research Number (Peak)")
    axes[0, 1].scatter(
        range(1, limit + 1), max_terms, alpha=0.7, s=1, c="tab:green")
    axes[0, 1].set_xlabel("Starting number (n)")
    axes[0, 1].set_ylabel("Max Value (Log Scale)")
    axes[0, 1].set_yscale("log")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    axes[1, 0].set_title("Total Stopping Time")
    axes[1, 0].scatter(
        range(1, limit + 1), stopping_times, alpha=0.7, s=1, c="tab:blue"
    )
    axes[1, 0].set_xlabel("Starting Number (n)")
    axes[1, 0].set_ylabel("Steps tp reach 1")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    axes[1, 1].set_title("Distribution of Stopping Times")
    axes[1, 1].hist(
        stopping_times, bins=50,
        color="tab:purple", edgecolor="black", alpha=0.5
    )
    axes[1, 1].set_xlabel("Stopping Time (Steps)")
    axes[1, 1].set_ylabel("Frequency")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()
    
    return fig


# Sample client
if __name__ == "__main__":
    # Print some Collatz sequences and their statistics
    for n in [1, 9, 10]:
        s = collatz(n)
        print(f"n: {n}")
        print(f"Sequence: {s}")
        print(f"Sum: {sum(s)}, Max: {max(s)}, Stopping time: {len(s) - 1}")

    # Create some plots of the Collatz sequence analysis
    fig1 = plot_collatz_stats(limit=10000)
    fig1.savefig("collatz_stats1.png")
    fig2 = plot_collatz_stats(limit=30000)
    fig2.savefig("collatz_stats2.png")
