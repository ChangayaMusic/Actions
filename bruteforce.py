import json
import itertools


class Action:
    def __init__(self, name, cost, gain_percentage):
        self.name = name
        self.cost = cost
        self.gain_percentage = gain_percentage


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


actions.sort(key=lambda action: action.gain_percentage, reverse=True)


best_combination = []
best_total_gain = 0
best_total_cost = 0


budget = 500


for r in range(1, len(actions) + 1):
    for combination in itertools.combinations(actions, r):
        total_cost = sum(action.cost for action in combination)
        total_gain = sum(action.cost * (action.gain_percentage / 100) for action in combination)

        if total_cost <= budget and total_gain > best_total_gain:
            best_combination = combination
            best_total_gain = total_gain
            best_total_cost = total_cost


print(f"Best Combination (Total Gain: {best_total_gain:.2f}, Total Cost: {best_total_cost:.2f}):")
for action in best_combination:
    print(f"Action: {action.name}, Cost: {action.cost}, Gain Percentage: {action.gain_percentage}%")
