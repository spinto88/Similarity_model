#ifndef ACTIVE_LINKS_H
#define ACTIVE_LINKS_H

#include <stdio.h>
#include <stdlib.h>
#include "model.h"

struct _link
{
        int i;
        int j;
};
typedef struct _link link;

int active_condition(mysys *, int, int, double);

int number_of_active_links(mysys *, double);
int active_links(mysys *, double, link *);

#endif
