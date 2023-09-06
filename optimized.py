import csv
import timeit


class Action:
    def __init__(self, name, cost, gain_percentage):
        self.name = name
        self.cost = cost
        self.gain_percentage = gain_percentage


def knapsack(actions, budget):
    n = len(actions)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(budget + 1):
            if actions[i - 1].cost > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][int(w - actions[i - 1].cost)] + actions[i - 1].cost * actions[i - 1].gain_percentage / 100
                )

    selected_actions = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][int(w)] != dp[i - 1][int(w)]:
            selected_actions.append(actions[i - 1])
            w -= actions[i - 1].cost

    total_cost = sum(action.cost for action in selected_actions)
    if total_cost > budget:
        # If total cost exceeds the budget, remove actions until it fits
        while total_cost > budget:
            removed_action = selected_actions.pop()
            total_cost -= removed_action.cost

    return selected_actions, dp[n][budget]


def read_actions_from_csv(csv_filename):
    actions = []
    with open(csv_filename, 'r', encoding='utf-8', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if it exists

        for row in csv_reader:
            name = row[0]
            price = float(row[1])
            profit = float(row[2])

            if price > 0:
                action = Action(name, price, profit)
                actions.append(action)
    return actions


budget = 500


def calculate_knapsack(actions, budget):
    selected_actions, best_total_gain = knapsack(actions, budget)
    total_cost = sum(action.cost for action in selected_actions)
    if total_cost > budget:
        # If total cost exceeds the budget, remove actions until it fits
        while total_cost > budget:
            removed_action = selected_actions.pop()
            total_cost -= removed_action.cost

    return selected_actions, best_total_gain


# Define a function to calculate average gain percentage
def calculate_average_gain_percentage(selected_actions):
    if not selected_actions:
        return 0
    total_percentage = sum(action.gain_percentage for action in selected_actions)
    return total_percentage / len(selected_actions)


# Define a function to perform knapsack for a dataset and print results
def knapsack_and_print(dataset_name, csv_filename):
    actions = read_actions_from_csv(csv_filename)
    selected_actions, best_total_gain = calculate_knapsack(actions, budget)
    total_cost = sum(action.cost for action in selected_actions)
    avg_gain_percentage = calculate_average_gain_percentage(selected_actions)

    print(f"Results for {dataset_name}:")
    print(f"Best Combination (Total Gain: {best_total_gain:.2f}, Total Cost: {total_cost:.2f}):")
    print(f"Average Gain Percentage: {avg_gain_percentage:.2f}%")
    for action in selected_actions:
        print(f"Action: {action.name}, Cost: {action.cost}, Gain Percentage: {action.gain_percentage}%")


# Measure and print the execution time for dataset1
time_dataset1 = timeit.timeit(lambda: knapsack_and_print("dataset1.csv", "dataset1.csv"), number=1)
print(f"Time taken for dataset1: {time_dataset1:.6f} seconds")

# Measure and print the execution time for dataset2
time_dataset2 = timeit.timeit(lambda: knapsack_and_print("dataset2.csv", "dataset2.csv"), number=1)
print(f"Time taken for dataset2: {time_dataset2:.6f} seconds")
