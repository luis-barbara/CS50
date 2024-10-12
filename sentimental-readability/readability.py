from cs50 import get_string

# Getting user input
text = get_string("Text: ")

letters = 0
words = 1
sentences = 0


# Counting letters, words, sentences
for i in text:
    if i.isalpha():
        letters += 1
    elif i == " ":
        words += 1
    elif i == "." or i == "!" or i == "?":
        sentences += 1

# Coleman-Liau index Function
L = letters / words * 100
S = sentences / words * 100

grade = 0.0588 * L - 0.296 * S - 15.8

# Print Grade
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print("Grade", round(grade))
