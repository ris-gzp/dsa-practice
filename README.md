# DSA Practice

Python workspace for Data Structures & Algorithms practice.

## Structure

```
dsa-practice/
├── arrays/        # Array problems
├── strings/       # String problems
├── trees/         # Binary trees, BST, tries
├── graphs/        # Graph traversal, shortest path, topology
└── dp/            # Dynamic programming
```

## Topics & Patterns

| Folder    | Key Patterns |
|-----------|-------------|
| `arrays`  | Two pointers, sliding window, prefix sum, Kadane's |
| `strings` | Sliding window, hashing, palindromes, anagrams |
| `trees`   | DFS, BFS, recursion, level-order traversal |
| `graphs`  | DFS, BFS, topological sort, union-find, Dijkstra |
| `dp`      | Memoization, tabulation, knapsack, LCS, LIS |

## Getting Started

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# Run any file directly
python arrays/problems.py
python dp/problems.py
```

## Workflow

Each folder has a `problems.py` with starter implementations.
Add new problems as separate functions in the same file, or create
new files per problem (e.g. `arrays/sliding_window.py`).

### Auto-commit daily solutions

`dsa_commit.py` auto-detects what you solved, extracts function names from the diff, and pushes with a descriptive commit message.

```bash
# After solving — commit + push everything
python dsa_commit.py

# With an optional note
python dsa_commit.py "LeetCode daily challenge"

# Preview the commit message without committing
python dsa_commit.py --dry-run
```

Example commit message generated:

```
solve: two_sum, max_subarray, is_palindrome [arrays, strings]

Date: 01 Jun 2026

Problems solved (3):
  - two_sum
  - max_subarray
  - is_palindrome

Topics: arrays, strings

Files:
  - arrays/problems.py
  - strings/problems.py
```
