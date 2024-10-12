#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(char text[]);
int count_sentences(string text);
int calculate_grade(int letters, int words, int sentences);

int main(void)
{
    // Getting user input
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    int grade = calculate_grade(letters, words, sentences);

    // Print Grade
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

    return 0;
}
int count_letters(string text)
{
    // Counting letters
    int count_letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)

    {
        if (isalpha(text[i]))

        {
            count_letters++;
        }
    }
    return count_letters;
}
int count_words(char text[])
{
    // Counting words
    int count_words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)

    {
        if (text[i] == ' ')

        {
            count_words++;
        }
    }

    return count_words;
}
int count_sentences(string text)
{
    // Counting sentences
    int count_sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))

        {
            count_sentences++;
        }
    }
    return count_sentences;
}
int calculate_grade(int letters, int words, int sentences)
{
    // Coleman-Liau index Function
    float L = ((float) letters / words) * 100;
    float S = ((float) sentences / words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    int round_index = round(index);

    return round_index;
}
