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
# Define a function to perform knapsack for dataset 1 and measure time
def knapsack_dataset1():
    actions1 = read_actions_from_csv('dataset1.csv')
    selected_actions1, best_total_gain1 = knapsack(actions1, budget)
    total_cost1 = sum(action.cost for action in selected_actions1)
    print("Results for dataset1.csv:")
    print(f"Best Combination (Total Gain: {best_total_gain1:.2f}, Total Cost: {total_cost1:.2f}):")
    for action in selected_actions1:
        print(f"Action: {action.name}, Cost: {action.cost}, Gain Percentage: {action.gain_percentage}%")

time_dataset1 = timeit.timeit(knapsack_dataset1, number=1)
print(f"Time taken for dataset1: {time_dataset1:.6f} seconds")

# Define a function to perform knapsack for dataset 2 and measure time
def knapsack_dataset2():
    actions2 = read_actions_from_csv('dataset2.csv')
    selected_actions2, best_total_gain2 = knapsack(actions2, budget)
    total_cost2 = sum(action.cost for action in selected_actions2)
    print("\nResults for dataset2.csv:")
    print(f"Best Combination (Total Gain: {best_total_gain2:.2f}, Total Cost: {total_cost2:.2f}):")
    for action in selected_actions2:
        print(f"Action: {action.name}, Cost: {action.cost}, Gain Percentage: {action.gain_percentage}%")

time_dataset2 = timeit.timeit(knapsack_dataset2, number=1)
print(f"Time taken for dataset2: {time_dataset2:.6f} seconds")