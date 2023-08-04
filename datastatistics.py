import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def read_dataframes():
    tanach_words_df = pd.read_excel('tanach_words.xlsx')
    tanach_verbs_df = pd.read_excel('tanach_verbs.xlsx')
    tanach_tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx', sheet_name='Tanach verbs')
    wiki_words_df = pd.read_excel('wiki_words.xlsx')
    wiki_verbs_df = pd.read_excel('wiki_verbs.xlsx')
    wiki_tagged_verbs_df = pd.read_excel('tagged_verbs.xlsx', sheet_name='Wiki verbs')
    # wiki_nifal_df = pd.read_excel('nifal_tanach_verbs.xlsx', sheet_name='Tancah verbs')

    return tanach_words_df, tanach_verbs_df, tanach_tagged_verbs_df, wiki_words_df, wiki_verbs_df, wiki_tagged_verbs_df



tanach_words_df, tanach_verbs_df, tanach_tagged_verbs_df, wiki_words_df, wiki_verbs_df, wiki_tagged_verbs_df = read_dataframes()
total_words = len(tanach_words_df)


nifal_words = len(tanach_tagged_verbs_df[tanach_tagged_verbs_df["binyan"] == "NIFAL"])

nifal_percentage = nifal_words / total_words * 100

plt.pie([nifal_percentage, 100 - nifal_percentage], labels=["NIFAL", "Other"], autopct="%1.1f%%")
plt.title("Percentage of words with BINYAN=NIFAL")
plt.show()


binyan_counts = tanach_verbs_df["BINYAN"].value_counts()

ax = binyan_counts.plot(kind="bar")
plt.title("Number of words for each BINYAN value")
plt.xlabel("BINYAN value")
plt.ylabel("Number of words")

plt.xticks(fontsize=8)

for i, count in enumerate(binyan_counts):
    plt.text(i, count, str(count), ha="center", va="bottom")

plt.show()

tanach_tagged_verbs_df["lemma"] = tanach_tagged_verbs_df["lemma"].str.replace(r"\[.*", "", regex=True)
tanach_tagged_verbs_df["lemma"] = tanach_tagged_verbs_df["lemma"].str.replace(r"=.*", "", regex=True)
lemma_counts = tanach_tagged_verbs_df["lemma"].value_counts()

top_10_labels = [label[::-1] for label in lemma_counts.head(10).index]

labels = top_10_labels + [""] * (len(lemma_counts) - 10)

wedges, texts, autotexts = plt.pie(lemma_counts, labels=labels, autopct="%1.1f%%")
plt.setp(autotexts, size=4)
plt.title("Distribution of lemma values")
plt.show()

gender_counts = tanach_tagged_verbs_df['gender'].value_counts()

gender_counts.plot.pie(autopct='%.1f%%')
plt.title("Distribution of gender values")
plt.show()

glinert_counts = tanach_tagged_verbs_df['Glinert'].value_counts()
blau_counts = tanach_tagged_verbs_df['Blau'].value_counts()

plt.figure()
ax = glinert_counts.plot.bar()
plt.title('Glinert Distribution')
plt.xlabel('Glinert Type')
plt.ylabel('Count')
for i, count in enumerate(glinert_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')

plt.figure()
ax = blau_counts.plot.bar()
plt.title('Blau Distribution')
plt.xlabel('Blau Type')
plt.ylabel('Count')

for i, count in enumerate(blau_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')
plt.show()

glinert_counts = tanach_tagged_verbs_df['Glinert'].value_counts()
blau_counts = tanach_tagged_verbs_df['Blau'].value_counts()

plt.figure()
glinert_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=6)
plt.title('Glinert Distribution')

plt.figure()
blau_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=6)
plt.title('Blau Distribution')

plt.show()

tense_counts = tanach_tagged_verbs_df['tense'].value_counts()
person_counts = tanach_tagged_verbs_df['person'].value_counts()
syntactic_attributes_counts = tanach_tagged_verbs_df['syntactic attributes'].value_counts()
number_counts = tanach_tagged_verbs_df['number'].value_counts()
source_counts = tanach_tagged_verbs_df['source'].value_counts()


plt.figure()
tense_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=7)
plt.title('Tense Distribution')

plt.figure()
person_counts.plot.pie(autopct='%.1f%%')
plt.title('Person Distribution')

plt.figure()
syntactic_attributes_counts.plot.pie(autopct='%.1f%%')
plt.setp(autotexts, size=6)
plt.title('Syntactic Attributes Distribution')

plt.figure()
ax = syntactic_attributes_counts.plot.bar()
plt.title('Syntactic Attributes Distribution')
plt.xlabel('Syntactic Attribute Type')
plt.ylabel('Count')

for i, count in enumerate(syntactic_attributes_counts):
    ax.text(i, count, str(count), ha='center', va='bottom')


plt.figure()
number_counts.plot.pie(autopct='%.1f%%')
plt.title('Number Distribution')

source_counts.index = source_counts.index.str.replace('.xml', '')
plt.figure()
source_counts.plot.pie(autopct='%.1f%%')
plt.title('Source Distribution')

plt.show()
