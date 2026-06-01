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
