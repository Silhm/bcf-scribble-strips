#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


int main()
{
    unsigned char sysEx[] = {0xF0, 0x00, 0x00, 0x66, 0x00, 0x12, 0X57, 0x4C, 0x35, 0x31, 0x52, 0x34, 0x39, 0x20, 0xF7};

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
    

    printf("\n -------Handle a big sysEx data -------------- \n");
    // Received big frame 
    unsigned char bigSysEx[] = {
        0xF0, 0x00, 0x00, 0x66, 0x00, 0x12, 0X57, 0x4C, 0x35, 0x31, 0x52, 0x34, 0x39, 0x20, 0xF7, 
        0xF0, 0x00, 0x00, 0x66, 0x00, 0x12, 0x00, 0x4C, 0x34, 0x32, 0x52, 0x50, 0x59, 0x20, 0xF7,
        0xF0, 0x00, 0x00, 0x66, 0x00, 0x12, 0x00, 0x4C, 0x35, 0x30, 0x52, 0x50, 0x59, 0x39, 0x39, 0xF7};
    // function gives us the sysEx size as well
    int buffersize = 46;

    int i=0;
    int start=0;
    int frameCpt = 0;

    //declare frame structure
    typedef struct {
       int start;
       int size;
       unsigned char *data;
    } t_frame;

    t_frame *frames;
    frames = malloc( 3 * sizeof(t_frame) ); // initial size at 3
    // iter all data in sysEx
    while (i<buffersize) {
       // Start of frame
       if(bigSysEx[i] == 0xF0){
          //frames[frameCpt] = malloc(sizeof(t_frame));
           frames[frameCpt].start = i;
           frameCpt++;
       }
    
       // End of frame
       if(bigSysEx[i] == 0xF7){
            frames[frameCpt-1].size = 1+i-start ;
            frames[frameCpt-1].data = malloc(frames[frameCpt-1].size);
            memcpy(frames[frameCpt-1].data, bigSysEx + frames[frameCpt-1].start, frames[frameCpt-1].size);           

            printf(" Frame #%d |   start=%d  i=%d   \n",frameCpt,start, i);
            start = i+1;
       }
       // Display it 
       //printf("0x%X.",bigSysEx[i]);
       i++;
    }

    printf("\n --------------------- \n");

    int j=0;
    for(j=0; j<frameCpt;j++){
        printf("|%d (size:%d)| %s|  \n", j, frames[j].size, frames[j].data + 7);
    }

    printf("\n --------------------- \n ");


    return(0);
}

int getDisplay(char *sysEx){
    int offset = (sysEx[6] / 7) ;
        return offset % 8 ;
}

