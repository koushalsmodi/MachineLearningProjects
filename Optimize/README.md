# 🏦 Bank Placement Optimization Using Hill Climbing

This project simulates a city grid where houses are randomly placed, and the goal is to optimally place a given number of banks such that the **total Manhattan distance** from each house to its nearest bank is minimized. It uses **Hill Climbing** and **Random Restart Hill Climbing** search algorithms to find locally (and potentially globally) optimal solutions.

## 🚀 Features

- Customizable grid size and number of banks.
- Random house placement on the grid.
- Hill Climbing algorithm to optimize bank locations.
- Random Restart Hill Climbing to escape local minima.
- Cost function based on the sum of shortest distances from houses to banks.
- Image output to visualize each state using `Pillow`.

## 🧠 Algorithms Used

- **Hill Climbing**: Iteratively moves to the best neighboring configuration until no improvement is found.
- **Random Restart Hill Climbing**: Runs hill climbing multiple times with different random initializations to improve the chance of finding the global optimum.

## 🖼️ Output Visualization

Each state of the grid is visualized using `Pillow`, showing:
- Houses 🏠 (from `assets/images/House.png`)
- Banks 🏦 (from `assets/images/Bank.png`)
- Cost displayed at the bottom of the image

Example output filenames:
