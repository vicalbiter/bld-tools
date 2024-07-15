import os
import csv
import random
import argparse
import pandas as pd

def create_groups(excel_path: str, output_directory: str):
    """Create individual groups CSVs"""
    pairs = pd.read_excel(excel_path, index_col=0)

    pairs_long = (
        pairs
        .melt(ignore_index=False)
        .reset_index()
        .dropna()
        .assign(letter_pair=lambda df: df["index"] + df["variable"])
        .rename(columns={"value": "image"})
        .pipe(lambda df: df[["letter_pair", "image"]])
        .pipe(lambda df: df[df.image != "."])
    )

    learn_last = lambda x: ("A" in x) or ("E" in x) or ("R" in x)

    pair_groups = (
        pairs_long
        .assign(learn_last = lambda df: df["letter_pair"].map(learn_last))
        .assign(rank=lambda df: df["letter_pair"].rank())
        .assign(rank=lambda df: df.apply(lambda x: x["rank"] * 100 if x.learn_last else x["rank"], axis=1))
        .assign(rank=lambda df: df["rank"].rank())
        .sort_values("rank")
        .assign(first_letter=lambda df: df["letter_pair"].map(lambda x: x[0]))
    )

    # Split between main and last-to-learn groups
    main_groups = pair_groups.pipe(lambda df: df[~df.learn_last])
    last_groups = pair_groups.pipe(lambda df: df[df.learn_last])

    # Save csvs
    for l, group in main_groups.groupby("first_letter"):
        file_path = os.path.join(output_directory, f"bld_pairs_{l}.csv")
        group[["letter_pair", "image"]].to_csv(file_path, index=False)

    file_path = os.path.join(output_directory, "bld_pairs_Z.csv")
    last_groups[["letter_pair", "image"]].to_csv(file_path, index=False)

def load_csv_files(directory):
    csv_files = {}
    for filename in os.listdir(directory):
        if filename.startswith("bld_pairs_") and filename.endswith(".csv"):
            letter = filename.split("_")[-1][0]
            csv_files[letter] = os.path.join(directory, filename)
    return csv_files

def load_word_pairs(file_paths):
    word_pairs = {}
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                letter_pair = row['letter_pair'].strip()
                image = row['image'].strip()
                word_pairs[letter_pair] = {'image': image, 'counter': 0}
    return word_pairs

def compare_answers(correct, user_input):
    correct_set = set(correct.lower().replace(" ", ""))
    user_set = set(user_input.lower().replace(" ", ""))
    return correct_set == user_set

def drill_groups(word_pairs, n_master):
    active_pairs = list(word_pairs.keys())
    while active_pairs:
        pair = random.choice(active_pairs)
        print(f"\nLetter pair: {pair}")
        user_answer = input("Your answer: ").strip()
        
        if user_answer.lower() == 'quit':
            return
        
        correct_answer = word_pairs[pair]['image']
        if compare_answers(correct_answer, user_answer):
            print("Correct!")
            word_pairs[pair]['counter'] += 1
            if word_pairs[pair]['counter'] == n_master:
                print(f"You've mastered '{pair}'!")
                active_pairs.remove(pair)
        else:
            print(f"Incorrect. The correct answer is: {correct_answer}")
            word_pairs[pair]['counter'] = 0

def main():
    parser = argparse.ArgumentParser(description="BLD Pairs Drilling Program")
    parser.add_argument("--n_master", type=int, default=3, help="Number of correct answers required for mastery")
    args = parser.parse_args()
    
    directory = "C:\\Users\\Vicente\\Documents\\Projects\\cubing\\sc-tools\\docs\\groups"
    excel_path = os.path.join(directory, "Bld Pairs.xlsx")
    
 # Create CSV files from Excel
    create_groups(excel_path, directory)
    
    # Load CSV files
    csv_files = load_csv_files(directory)
    
    print(f"Mastery requires {args.n_master} correct answers")
    
    while True:
        print("\nAvailable groups:", ", ".join(sorted(csv_files.keys())))
        group_input = input("Select group(s) to drill (space-separated, or 'exit' to quit): ").upper()
        
        if group_input == 'EXIT':
            break
        
        selected_groups = group_input.split()
        valid_groups = [group for group in selected_groups if group in csv_files]
        
        if not valid_groups:
            print("No valid groups selected. Please try again.")
            continue
        
        print(f"Drilling groups: {', '.join(valid_groups)}")
        
        selected_files = [csv_files[group] for group in valid_groups]
        word_pairs = load_word_pairs(selected_files)
        drill_groups(word_pairs, args.n_master)

if __name__ == "__main__":
    main()