#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main()
{
    char sysEx[] = {0xF0, 0x00, 0x00, 0x66, 0x00, 0x12, 0X57, 0x4C, 0x35, 0x31, 0x52, 0x34, 0x39, 0x20, 0xF7};
    char *ptr;
    char *readable = sysEx + 7;
    
    strtol(readable, &ptr, 10);
    printf("String part is |%s|\n", ptr);
    printf("offset |0x%x : %d |", sysEx[6], sysEx[6]);
    printf("Display |%d|", getDisplay(sysEx));

    struct channel {
        char* trackName;
        char* displayLine1;
        char* displayLine2;
        char* assign;
        char* faderLevel;
        int leftPan;
        int rightPan;
    };

    struct channel oledDisplay1;

    // allocate 7 bytes for 7 digits of the display line
    oledDisplay1.displayLine1 = malloc(7);
    // The 7 firsts bytes are used for <hdr>(5) + LCD message(1) + offset(1)
    strncpy(oledDisplay1.displayLine1, sysEx + 7, 7); // get next 7 bytes (skip the 0xF7 EOSysEx) 
    printf("\n oledDisplay1.displayLine1 :  |%s|  \n", oledDisplay1.displayLine1);
    
    return(0);
}

int getDisplay(char *sysEx){
    int offset = (sysEx[6] / 7) ;
        return offset % 8 ;
}

