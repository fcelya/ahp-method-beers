import ahpy

# Welcome
print("\n\n########## WELCOME TO THE AHP METHOD BEER COMPARATOR ##########")
print(
    "Here we will implement the AHP method to aid in multi-variable multi-criteria decisions. The problem chosen at hand is that of which beer brand to buy. This problem has been chosen given its usefullness in day to day life and the easiness to find willing subjects to give input on the different wheightings between criteria and beer brands."
)
print(
    "The implementation will be done with the use of the package AHPy 2.0 found at https://pypi.org/project/ahpy/"
)

# Input beers
brands_labels = []
beer = input(
    "\n\nWhat beers would you like to compare? Introduce them one by one (input 'n' to stop): "
)
while beer != "n":
    brands_labels.append(beer)
    print("Current list is: ", brands_labels)
    beer = input(
        "What beers would you like to compare? Introduce them one by one (input 'n' to stop): "
    )

# Input criteria
criteria_labels = []
crit = input(
    "\n\nWhat criteria would you like to use? Introduce them one by one (input 'n' to stop): "
)
while crit != "n":
    criteria_labels.append(crit)
    print("Current list is: ", criteria_labels)
    crit = input(
        "What criteria would you like to use? Introduce them one by one (input 'n' to stop): "
    )

# Criteria ranking
print(
    "How do you think these criteria's relative importance compare? (from 9 (first one is incredibly more important) to 1 (they are equal) to -9 (second one is incredibly more important))"
)
criteria_pairs = []
for i in range(len(criteria_labels)):
    for j in range(len(criteria_labels) - 1 - i):
        criteria_pairs.append((criteria_labels[i], criteria_labels[j + 1 + i]))

criteria = {}

keep_going = True

while keep_going:
    for pair in criteria_pairs:
        prompt = f"{pair[0]}, {pair[1]}: "
        criteria[pair] = float(input(prompt))
        if criteria[pair] < 0:
            criteria[pair] = -1 / criteria[pair]

    criteria_ahpy = ahpy.Compare(
        "Criteria", criteria, precision=3, random_index="saaty"
    )
    consistency = criteria_ahpy.consistency_ratio
    if consistency <= 0.1:
        keep_going = False
    else:
        answer = input(
            f"Your answers were not very consistent (with an inconsistency ratio of {consistency} > 0.1). To get the best results we recommend going through this exercise again. Do you agree to go through it again (y-yes, n-no): "
        )
        if answer != "y":
            keep_going = False

# Beer ranking per criteria
print("Now we will analyse each of the brands for each of the criteria")

brands_pairs = []
for i in range(len(brands_labels)):
    for j in range(len(brands_labels) - 1 - i):
        brands_pairs.append((brands_labels[i], brands_labels[j + 1 + i]))

comparisons = {}
comparisons_ahpy = []

comp = {}

for criteria in criteria_labels:
    print(
        f"How do the beers compare in {criteria}? (from 9 (first one is incredibly more important) to 1 (they are equal) to -9 (second one is incredibly more important))'"
    )

    keep_going = [True, False]

    while keep_going[0]:
        for pair in brands_pairs:
            prompt = f"{pair[0]}, {pair[1]}: "
            comp[pair] = float(input(prompt))
            if comp[pair] < 0:
                comp[pair] = -1 / comp[pair]

        comparisons[criteria] = comp

        consistency = ahpy.Compare(
            criteria, comp, precision=3, random_index="saaty"
        ).consistency_ratio

        if consistency <= 0.1:
            keep_going[0] = False
            comparisons_ahpy.append(
                ahpy.Compare(criteria, comp, precision=3, random_index="saaty")
            )
        else:
            keep_going[1] = True
            answer = input(
                f"Your answers were not very consistent for {criteria} (with an inconsistency ratio of {consistency} > 0.1). To get the best results we recommend going through this exercise for {criteria} again. Do you agree to go through it again (y-yes, n-no): "
            )
            if answer != "y":
                keep_going[0] = False
                comparisons_ahpy.append(
                    ahpy.Compare(criteria, comp, precision=3, random_index="saaty")
                )

# Output results
criteria_ahpy.add_children(comparisons_ahpy)
criteria_ahpy.target_weights
print("\n\nWe have your results! These are the relative scores: ")
for beer in brands_labels:
    print(f"{beer}: {criteria_ahpy.target_weights[beer]*100:.2f}%")
