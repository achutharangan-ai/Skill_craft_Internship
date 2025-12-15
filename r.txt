#include<stdio.h>
#include<limits.h>
void main()
{
	int n,i,j;
	scanf("%d",&n);
	int dist[n],g[n][n],vis[n];
	for(i=0;i<n;i++)
		{
			for(j=0;j<n;j++)
				{
					scanf("%d",&g[i][j]);
				}
		}
	for(i=0;i<n;i++)
		{
			dist[i]=INT_MAX;
			vis[i]=0;
		}
	dist[0]=0;
	for(i=0;i<n-1;i++)
		{
			int min=INT_MAX,u;
			for(j=0;j<n;j++)
				{
					if(!vis[j]&&dist[j]<min)
					{
						min=dist[j];
						u=j;
					}
				}
	vis[u]=1;
	for(j=0;j<n;j++)
		{
			if(!vis[j]&&g[u][j]&&dist[u]+g[u][j]<dist[j])
			{
				dist[j]=dist[u]+g[u][j];
			}
		}
		}
	printf("Vertex \t\t Distance from Source\n");
	for(int i=0;i<n;i++)
		{
			
			printf("%d \t\t\t\t %d\n",i,dist[i]);
		}
}
dijikstra
#include <stdio.h>

int main() {
    int N, W;
    scanf("%d %d", &N, &W);

    int val[1001], wt[1001], dp[1001] = {0};

    for(int i = 0; i < N; i++)
        scanf("%d", &val[i]);

    for(int i = 0; i < N; i++)
        scanf("%d", &wt[i]);

    for(int i = 0; i < N; i++) {
        for(int w = W; w >= wt[i]; w--) {
            if(dp[w] < dp[w - wt[i]] + val[i])
                dp[w] = dp[w - wt[i]] + val[i];
        }
    }

    printf("%d", dp[W]);
    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

int minDist(int *d, bool *v, int n) {
	int m = INT_MAX, k = -1;
	for (int i = 0; i < n; i++)
		if (!v[i] && d[i] <= m) m = d[i], k = i;
	return k;
}

int main() {
	int n; scanf("%d", &n);
	int **g = malloc(n * sizeof(int*));
	for (int i = 0; i < n; i++) {
		g[i] = malloc(n * sizeof(int));
		for (int j = 0; j < n; j++) scanf("%d", &g[i][j]);
	}

	int *d = malloc(n * sizeof(int));
	bool *v = calloc(n, sizeof(bool));
	for (int i = 0; i < n; i++) d[i] = INT_MAX;
	d[0] = 0;

	for (int c = 0; c < n - 1; c++) {
		int u = minDist(d, v, n);
		if (u < 0) break;
		v[u] = true;
		for (int x = 0; x < n; x++)
			if (!v[x] && g[u][x] && d[u] + g[u][x] < d[x])
				d[x] = d[u] + g[u][x];
	}

	printf("Vertex \t\t Distance from Source\n");
	for (int i = 0; i < n; i++)
		printf("%d \t\t\t\t %d\n", i, d[i]);

	free(d);
	free(v);
	for (int i = 0; i < n; i++) free(g[i]);
	free(g);
}
dijkstra 36 line version
#include <stdio.h>
#include <limits.h>

int n, cost[20][20], dp[1<<16][20];

int tsp(int mask, int pos){
	if(mask == (1<<n)-1)
		return cost[pos][0] == -1 ? INT_MAX : cost[pos][0];

	if(dp[mask][pos] != -1) return dp[mask][pos];

	int ans = INT_MAX;
	for(int c=0;c<n;c++)
		if(!(mask&(1<<c)) && cost[pos][c]!=-1){
			int t = tsp(mask|(1<<c), c);
			if(t!=INT_MAX && cost[pos][c]+t < ans)
				ans = cost[pos][c] + t;
		}
	return dp[mask][pos] = ans;
}

int main(){
	scanf("%d",&n);
	for(int i=0;i<n;i++)
		for(int j=0;j<n;j++)
			scanf("%d",&cost[i][j]);

	for(int i=0;i<(1<<n);i++)
		for(int j=0;j<n;j++)
			dp[i][j] = -1;

	int r = tsp(1,0);
	printf("%d\n", r==INT_MAX ? -1 : r);
}
28 line code tsp
#include <stdio.h>

int main(){
	int n,e; scanf("%d%d",&n,&e);

	int g[n][n], res[n], avail[n];
	for(int i=0;i<n;i++){
		for(int j=0;j<n;j++) g[i][j]=0;
		res[i]=-1;
	}

	while(e--){
		int a,b; scanf("%d%d",&a,&b);
		g[a][b]=g[b][a]=1;
	}

	res[0]=0;

	for(int u=1;u<n;u++){
		for(int i=0;i<n;i++) avail[i]=1;
		for(int i=0;i<n;i++)
			if(g[u][i] && res[i]!=-1) avail[res[i]]=0;
		for(int c=0;c<n;c++)
			if(avail[c]){ res[u]=c; break; }
	}

	int mx=0;
	for(int i=0;i<n;i++) if(res[i]>mx) mx=res[i];

	printf("%d\n",mx+1);
}
24 line graph coloring
#include <stdio.h>
#include <stdbool.h>

int cnt=0;

bool safe(int b[],int r,int c,int N){
	for(int i=0;i<r;i++){
		if(b[i]==c||(r-i==c-b[i])||(r-i==b[i]-c)) return false;
	}
	return true;
}

void print(int b[],int N){
	for(int i=0;i<N;i++){
		for(int j=0;j<N;j++)
			printf("%s\t",b[i]==j?"Q":"*");
		printf("\n");
	}
}

int solve(int b[],int N,int r){
	if(r==N){
		cnt++;
		printf("Solution #%d:\n",cnt);
		print(b,N);
		return 1;
	}
	int s=0;
	for(int c=0;c<N;c++){
		if(safe(b,r,c,N)){
			b[r]=c;
			s+=solve(b,N,r+1);
			b[r]=-1;
		}
	}
	return s;
}

int main(){
	int N;
	scanf("%d",&N);
	int b[N];
	for(int i=0;i<N;i++) b[i]=-1;
	printf("Total solutions:%d\n",solve(b,N,0));
}
38 line n queen
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int N, bestCost, *best;

int LB(int **c,int *a,int k){
	int lb=0;
	for(int i=0;i<k;i++) lb+=c[i][a[i]];
	for(int i=k;i<N;i++){
		int m=INT_MAX;
		for(int j=0;j<N;j++){
			int used=0;
			for(int x=0;x<k;x++) if(a[x]==j) used=1;
			if(!used && c[i][j]<m) m=c[i][j];
		}
		lb+=m;
	}
	return lb;
}
void BnB(int **c,int *a,int k,int cost){
	if(k==N){
		if(cost<bestCost){
			bestCost=cost;
			for(int i=0;i<N;i++) best[i]=a[i];
		}
		return;
	}
	if(LB(c,a,k)>=bestCost) return;

	for(int j=0;j<N;j++){
		int used=0;
		for(int x=0;x<k;x++) if(a[x]==j) used=1;
		if(!used){
			a[k]=j;
			BnB(c,a,k+1,cost+c[k][j]);
			a[k]=-1;
		}
	}
}
int main(){
	scanf("%d",&N);
	int **c = (int**)malloc(N*sizeof(int*));
	for(int i=0;i<N;i++){
		c[i] = (int*)malloc(N*sizeof(int));
		for(int j=0;j<N;j++) scanf("%d",&c[i][j]);
	}

	best = (int*)malloc(N*sizeof(int));
	int *a = (int*)malloc(N*sizeof(int));
	for(int i=0;i<N;i++) a[i]=best[i]=-1;

	bestCost=INT_MAX;
	BnB(c,a,0,0);

	for(int i=0;i<N;i++) printf("Worker %c - Job %d\n",'A'+i,best[i]);
	printf("Optimal Cost:%d\n",bestCost);
	for(int i=0;i<N;i++) free(c[i]);
	free(c); free(a); free(best);
}
job assignment 55 lines
