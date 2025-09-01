import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1) Load Data
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# 2) Clean Data (just drop duplicates)
def clean_data(df):
    df = df.drop_duplicates(subset=["Member_ID"])
    return df

# 3) Analysis
def analyze_data(df):
    print("\n--- Basic Analysis ---")
    print("Average Progress Score:", df["Progress_Score"].mean())
    print("Max Calories Burned:", df["Calories_Burned"].max())
    print("Min Calories Burned:", df["Calories_Burned"].min())
    print("\nWorkout Type Count:\n", df["Workout_Type"].value_counts())

    # Unique insights
    top_workout = df.groupby("Workout_Type")["Calories_Burned"].mean().idxmax()
    best_row = df.loc[df["Progress_Score"].idxmax()]
    print("\n--- Unique Insights ---")
    print("Workout with highest avg calories:", top_workout)
    print("Best Performer:", best_row["Name"], "with score", best_row["Progress_Score"])

# 4) Charts
def generate_charts(df, charts_dir="charts"):
    os.makedirs(charts_dir, exist_ok=True)

    # Bar chart
    plt.figure(figsize=(6,4))
    df["Workout_Type"].value_counts().plot(kind="bar")
    plt.title("Workout Type Distribution")
    plt.xlabel("Workout Type")
    plt.ylabel("No. of Members")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "workout_type_bar.png"))
    plt.close()

    # Histogram
    plt.figure(figsize=(6,4))
    plt.hist(df["Progress_Score"], bins=10)
    plt.title("Progress Score Distribution")
    plt.xlabel("Progress Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "progress_score_hist.png"))
    plt.close()

    # Pie chart
    plt.figure(figsize=(6,6))
    df["Workout_Type"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Workout Type Percentage")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "workout_type_pie.png"))
    plt.close()

def main():
    df = load_data("fitness_tracker.xlsx")
    df_clean = clean_data(df)
    analyze_data(df_clean)
    generate_charts(df_clean)

if __name__ == "__main__":
    main()
