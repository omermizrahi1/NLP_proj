import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Function to format the autopct value
def format_autopct(pct):
    return f"{pct:.1f}%" if pct > 0 else ""

def read_dataframes():
    tanach_words_df = pd.read_excel('tanach_words.xlsx')
    tanach_verbs_df = pd.read_excel('tanach_verbs.xlsx')
    tanach_tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx', sheet_name='Tanach verbs')
    wiki_words_df = pd.read_excel('wiki_words.xlsx')
    wiki_verbs_df = pd.read_excel('wiki_verbs.xlsx')
    wiki_tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx', sheet_name='Wiki verbs')
    # wiki_nifal_df = pd.read_excel('nifal_tanach_verbs.xlsx', sheet_name='Tancah verbs')

    return tanach_words_df, tanach_verbs_df, tanach_tagged_verbs_df, wiki_words_df, wiki_verbs_df, wiki_tagged_verbs_df


# Calculate the total number of words
tanach_words_df, tanach_verbs_df, tanach_tagged_verbs_df, wiki_words_df, wiki_verbs_df, wiki_tagged_verbs_df = read_dataframes()
total_words = len(tanach_words_df)

# Calculate the number of words with BINYAN=NIFAL
nifal_words = len(tanach_tagged_verbs_df[tanach_tagged_verbs_df["binyan"] == "NIFAL"])

# Calculate the percentage of words with BINYAN=NIFAL
nifal_percentage = nifal_words / total_words * 100

# Create a pie chart to visualize the results
plt.pie([nifal_percentage, 100 - nifal_percentage], labels=["NIFAL", "Other"], autopct="%1.1f%%")
plt.title("Percentage of words with BINYAN=NIFAL")
plt.show()

# Calculate the number of words for each BINYAN value
binyan_counts = tanach_verbs_df["BINYAN"].value_counts()
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

# Clean up the lemma column
tanach_tagged_verbs_df["lemma"] = tanach_tagged_verbs_df["lemma"].str.replace(r"\[.*", "", regex=True)
tanach_tagged_verbs_df["lemma"] = tanach_tagged_verbs_df["lemma"].str.replace(r"=.*", "", regex=True)
# Calculate the number of rows for each lemma value
lemma_counts = tanach_tagged_verbs_df["lemma"].value_counts()

# Create a list of labels for the top 10 most common values
top_10_labels = [label[::-1] for label in lemma_counts.head(10).index]

# Create a list of labels for all values, with empty strings for values outside the top 10
labels = top_10_labels + [""] * (len(lemma_counts) - 10)

#  Create a pie chart to visualize the results
wedges, texts, autotexts = plt.pie(lemma_counts, labels=labels, autopct="%1.1f%%")
plt.setp(autotexts, size=4)
plt.title("Distribution of lemma values")
plt.show()

# assuming your dataframe is stored in a variable called df
gender_counts = tanach_tagged_verbs_df['gender'].value_counts()

# create a pie chart
gender_counts.plot.pie(autopct='%.1f%%')
plt.title("Distribution of gender values")
plt.show()

# assuming your dataframe is stored in a variable called df
glinert_counts = tanach_tagged_verbs_df['Glinert'].value_counts()
blau_counts = tanach_tagged_verbs_df['Blau'].value_counts()

# create a bar chart of the Glinert distribution
plt.figure()
ax = glinert_counts.plot.bar()
plt.title('Glinert Distribution')
plt.xlabel('Glinert Type')
plt.ylabel('Count')
# add the count of each type on top of the bars
for i, count in enumerate(glinert_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')

# create a bar chart of the Blau distribution
plt.figure()
ax = blau_counts.plot.bar()
plt.title('Blau Distribution')
plt.xlabel('Blau Type')
plt.ylabel('Count')

# add the count of each type on top of the bars
for i, count in enumerate(blau_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')
# show the charts
plt.show()

# assuming your dataframe is stored in a variable called df
glinert_counts = tanach_tagged_verbs_df['Glinert'].value_counts()
blau_counts = tanach_tagged_verbs_df['Blau'].value_counts()

# create a pie chart of the Glinert distribution
plt.figure()
glinert_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=6)
plt.title('Glinert Distribution')

# create a pie chart of the Blau distribution
plt.figure()
blau_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=6)
plt.title('Blau Distribution')

# show the charts
plt.show()

# assuming your dataframe is stored in a variable called df
tense_counts = tanach_tagged_verbs_df['tense'].value_counts()
person_counts = tanach_tagged_verbs_df['person'].value_counts()
syntactic_attributes_counts = tanach_tagged_verbs_df['syntactic attributes'].value_counts()
number_counts = tanach_tagged_verbs_df['number'].value_counts()
source_counts = tanach_tagged_verbs_df['source'].value_counts()


# create a pie chart of the tense distribution
plt.figure()
tense_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=7)
plt.title('Tense Distribution')

# create a pie chart of the person distribution
plt.figure()
person_counts.plot.pie(autopct='%.1f%%')
plt.title('Person Distribution')

# create a pie chart of the syntactic attributes distribution
plt.figure()
syntactic_attributes_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=6)
plt.title('Syntactic Attributes Distribution')

# create a bar chart of the syntactic attributes distribution
plt.figure()
ax = syntactic_attributes_counts.plot.bar()
plt.title('Syntactic Attributes Distribution')
plt.xlabel('Syntactic Attribute Type')
plt.ylabel('Count')

# add the count of each type on top of the bars
for i, count in enumerate(syntactic_attributes_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')


# create a pie chart of the number distribution
plt.figure()
number_counts.plot.pie(autopct='%.1f%%')
plt.title('Number Distribution')

# create a pie chart of the source distribution
source_counts.index = source_counts.index.str.replace('.xml', '')
plt.figure()
source_counts.plot.pie(autopct='%.1f%%')
# create a new series with the .xml extension removed from the index labels
plt.title('Source Distribution')

plt.show()
