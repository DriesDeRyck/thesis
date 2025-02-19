import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from tqdm import tqdm

correlation_df = pd.read_csv("./data/correlation_matrix.tsv", sep='\t', index_col=0)
pvalues_df = pd.read_csv("./data/correlation_pvalues.tsv", sep='\t', index_col=0)
#%%
# plt.hist(correlation_df.to_numpy(), bins=10)
# correlation_df.stack().plot(kind='hist', alpha=0.5, bins=20)
# plt.show()
# pvalues_df.stack().plot(kind='hist', alpha=0.5, bins=20, range=(0, 0.1))
# test = pvalues_df.where(pvalues_df < 0.05)
#
# pvalues_df.head()
# test.head()

correlation_df = correlation_df.where(abs(correlation_df) >= 0.5)
print(f"# Remaining microbe-metabolite pairs: {correlation_df.stack().count()}")

# save selection
correlation_df.to_csv("./data/correlation_filtered.tsv", sep='\t', index=True)


# make figure
figure = plt.figure()
axes = figure.add_subplot()

# using the matshow() function
caxes = axes.matshow(correlation_df, cmap='coolwarm')
figure.colorbar(caxes, orientation='horizontal')
plt.title("Correlation matrix where correlation >= 0.5")
figure.tight_layout()  # otherwise the right y-label is slightly clipped

plt.savefig("./figures/correlation_filtered.png")

# correlation_df.stack().plot(kind='hist', alpha=0.5, bins=50)
# plt.show()

# plt.show()