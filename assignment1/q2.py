def pascal_triangle(n: int) -> None:
    nums = [[0 for _ in range(n + 2)] for _ in range(n + 2)]
    for i in range(1, n + 2):
        nums[i][1] = nums[i][i] = 1
        if i > 2:
            for j in range(2, i):
                nums[i][j] = nums[i - 1][j - 1] + nums[i - 1][j]
    wid = len(str(nums[n + 1][n // 2 + 1]))
    if wid % 2 == 0:
        wid += 1
    for i in range(1, n + 2):
        leading_space = (n - i + 1) * (wid + 1) // 2
        print(" " * leading_space, end="")
        for j in range(1, i + 1):
            print(f"{nums[i][j]:^{wid}}", end="")
            if j < i:
                print(" ", end="")
        print("")


if __name__ == "__main__":
    n = int(input("Enter nums: "))
    pascal_triangle(n)
