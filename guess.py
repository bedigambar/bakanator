import pandas as pd

csv_path = r"guess.csv"
df = pd.read_csv(csv_path)

def guess_object(df, csv_path):
    print("Hello! I am BakaNator.\nThink of an object (person, animal, thing). And I will try to guess it for you.")
    input("Press Enter when you're ready!")

    remaining = df.copy()

    traits = [col for col in df.columns if col != "Name"]
    print("\nPlease answer with: Yes / No / Maybe / Maybe Not / I don't know\n")
    user_answers = {}

    for trait in traits:
        answer = input(f"Is it '{trait}'? ").strip().lower()
        while answer not in ["yes", "no", "maybe", "maybe not", "i don't know", "idk"]:
            print("Invalid answer. Please respond with: Yes / No / Maybe / Maybe Not / I don't know.")
            answer = input(f"Is it '{trait}'? ").strip().lower()
        user_answers[trait] = answer
        if answer == "yes":
            remaining = remaining[remaining[trait] == "Yes"]
        elif answer == "no":
            remaining = remaining[remaining[trait] == "No"]
        else:
            pass 

        if len(remaining) == 0:
            print("\n I couldn't guess it. You stumped me!")
            return learn_new_object(df, user_answers, traits, csv_path)

        if len(remaining) == 1:
            guess = remaining.iloc[0]['Name']
            print(f"\n I guess... you're thinking of: ***{guess}***!")
            correct = input("Is my guess correct? (yes/no): ").strip().lower()
            while correct not in ["yes", "no"]:
                correct = input("Please answer with 'yes' or 'no': ").strip().lower()
            if correct == "yes":
                print("Yay! I guessed it right! ")
                return df
            else:
                print("Oh no! Let's improve my knowledge.")
                return learn_new_object(df, user_answers, traits, csv_path)

    print("\n I'm not sure, but here are some guesses:")
    for name in remaining["Name"].values:
        print(f" - {name}")
    return df

# Function to learn a new object
def learn_new_object(df, user_answers, traits, csv_path):
    print("\nHelp me learn! What was the object you were thinking of?")

    name = input("Enter the name: ").strip()
    new_data = {"Name": name}

    for trait in traits:
        ans = user_answers.get(trait, "no").strip().lower()
        if ans == "yes":
            new_data[trait] = "Yes"
        elif ans == "no":
            new_data[trait] = "No"
        else:
            new_data[trait] = "No"

    df_new = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df_new.to_csv(csv_path, index=False)
    print(f"\nThanks! I've added '{name}' to my knowledge base.")
    return df_new

df = guess_object(df, csv_path)             # Run the game and update df accordingly