#include<bits/stdc++.h>
using namespace std;

#define ll long long int
#define ld long double

int main()
{
    ll a,b,c,d,t;
    cin>>t;
    for(ll i=0;i<t;i++)
    {
        cin>>a>>b>>c>>d;
        
        if(a<=b)    cout<<b<<"\n";
        else
        {
            if(d>=c)    cout<<-1<<"\n";
            else
            {
                cout<<setprecision(20)<<b+(ceil((ld)(a-b)/(c-d)))*c<<"\n";
            }
        }
    }
    
    
    
}