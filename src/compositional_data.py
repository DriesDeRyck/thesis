import numpy as np
import matplotlib.pyplot as plt

# Time or sample index
x = np.arange(0, 10)

# Absolute abundances
increasing = np.linspace(4, 12, 10)
constant_top = np.full_like(x, 4)

decreasing = np.power(1.05, np.linspace(10, 1, 10)*2.8)
constant_bottom = np.full_like(x, 4)

# Relative abundances (normalized to sum to 1 at each time point)
top_total = increasing + constant_top
top_rel_inc = increasing / top_total
top_rel_const = constant_top / top_total

bottom_total = decreasing + constant_bottom
bottom_rel_dec = decreasing / bottom_total
bottom_rel_const = constant_bottom / bottom_total

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Absolute vs. Relative Abundances", fontsize=16)

# Top-left: Absolute abundances (increasing + constant)
axs[0, 0].plot(x, increasing, label='A', color='blue', marker='o')
axs[0, 0].plot(x, constant_top, label='B', color='orange', marker='o')
axs[0, 0].set_title('Absolute Abundance')
axs[0, 0].set_ylabel('Abundance')
axs[0, 0].legend()

# Top-right: Relative abundances
axs[0, 1].set_ylim(0, 1)
axs[0, 1].plot(x, top_rel_inc, label='A', color='blue', marker='o')
axs[0, 1].plot(x, top_rel_const, label='B', color='orange', marker='o')
axs[0, 1].set_title('Relative Abundance')
axs[0, 1].set_ylabel('Abundance')
axs[0, 1].legend()

# Bottom-left: Absolute abundances (decreasing + constant)
axs[1, 0].plot(x, decreasing, label='C', color='green', marker='o')
axs[1, 0].plot(x, constant_bottom, label='D', color='red', marker='o')
axs[1, 0].set_title('Absolute Abundance')
axs[1, 0].set_xlabel('Sample')
axs[1, 0].set_ylabel('Abundance')
axs[1, 0].legend()

# Bottom-right: Relative abundances
axs[1, 1].set_ylim(0, 1)
axs[1, 1].plot(x, bottom_rel_dec, label='C', color='green', marker='o')
axs[1, 1].plot(x, bottom_rel_const, label='D', color='red', marker='o')
axs[1, 1].set_title('Relative Abundance')
axs[1, 1].set_ylabel('Abundance')
axs[1, 1].set_xlabel('Sample')
axs[1, 1].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.subplots_adjust(wspace=0.3)  # Increase from default (~0.2)

plt.savefig("../figures/compositional_data.png")
plt.show()
