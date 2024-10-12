#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function prototypes
bool only_digits(string key);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Check for valid key input
    if (argc != 2 || only_digits(argv[1]) == 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Get the key as an integer
    int key = atoi(argv[1]);

    // Get plaintext input
    string plaintext = get_string("plaintext:  ");

    printf("ciphertext: ");

    // Encrypt the plaintext
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char encrypted_char = rotate(plaintext[i], key);
        printf("%c", encrypted_char);
    }
    printf("\n");

    return 0;
}
// Function to check if the string contain only strings
bool only_digits(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isdigit(key[i]) || key[i] < '0' || key[i] > '9')

        {
            return false;
        }
    }
    return true;
}

// Function to rotate the characters
char rotate(char c, int n)
{
    if (isalpha(c))
    {
        if (islower(c))
        {
            return 'a' + (c - 'a' + n) % 26;
        }
        else if (isupper(c))
        {
            return 'A' + (c - 'A' + n) % 26;
        }
    }
    // Return unchanged if is not an alphatical character
    return c;
}
