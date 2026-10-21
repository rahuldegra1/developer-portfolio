import csv

questions = []
with open("questions.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        formatted_question = {
            "question": row["Question"],
            "options": [row["Opt1"], row["Opt2"], row["Opt3"], row["Opt4"]],
            "answer": row["Answer"],
        }
        questions.append(formatted_question)
score = 0


for question in questions:
    print(question["question"])
    for option in question["options"]:
        print(option)
    user = input("your answer: ")

    if user.lower() == question["answer"].lower():
        print("correct!")
        score += 1
    else:
        print("Wrong. The answer was", question["answer"])

print(f"you scored {score} out of {len(questions)}")
