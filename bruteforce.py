import json
import itertools
import timeit

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
        gain_percentage = int(action_data['gain']*100)
        action = Action(name, cost, gain_percentage)
        actions.append(action)

actions.sort(key=lambda action: action.gain_percentage, reverse=True)

best_combination = []
best_total_gain = 0
best_total_cost = 0
budget = 500

def find_best_combination():
    global best_combination, best_total_gain, best_total_cost

    for r in range(1, len(actions) + 1):
        for combination in itertools.combinations(actions, r):
            total_cost = sum(action.cost for action in combination)
            total_gain = sum(action.cost * (action.gain_percentage) for action in combination)

            if total_cost <= budget and total_gain > best_total_gain:
                best_combination = combination
                best_total_gain = total_gain
                best_total_cost = total_cost

# Measure the execution time
execution_time = timeit.timeit(find_best_combination, number=1)

# Calculate the average gain percentage
if best_combination:
    average_gain_percentage = sum(action.gain_percentage for action in best_combination) / len(best_combination)
else:
    average_gain_percentage = 0

print(f"Best Combination (Total Cost: {best_total_cost:.2f}):")
print(f"Average Gain Percentage in Best Combination: {average_gain_percentage:.2f}%")
for action in best_combination:
    print(f"Action: {action.name}, Cost: {action.cost}, Gain Percentage: {action.gain_percentage}%")

print(f"Execution Time: {execution_time:.6f} seconds")
