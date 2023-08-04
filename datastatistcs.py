import matplotlib.pyplot as plt
import pandas as pd

def read_dataframes():
    # tanach_words_df = pd.read_excel('tanach_words.xlsx')
    # tanach_verbs_df = pd.read_excel('tanach_verbs.xlsx')
    # tanach_tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx', sheet_name='Tancah verbs')
    # tanach_nifal_df = pd.read_excel('verbs.xlsx', sheet_name='Tancah verbs')
    wiki_words_df = pd.read_excel('wiki_words.xlsx')
    wiki_verbs_df = pd.read_excel('wiki_verbs.xlsx')
    wiki_tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx', sheet_name='Wiki verbs')
    wiki_nifal_df = pd.read_excel('verbs.xlsx', sheet_name='Wiki verbs')

    return wiki_words_df,wiki_verbs_df,wiki_tagged_verbs_df,wiki_nifal_df
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
binyan_counts = all_verbs_df["binyan"].value_counts()
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


# Read the dataframes
all_words_df,all_verbs_df,tagged_verbs_df,verbs_df = read_dataframes()

# Convert the gender values to lowercase to ensure uniformity
verbs_df['gender'] = verbs_df['gender'].str.lower()

# Calculate the gender distribution
gender_distribution = verbs_df['gender'].value_counts()

# Plot the gender distribution
plt.figure(figsize=(10, 10))
plt.pie(gender_distribution, labels = gender_distribution.index, autopct='%1.1f%%')
plt.title("Gender Distribution in wiki_nifal_df")
plt.show()  


verbs_df['lemma'] = verbs_df['lemma'].apply(lambda x: x[::-1])

# Calculate the lemma distribution (top 10)
lemma_distribution = verbs_df['lemma'].value_counts().nlargest(10)

# Plot the lemma distribution
plt.figure(figsize=(10, 5))
lemma_distribution.plot(kind='bar', color='green')
plt.title("Top 10 Lemmas in wiki_nifal_df")
plt.xlabel("Lemma")
plt.ylabel("Count")
plt.show()

# Calculate the Glinert distribution
glinert_distribution = tagged_verbs_df['Glinert'].value_counts()

# Plot the Glinert distribution
plt.figure(figsize=(10, 10))
plt.pie(glinert_distribution, labels = glinert_distribution.index, autopct='%1.1f%%')
plt.title("Glinert Distribution in wiki_nifal_df")
plt.show()

# Calculate the Glinert distribution
blau_distribution = tagged_verbs_df['Blau'].value_counts()

# Plot the Glinert distribution
plt.figure(figsize=(10, 10))
plt.pie(blau_distribution, labels = blau_distribution.index, autopct='%1.1f%%')
plt.title("Blau Distribution in wiki_nifal_df")
plt.show()

# Calculate the person distribution
person_distribution = verbs_df['person'].value_counts()

# Plot the person distribution
plt.figure(figsize=(10, 10))
plt.pie(person_distribution, labels = person_distribution.index, autopct='%1.1f%%')
plt.title("Person Distribution in wiki_nifal_df")
plt.show()

# Calculate the tense distribution
tense_distribution = verbs_df['tense'].value_counts()

# Plot the tense distribution
plt.figure(figsize=(10, 10))
plt.pie(tense_distribution, labels = tense_distribution.index, autopct='%1.1f%%')
plt.title("Tense Distribution in wiki_nifal_df")
plt.show()