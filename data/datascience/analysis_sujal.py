import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

laptop = pd.read_csv("data/laptop.csv")

plt.figure(figsize=(14, 10))
sns.boxplot(data=laptop, x='ram memory', y='price',
            hue='ram memory', palette='deep')
plt.legend([], [], frameon=False)
plt.show()

# plt.figure(figsize=(14, 10))
# sns.boxplot(data=laptop, x='display size', y='price',
#             hue='display size', palette='deep')
# plt.legend([], [], frameon=False)
# plt.show()
#
#
# plt.figure(figsize=(14, 10))
# sns.boxplot(data=laptop, x='processor', y='price',
#             hue='processor', palette='deep')
# plt.legend([], [], frameon=False)
# plt.show()
#
# plt.figure(figsize=(14, 10))
# sns.boxplot(data=laptop, x='storage capacity', y='price',
#             hue='storage capacity', palette='deep')
# plt.legend([], [], frameon=False)
# plt.show()
