#include "active_links.h"

int active_condition(mysys *msys, int i, int j, double delta, double threshold)
{
        if(msys->a[i][j] == 1)
        {
		if((msys->corr[i][j] > threshold) && (msys->corr[i][j] < (1.00 - delta)))
			return 1;
        }

        return 0;
}

int number_of_active_links(mysys *msys, double delta, double threshold)
{
	int i,j;
	int n = msys->n;
	int number_active_links = 0;

        for(i = 0; i < n; i++)
	{
		for(j = 0; j < n; j++)
		{
			if(active_condition(msys, i, j, delta, threshold))
				number_active_links++;
		}
	}
	return number_active_links;
}


int active_links(mysys *msys, double delta, double threshold, link *list_active_links)
{
	int i, j, k;
	int n = msys->n;

	k = 0;	
        for(i = 0; i < n; i++)
	{
		for(j = 0; j < n; j++)
		{
			if(active_condition(msys, i, j, delta, threshold))
			{
				list_active_links[k].i = i;
				list_active_links[k].j = j;
				k++;
			}
		}
	}
		
	return 1;
}

