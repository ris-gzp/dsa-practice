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


def max_subarray(nums: list[int]) -> int:
    max_sum = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        max_sum = max(max_sum, cur)
    return max_sum
