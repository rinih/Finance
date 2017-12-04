// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

#define NUM_BUCKETS 600000
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
node *hashtable[NUM_BUCKETS];

int num_words = 0;
// Hash function was found at https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
unsigned int hash_word(const char* word)
 {
     unsigned long hash = 5381;

     for (const char* ptr = word; *ptr != '\0'; ptr++)
     {
         hash = ((hash << 5) + hash) + tolower(*ptr);
     }

     return hash % NUM_BUCKETS;
 }

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hash_i = hash_word(word);
    if(hashtable[hash_i] == NULL)
    {
        return false;
    }


    node *cursor = hashtable[hash_i];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}
// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if(file == NULL)
    {
       return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%s", word)!= EOF)
    {
        num_words++;
        node* new_node = malloc(sizeof(node));
        strcpy (new_node->word, word);
        int hash_i = hash_word(word);
        if (hashtable[hash_i] == NULL)
        {
            hashtable[hash_i] = new_node;
            new_node -> next = NULL;
        }
        else
        {
            new_node->next = hashtable[hash_i];
            hashtable[hash_i] = new_node;
        }

    }

    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return num_words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int hash_i = 0; hash_i < NUM_BUCKETS; hash_i++)
    {
      if (hashtable[hash_i] == NULL)
      {
          continue;
      }
      else
      {
          node *cursor = hashtable[hash_i];
          while(cursor != NULL)
          {
              node *temp = cursor;
              cursor = cursor -> next;
              free(temp);
          }

      }
    }
    return true;
}

