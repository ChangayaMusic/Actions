import json


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
                    dp[i - 1][w - actions[i - 1].cost] + actions[i - 1].cost * actions[i - 1].gain_percentage / 100
                )

    selected_actions = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_actions.append(actions[i - 1])
            w -= actions[i - 1].cost

    return selected_actions, dp[n][budget]


# Load JSON data from a file into a list of Action objects
actions = []

with open('data.json', 'r', encoding='utf-8') as json_file:
    data_dict = json.load(json_file)
    for action_data in data_dict['actions']:
        name = action_data['name']
        cost = action_data['cost']
        gain_percentage = action_data['gain']
        action = Action(name, cost, gain_percentage)
        actions.append(action)

budget = 500

selected_actions, best_total_gain = knapsack(actions, budget)
total_cost = sum(action.cost for action in selected_actions)

print(f"Best Combination (Total Gain: {best_total_gain:.2f}, Total Cost: {total_cost:.2f}):")
for action in selected_actions:
    print(f"Action: {action.name}, Cost: {action.cost}, Gain Percentage: {action.gain_percentage}%")
