#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    // Check if the memory card file could not be opened
    if (card == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // Counter for JPEG files
    int jpeg_count = 0;

    // File pointer for JPEG files
    FILE *jpeg = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Check if the current block might be the start of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG file is already open, close it
            if (jpeg != NULL)
            {
                fclose(jpeg);
            }

            // Create a new JPEG file
            char filename[8];
            sprintf(filename, "%03d.jpg", jpeg_count++);
            jpeg = fopen(filename, "w");
            if (jpeg == NULL)
            {
                printf("Could not create JPEG file\n");
                fclose(card);
                return 2;
            }
        }

        // If a JPEG file is open, write the current block to it
        if (jpeg != NULL)
        {
            fwrite(buffer, 1, 512, jpeg);
        }
    }

    // Close the last JPEG file
    if (jpeg != NULL)
    {
        fclose(jpeg);
    }

    // Close the memory card
    fclose(card);

    return 0;
}
