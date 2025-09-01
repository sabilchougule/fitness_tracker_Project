import tkinter as tk
from tkinter import messagebox
import os
from main import load_data, clean_data, analyze_data, generate_charts
from PIL import Image, ImageTk

def show_data(df):
    top = tk.Toplevel()
    top.title("Data Preview")
    text = tk.Text(top, wrap="none", width=80, height=15)
    text.pack(padx=10, pady=10)
    text.insert("end", str(df.head(10)))

def show_analysis(df):
    top = tk.Toplevel()
    top.title("Analysis Report")

    avg_score = df["Progress_Score"].mean()
    max_cal = df["Calories_Burned"].max()
    min_cal = df["Calories_Burned"].min()
    workout_counts = df["Workout_Type"].value_counts()

    # Unique insights
    top_workout = df.groupby("Workout_Type")["Calories_Burned"].mean().idxmax()
    best_row = df.loc[df["Progress_Score"].idxmax()]

    text = f"""
Average Progress Score: {avg_score:.2f}
Max Calories Burned: {max_cal}
Min Calories Burned: {min_cal}

Workout Types Count:
{workout_counts.to_string()}

Unique Insights:
- Workout with highest avg calories: {top_workout}
- Best Performer: {best_row["Name"]} (Score: {best_row["Progress_Score"]})
"""
    tk.Label(top, text=text, justify="left", anchor="w").pack(padx=10, pady=10)

def show_best_performer(df):
    best_row = df.loc[df["Progress_Score"].idxmax()]
    messagebox.showinfo("🏆 Best Performer", f"{best_row['Name']} scored {best_row['Progress_Score']}")

def show_charts(df):
    charts_dir = "charts"
    generate_charts(df, charts_dir)

    for chart in ["workout_type_bar.png", "progress_score_hist.png", "workout_type_pie.png"]:
        chart_path = os.path.join(charts_dir, chart)
        if os.path.exists(chart_path):
            win = tk.Toplevel()
            win.title(chart)

            img = Image.open(chart_path)
            img = img.resize((500, 360))
            photo = ImageTk.PhotoImage(img)

            lbl = tk.Label(win, image=photo)
            lbl.image = photo  # keep a reference
            lbl.pack(padx=5, pady=5)

def main():
    root = tk.Tk()
    root.title("💪 Fitness Tracker (Tkinter)")
    root.geometry("360x280")

    file_path = "fitness_tracker.xlsx"
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Dataset not found! Place 'fitness_tracker.xlsx' in this folder.")
        return

    df = load_data(file_path)
    df_clean = clean_data(df)

    tk.Button(root, text="📄 Data Preview", command=lambda: show_data(df_clean)).pack(pady=8)
    tk.Button(root, text="📊 Analysis Report", command=lambda: show_analysis(df_clean)).pack(pady=8)
    tk.Button(root, text="📈 Show Charts", command=lambda: show_charts(df_clean)).pack(pady=8)
    tk.Button(root, text="🏆 Best Performer", command=lambda: show_best_performer(df_clean)).pack(pady=8)
    tk.Button(root, text="Exit", command=root.destroy).pack(pady=8)

    root.mainloop()

if __name__ == "__main__":
    main()
