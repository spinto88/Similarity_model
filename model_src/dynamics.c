#include "dynamics.h"

int dynamics_asimetric(mysys *msys, double delta, double threshold, int steps)
{
	int i, j, k;
	double random;
	int step = 0;
	int step_n = 0;
	double aux = 0.00;
	int n = msys->n;
	double factor;
	int number_active_links = 0;
	link *list_active_links;

	while(step < steps)
	{
		step_n = 0;
	        srand(msys->seed);
		number_active_links = number_of_active_links_asimetric(msys, delta, threshold);
		if(number_active_links == 0)
			break;
		else
		{
			list_active_links = (link *)malloc(sizeof(link) * number_active_links);
			active_links_asimetric(msys, delta, threshold, list_active_links);
		}
			
		while(step_n < number_active_links)
		{
			k = rand() % number_active_links;
			i = list_active_links[k].i;
			j = list_active_links[k].j;

			random = (double)rand()/RAND_MAX;

		        if((random < msys->corr[i][j]) && (active_condition(msys, i, j, delta, threshold) == 1))
			{		
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
			}
			step_n++;
		}

		free(list_active_links);
		step++;

	        msys->seed = rand();
	}

	return 1;
}

int dynamics_simetric(mysys *msys, double delta, double threshold, int steps)
{
	int i, j, k;
	double random;
	int step = 0;
	int step_n = 0;
	double aux, aux2;
	int n = msys->n;
	double factor;
	int number_active_links = 0;
	link *list_active_links;

	while(step < steps)
	{
		step_n = 0;
	        srand(msys->seed);
		number_active_links = number_of_active_links_simetric(msys, delta, threshold);
		if(number_active_links == 0)
			break;
		else
		{
			list_active_links = (link *)malloc(sizeof(link) * number_active_links);
			active_links_simetric(msys, delta, threshold, list_active_links);
		}
			
		while(step_n < number_active_links)
		{
			k = rand() % number_active_links;
			i = list_active_links[k].i;
			j = list_active_links[k].j;

			random = (double)rand()/RAND_MAX;

		        if((random < msys->corr[i][j]) && (active_condition(msys, i, j, delta, threshold) == 1))
			{		
				aux = msys->corr[i][j] + delta;
				if(aux >= 1.00)
					aux = 1.00;	
				if(aux < 1.00)
				{
				        factor = (0.5 * delta) / (1.00 - msys->corr[i][j]);
					for(k = 0; k < n; k++)
					{
						if((k!=i) && (k!=j))
						{
							aux2 = (msys->corr[j][k] - msys->corr[i][k]) * factor;
							msys->corr[i][k] += aux2;
							msys->corr[j][k] -= aux2;

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
							aux2 = 0.5 * (msys->corr[i][k] + msys->corr[j][k]);
							msys->corr[i][k] = aux2;
							msys->corr[j][k] = aux2;

							msys->corr[k][i] = msys->corr[i][k];	
							msys->corr[k][j] = msys->corr[j][k];	
						}
					}
				}
				msys->corr[i][j] = aux;
				msys->corr[j][i] = msys->corr[i][j];
			}
			step_n++;
		}

		free(list_active_links);
		step++;

	        msys->seed = rand();
	}

	return 1;
}

int one_step_simetric(mysys *msys, double delta, int i, int j)
{
	int k;
	double aux, aux2;
	int n = msys->n;
	double factor;

	aux = msys->corr[i][j] + delta;
	if(aux >= 1.00)
		aux = 1.00;	
	if(aux < 1.00)
	{
		factor = (0.5 * delta) / (1.00 - msys->corr[i][j]);
		for(k = 0; k < n; k++)
		{
			if((k!=i) && (k!=j))
			{
				aux2 = (msys->corr[j][k] - msys->corr[i][k]) * factor;
				msys->corr[i][k] += aux2;
				msys->corr[j][k] -= aux2;

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
				aux2 = 0.5*(msys->corr[i][k] + msys->corr[j][k]);	
				msys->corr[i][k] = aux2;
				msys->corr[j][k] = aux2;

				msys->corr[k][i] = msys->corr[i][k];	
				msys->corr[k][j] = msys->corr[j][k];	
			}
		}
	}
	
	msys->corr[i][j] = aux;
	msys->corr[j][i] = msys->corr[i][j];

	return 1;
}

int one_step_asimetric(mysys *msys, double delta, int i, int j)
{
	int k;
	double aux = 0.00;
	int n = msys->n;
	double factor;

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
				msys->corr[i][k] = msys->corr[k][i];

				msys->corr[k][i] = msys->corr[i][k];	
			}
		}
	}
	
	msys->corr[i][j] = aux;
	msys->corr[j][i] = msys->corr[i][j];

	return 1;
}
