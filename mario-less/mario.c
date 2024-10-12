#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt user for height
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // print wall
    for (int i = 0; i < height; i++)
    {

        // print dots
        for (int j = height - 1; j > i; j--)
        {
            printf(" ");
        }

        // print bricks
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
