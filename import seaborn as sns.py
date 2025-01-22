import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="ticks")

df = sns.load_dataset("penguins")
sns.pairplot(df, hue="species")
plt.show()