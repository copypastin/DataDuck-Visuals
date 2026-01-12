import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import src.helpers.DataLoader as dl

df_course_averages = dl.DataLooder("DataDucks", "Class Averages").get_data()
df_course_info = dl.DataLooder("DataDucks", "Course Info").get_data()
workloadScores: list[float] = []
highestWorkloadGlobal = 0
df_master = df_course_info.copy()


rows_to_drop = []

for index, course in df_master.iterrows():

    course_id = course.class_id
    course_avg = df_course_averages[df_course_averages["course_id"] == course_id]  

    if course_avg.empty:
        rows_to_drop.append(index)
        continue
    
    quality = course_avg["average_quality"].values[0]
    difficulty = course_avg["average_difficulty"].values[0]
    credits = df_course_info[df_course_info["class_id"] == course_id]["credit"].values[0]

    df_master.at[index, "quality"] = quality
    df_master.at[index, "difficulty"] = difficulty

    # Calculating workload score

    # rawScore = (6 - quality) + credits + difficulty
    # workloadScore = (rawScore / highestWorkloadGlobal) * 100 

    calculatedWorkload = ((6 - quality) + credits + difficulty)
    workloadScores.append(calculatedWorkload)
    if calculatedWorkload > highestWorkloadGlobal:
        highestWorkloadGlobal = calculatedWorkload
        

df_master.drop(rows_to_drop, inplace=True)
        
workloadScores = [(score / highestWorkloadGlobal) * 100 for score in workloadScores]
df_master["workload_score"] = workloadScores
        


# Giving each course a subject tag for better visualizations

subjects: list[str] = []
all_subjects: list[str] = []
for course in df_master["class_id"]:

    subject = course.split("-")[0]
    if subject not in subjects:
        subjects.append(subject)

    all_subjects.append(subject)

print(subjects)

df_master["subject"] = all_subjects
print(df_master.sample(5))



# sns.scatterplot(
#     data=df_master, x="difficulty", y="workload_score", hue="subject",)

fig, ax = plt.subplots(figsize=(12, 6))
plt.xlim(0, 100)

sns.histplot(
    data=df_master, x="workload_score", hue="subject", multiple="stack", ax=ax
    )

ax.set_xlabel("Calculated Workload Score")
ax.set_ylabel("Number of Courses (n = {})".format(len(df_master)))
ax.set_title("Distribution of Calculated Workload Scores by Subject")

legend = ax.get_legend()
if legend:
    handles = legend.legend_handles
    labels = [t.get_text() for t in legend.get_texts()]
    legend.remove()
    
    ax.legend(
        handles, labels,
        title="Subject",
        fontsize=6,
        title_fontsize=8,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.2),
        ncol=6,
        frameon=False
    )

plt.subplots_adjust(bottom=0.35)
plt.savefig("workload_distribution.png", bbox_inches='tight', dpi=150)
plt.show()