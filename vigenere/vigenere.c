#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

// allows for command line arguments in my program.
int main(int argc, string argv[])
{
    // condtion for if argc is not 2
    if (argc != 2)
    {
        // prints error message if input is not valid.
        printf("Please enter a valid input\n");
        return 1;
    }

    string key = argv[1];
    // stores length of key string in key_length as an integer
    int key_length = strlen(key);
    // for loop that will cycle through each individual letter of the key until it hits the length of the key.
    for (int i = 0; i < key_length; i++)
    {
        // stores idicies of the key as letters
        char letter = key[i];
        // sets conditon if key is not a letter
        if (!isalpha(letter))
        {
            // prints error message
            printf("Key needs to be alphabetical letters only\n");
            return 1;
        }
    }

    // prints plaintext
    printf("plaintext:");
    // prompts user for plaintext
    string plaintext = get_string();
    // stores length of plaintext string in word_length as an integer
    int word_length = strlen(plaintext);

    // prints ciphertext
    printf("ciphertext:");
    // for loop that will cycle through each individual letter of the plaintext and key until it hits the length of each.
    for (int i = 0, j = 0; i < word_length; i++)
    {
        // storing ASCII value into plain_ascii to avoid redundancies in the for loop
        int plain_ascii = 'A';
        // storing ASCII value into key_ascii to avoid redundancies in the for loop
        int key_ascii = 'A';
        // stores letters in plaintext into the variable plain_letter to reduce redundancies in the for loop
        char plain_letter = plaintext[i];
        // stores letters in the key into the variable key_letter to reduce redundancies in the for loop
        char key_letter = key[j];
        // stores integer 26 (letters in alphabet) as num_letters variable to make code more readable.
        int num_letters = 26;
        // checks if plain_letter is in the alphabet
        if (isalpha(plain_letter))
        {
            // checks if plain_letter is uppercase and if key_letter is uppercase
            if (isupper(plain_letter) && isupper(key_letter))
            {
                // stores uppercase ASCII value for plain_ascii
                plain_ascii = 'A';
                // stores uppercase ASCII value for key_ascii
                key_ascii = 'A';
            }
            // checks if plain_letter is lowercase and if key_letter is lowercase
            else if (islower(plain_letter) && islower(key_letter))
            {
                // stores lowercase ASCII value for plain_ascii
                plain_ascii = 'a';
                // stores lowercase ASCII value for key_ascii
                key_ascii = 'a';
            }
            // checks if plain_letter is uppercase and if key_letter is lowercase
            else if (isupper(plain_letter) && islower(key_letter))
            {
                // stores uppercase ASCII value for plain_ascii
                plain_ascii = 'A';
                // stores lowercase ASCII value for key_ascii
                key_ascii = 'a';
            }
            // checks if plain_letter is lowercase and if key_letter is uppercase
            else if (islower(plain_letter) && isupper(key_letter))
            {
                //stores lowercase ASCII value for plain_ascii
                plain_ascii = 'a';
                //stores uppercase ASCII value for key_ascii
                key_ascii = 'A';
            }

            /* creates cipher letter by substracting the plain_ascii
            from the plain_letter and the same for the key and adds them which will
            convert it to alphabetical index. Next we have to mod by 26 (num_letters) to wrap
            around the entire alphabet. Last we add the plain_ascii value to convert back to ASCII. */
            int cipher = ((plain_letter - plain_ascii) + (key_letter - key_ascii)) % num_letters + plain_ascii;
            // prints the cipher
            printf("%c", cipher);
            // adds one to the key to go through the key, and you mod by the key length so it wraps around the key.
            j = (j + 1) % key_length;
        }
        //condition if given input does not contain alphabetic letters
        else
        {
            //prints whatever input was given
            printf("%c", plain_letter);
        }
    }

    // prints cipher text on new line
    printf("\n");
    return 0;
}