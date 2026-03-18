def esthetic(n: int) -> list[int] | str:
    def to_base(n, base):
        digit_li = []
        while n > 0:
            digit_li.append(n % base)
            n //= base
        return digit_li

    def check(digits):
        length = len(digits)
        for i in range(0, length - 1):
            if abs(digits[i] - digits[i + 1]) != 1:
                return False
        return True

    answer_list = []
    for i in range(2, 11):
        if check(to_base(n, i)) is True:
            answer_list.append(i)
        else:
            continue

    if answer_list:
        return answer_list
    else:
        return "non-esthetic"


if __name__ == "__main__":
    n = int(input("Enter num: "))
    print(esthetic(n))
