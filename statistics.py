import matplotlib.pyplot as plt
import pandas as pd

def read_dataframes():
    all_words_df = pd.read_excel('all_words.xlsx')
    all_verbs_df = pd.read_excel('all_verbs.xlsx')
    tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx')
    verbs_df = pd.read_excel('verbs.xlsx')
    return all_words_df,all_verbs_df,tagged_verbs_df,verbs_df
# Calculate the total number of words
all_words_df,all_verbs_df,tagged_verbs_df,verbs_df = read_dataframes()
total_words = len(all_words_df)

# Calculate the number of words with BINYAN=NIFAL
nifal_words = len(verbs_df[verbs_df["binyan"] == "NIFAL"])

# Calculate the percentage of words with BINYAN=NIFAL
nifal_percentage = nifal_words / total_words * 100

# Create a pie chart to visualize the results
plt.pie([nifal_percentage, 100 - nifal_percentage], labels=["NIFAL", "Other"], autopct="%1.1f%%")
plt.title("Percentage of words with BINYAN=NIFAL")
plt.show()

# Calculate the number of words for each BINYAN value
binyan_counts = all_verbs_df["BINYAN"].value_counts()
# Create a bar chart to visualize the results
ax = binyan_counts.plot(kind="bar")
plt.title("Number of words for each BINYAN value")
plt.xlabel("BINYAN value")
plt.ylabel("Number of words")

# Set the font size of the x-axis labels
plt.xticks(fontsize=8)

# Add text annotations to the top of each bar
for i, count in enumerate(binyan_counts):
    plt.text(i, count, str(count), ha="center", va="bottom")

plt.show()
