#include <iostream>
using namespace std;

int main()
{
	long n, m;
	cin >;>; n >;>; m;
	long i = 1;
	m--;
	while (m!=0)
	{
		long num = 0;
		long start = i, end = i + 1;
		while (start<=n)
		{
			num += min(n + 1, end) - start;
			start *= 10;
			end *= 10;
		}
		if (num >; m)
		{
			i *= 10;
			m--;
		}
		else
		{
			m -= num;
			i++;
		}
	}
	cout << i << endl;
	return 0;
}