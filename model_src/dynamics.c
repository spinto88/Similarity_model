#include "dynamics.h"

int dynamics(mysys *msys, double delta, double threshold, int steps, int simetric)
{
	int i, j, k;
	int step = 0;
	int step_n = 0;
	int number_active_links = 0;
	link *list_active_links;

	while(step < steps)
	{
		step_n = 0;
	        srand(msys->seed);
		if(simetric == 0)
			number_active_links = number_of_active_links(msys, threshold);
		else if(simetric == 1)
			number_active_links = number_of_active_links_simetric(msys, threshold);
		if(number_active_links == 0)
			break;
		else
		{
			list_active_links = (link *)malloc(sizeof(link) * number_active_links);
			if(simetric == 0)
				active_links(msys, threshold, list_active_links);
			else if(simetric == 1)
				active_links_simetric(msys, threshold, list_active_links);
		}
			
		while(step_n < number_active_links)
		{
			k = rand() % number_active_links;
			i = list_active_links[k].i;
			j = list_active_links[k].j;

			if(active_condition(msys, i, j, threshold) == 1)
			{
				if(simetric == 0)
					increase_similarity(msys, i, j, msys->corr[i][j]*delta);
				else if(simetric == 1)
					increase_similarity_simetric(msys, i, j, msys->corr[i][j]*delta);
			}

			step_n++;
		}

		free(list_active_links);
		step++;

	        msys->seed = rand();
	}

	return 1;
}

int increase_similarity(mysys *msys, int i, int j, double delta)
{
	int k;
	int n = msys->n;
	double aux, factor;

	aux = msys->corr[i][j] + delta;
	if(aux >= 1.00)
		aux = 1.00;	
	if(aux < 1.00)
	{
		factor = delta / (1.00 - msys->corr[i][j]);
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

int increase_similarity_simetric(mysys *msys, int i, int j, double delta)
{
	int k;
	int n = msys->n;
	double aux, factor;

	aux = msys->corr[i][j] + delta;
	if(aux >= 1.00)
		aux = 1.00;	
	if(aux < 1.00)
	{
		factor = 0.5 * delta / (1.00 - msys->corr[i][j]);
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				msys->corr[i][k] += (msys->corr[j][k] - msys->corr[i][k]) * factor;
				msys->corr[j][k] += (msys->corr[i][k] - msys->corr[j][k]) * factor;
				msys->corr[k][i] = msys->corr[i][k];
				msys->corr[k][j] = msys->corr[j][k];
			}
		}
	}	
	else if(aux == 1.00)
	{
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				msys->corr[i][k] = 0.5 * (msys->corr[j][k] + msys->corr[i][k]);	
				msys->corr[j][k] = 0.5 * (msys->corr[j][k] + msys->corr[i][k]);	

				msys->corr[k][i] = msys->corr[i][k];	
				msys->corr[k][j] = msys->corr[j][k];	

			}
		}
	}

	msys->corr[i][j] = aux;
	msys->corr[j][i] = msys->corr[i][j];

	return 1;
}
