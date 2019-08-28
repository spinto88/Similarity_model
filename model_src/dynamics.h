#ifndef DYNAMICS_H
#define DYNAMICS_H

#include <stdio.h>
#include <stdlib.h>
#include "model.h"
#include "active_links.h"

int dynamics_asimetric(mysys *, double, double, int);
int dynamics_simetric(mysys *, double, double, int);

int one_step_simetric(mysys *, double, int, int);
int one_step_asimetric(mysys *, double, int, int);
#endif
