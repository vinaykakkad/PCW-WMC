#include<bits/stdc++.h>
using namespace std;

#define ll long long int
#define ld long double
#define PI 3.141592653589793238462643383279502884197169399375105820974944592307816406286

int main()
{
    ll t,n;
    cin>>t;
    ld a,ans;
    for(ll i=0;i<t;i++)
    {
        cin>>n;
        a=(ld)(PI)/(ld)(2*n);
        ans=(ld)1/(ld)tan(a);
        cout<<setprecision(20)<<ans<<"\n";
    }
    
    
    
}