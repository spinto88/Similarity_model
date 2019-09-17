#include "dynamics.h"

double overlap(double a, double b, double c)
{
	double min, max;
	double r;
	
	min = a;
	if(b < a) { min = b; if(c < b) min = c; }
	else { if(c < a) min = c; }

	if((a+b-1.00) > 0.00) {	max = a + b - 1.00; }
	else max = 0.00;

	r = 0.5*(min + max);
	
	return r;
}

int dynamics(mysys *msys, double delta_up, double delta_down, double threshold, int steps)
{
	int i, j, k;
	double random = 0.00;
	int step = 0;
	int step_n = 0;
	double proba2interact = 0.00;
	int number_active_links = 0;
	link *list_active_links;

	while(step < steps)
	{
		step_n = 0;
	        srand(msys->seed);
		number_active_links = number_of_active_links(msys, delta_up, delta_down, threshold);
		if(number_active_links == 0)
			break;
		else
		{
			list_active_links = (link *)malloc(sizeof(link) * number_active_links);
			active_links(msys, delta_up, delta_down, threshold, list_active_links);
		}
			
		while(step_n < number_active_links)
		{
			k = rand() % number_active_links;
			i = list_active_links[k].i;
			j = list_active_links[k].j;

			if(active_condition(msys, i, j, delta_up, delta_down, threshold) == 1)
			{		

				random = (double)rand()/RAND_MAX;

				proba2interact = (msys->corr[i][j] - threshold)/(1.00 - threshold);
				
				if(random < proba2interact)
					increase_similarity(msys, i, j, delta_up);
			  	else
			  	{
					if(delta_down != 0.00)
						decrease_similarity(msys, i, j, delta_down);
				}
			}

			step_n++;
		}

		free(list_active_links);
		step++;

	        msys->seed = rand();
	}

	return 1;
}

int increase_similarity(mysys *msys, int i, int j, double delta_up)
{

	int k;
	int n = msys->n;
	double aux, factor;

	aux = msys->corr[i][j] + delta_up;
	if(aux >= 1.00)
		aux = 1.00;	
	if(aux < 1.00)
	{
		factor = delta_up / (1.00 - msys->corr[i][j]);
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				msys->corr[i][k] += (msys->corr[j][k] - msys->corr[i][k]) * factor;
				msys->corr[k][i] = msys->corr[i][k];
			}
		}
	}	
	else if(aux == 1.00)
	{
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				msys->corr[i][k] = msys->corr[j][k];	
				msys->corr[k][i] = msys->corr[i][k];	
			}
		}
	}

	msys->corr[i][j] = aux;
	msys->corr[j][i] = msys->corr[i][j];

	return 1;
}

int decrease_similarity(mysys *msys, int i, int j, double delta_down)
{

	int k;
	int n = msys->n;
	double aux, factor;

	aux = msys->corr[i][j] - delta_down;
	
	if(aux < 0.00)
		aux = 0.00;

	if(aux > 0.00)
	{
		factor = delta_down / msys->corr[i][j];
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				msys->corr[i][k] -= overlap(msys->corr[i][j], msys->corr[j][k], msys->corr[i][k]) * factor;
				msys->corr[k][i] = msys->corr[i][k];
			}
		}
	}
	else
	{
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				msys->corr[i][k] -= overlap(msys->corr[i][j], msys->corr[j][k], msys->corr[i][k]);
				msys->corr[k][i] = msys->corr[i][k];
			}
		}
	}

	msys->corr[i][j] = aux;
	msys->corr[j][i] = msys->corr[i][j];

	return 1;
}
