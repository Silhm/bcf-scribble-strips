#include <stdio.h>
#include <stdlib.h>
#include <math.h>


int main()
{
    char sysEx[] = {0xF0, 0x00, 0x00, 0x66, 0x00, 0x12, 0X57, 0x4C, 0x35, 0x31, 0x52, 0x34, 0x39, 0x20, 0xF7};
    char *ptr;
    char *readable = sysEx + 6;
    
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
    oledDisplay1.trackName = "Kick";
    oledDisplay1.assign = "Pn";




    
    return(0);
}

int getDisplay(char *sysEx){
    int offset = (sysEx[6] / 7) ;
        return offset % 8 ;
}

