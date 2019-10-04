#ifndef DYNAMICS_H
#define DYNAMICS_H

#include <stdio.h>
#include <stdlib.h>
#include "model.h"
#include "active_links.h"

int increase_similarity(mysys *, int, int, double);

int dynamics(mysys *, double, double, int);

#endif
