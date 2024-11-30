import matplotlib.pyplot as plt
import numpy as np

# Data for the first plot
poisoning_rates1 = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
accuracies1 = [0.7, 0.9, 0.95, 0.93, 0.98, 1.0]
label1 = "Target 1: Sex = Female, Occupation = Sales (1.0% vs 3.5%)"

# Data for the second plot
poisoning_rates2 = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
accuracies2 = [0.4, 0.65, 0.9, 0.95, 0.97, 1.0]
label2 = "Target 2: Marital-status = Divorced, Sex = Male (1.0% vs 5.0%)"

# Plot
plt.figure(figsize=(12, 8))

# First dataset
plt.plot(
    poisoning_rates1,
    accuracies1,
    marker="o",
    linestyle="--",
    color="blue",
    label=label1,
)

# Second dataset
plt.plot(
    poisoning_rates2,
    accuracies2,
    marker="o",
    linestyle="--",
    color="green",
    label=label2,
)

# Title and labels
plt.title(
    "Attack Accuracy vs Poisoning Rate",
    fontsize=16,
    color="darkred",
    fontweight="bold",
    loc="center",
)
plt.xlabel("Poisoning Rate", fontsize=14, fontweight="bold")
plt.ylabel("Attack Accuracy", fontsize=14, fontweight="bold")

# Grid and legend
plt.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)
plt.legend(fontsize=12, loc="lower right", fancybox=True, framealpha=0.8)

# Add a decorative background color
plt.gca().set_facecolor("#f5f5f5")

# Save and show the plot
plt.tight_layout()
plt.savefig("/mnt/data/Merged_Attack_Accuracy_Plot.png")
plt.show()
