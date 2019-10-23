#include "active_links.h"

int active_condition(mysys *msys, int i, int j, double threshold)
{
        if(msys->a[i][j] == 1)
        {
		if((msys->corr[i][j] > threshold + EPSILON) && (msys->corr[i][j] < (1.00 - EPSILON)))
			return 1;
        }

        return 0;
}

int number_of_active_links(mysys *msys, double threshold)
{
	int i,j;
	int n = msys->n;
	int number_active_links = 0;

        for(i = 0; i < n; i++)
	{
		for(j = 0; j < n; j++)
		{
			if(active_condition(msys, i, j, threshold))
				number_active_links++;
		}
	}
	return number_active_links;
}

int number_of_active_links_simetric(mysys *msys, double threshold)
{
	int i,j;
	int n = msys->n;
	int number_active_links = 0;

        for(i = 0; i < n; i++)
	{
		for(j = i+1; j < n; j++)
		{
			if(active_condition(msys, i, j, threshold))
				number_active_links++;
		}
	}
	return number_active_links;
}

int active_links(mysys *msys, double threshold, link *list_active_links)
{
	int i, j, k;
	int n = msys->n;

	k = 0;	
        for(i = 0; i < n; i++)
	{
		for(j = 0; j < n; j++)
		{
			if(active_condition(msys, i, j, threshold))
			{
				list_active_links[k].i = i;
				list_active_links[k].j = j;
				k++;
			}
		}
	}
		
	return 1;
}

int active_links_simetric(mysys *msys, double threshold, link *list_active_links)
{
	int i, j, k;
	int n = msys->n;

	k = 0;	
        for(i = 0; i < n; i++)
	{
		for(j = i+1; j < n; j++)
		{
			if(active_condition(msys, i, j, threshold))
			{
				list_active_links[k].i = i;
				list_active_links[k].j = j;
				k++;
			}
		}
	}
		
	return 1;
}

