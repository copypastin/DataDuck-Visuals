import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import src.helpers.DataLoader as dl

df = dl.DataLooder("DataDucks", "Complied Professor Reviews").get_data()
df = dl.DataLooder("DataDucks", "Complied Professor Reviews").get_data()

# Giving each course a subject tag for better visualizations

subjects: list[str] = []
all_subjects: list[str] = []
for course in df["course_number"]:

    subject = course.split("-")[0]
    if subject not in subjects:
        subjects.append(subject)

    all_subjects.append(subject)

print(subjects)
df["subject"] = all_subjects
print(df.sample(5))



# rawScore = (6 - quality) + credits + difficulty
# workloadScore = (rawScore / highestWorkloadGlobal) * 100

worklaodScores: list[float] = []
highestWorkloadGlobal = 0

for index, row in df.iterrows():
    quality = row["quality"]
    credits = row["credit"]
    difficulty = row["difficulty"]

    workloadScore = ((6 - quality) + credits + difficulty) / 10 * 100
    worklaodScores.append(workloadScore)

    if workloadScore > highestWorkloadGlobal:
        highestWorkloadGlobal = workloadScore
    
for score in worklaodScores:
    score = (score / highestWorkloadGlobal) * 100

df["workload_score"] = worklaodScores

print(df.sample(5))




sns.scatterplot(
    data=df, x="quality", y="difficulty", hue="subject")

plt.show()