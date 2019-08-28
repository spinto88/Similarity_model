#ifndef MODEL_H
#define MODEL_H

#include <stdlib.h>
#include <stdio.h>

struct _mysys
{
        int n;
        double **corr;
        int **a;
        int seed;
};
typedef struct _mysys mysys;

#endif 

