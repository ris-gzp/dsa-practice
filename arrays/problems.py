# Arrays — common patterns: two pointers, sliding window, prefix sum, kadane's


def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
