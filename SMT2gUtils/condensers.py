def product(numbers: list[int], limit=None):
    if limit is None:
        # If no limit is provided, multiply all values together
        result = 1
        for num in numbers:
            result *= num
        return [result]

    result = []

    for i in range(0, len(numbers), limit):
        group = numbers[i:i + limit]
        group_product = 1

        for num in group:
            group_product *= num

        result.append(group_product)

    return result