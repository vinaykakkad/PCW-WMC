#include<iostream>
#include<conio.h>
#include<stdlib.h>

using namespace std;

struct ll
{
    int val;
    ll  *pt,*lc,*rc;
};
typedef struct ll ll;

void inorder(ll *);

ll* l_r(ll *a)
{
    ll b=*(a->lc);
    b.pt=NULL;

    ll br=*(b.rc);

    b.rc=a;
    *(a->pt)=b;

    *(a->lc)=br;
    (br.pt)=a;

    inorder(&b);
    
    exit;
    
    return a;
}
void r_r(ll *n)
{

}

void insert(ll *n,ll* head)
{
    if(n->val>head->val)
    {
        if(head->rc==NULL)
        {
          head->rc=n;
          n->pt=head;
        }
        else    insert(n,head->rc);
    }
    if(head->val>n->val)
    {
        if(head->lc==NULL)
        {
            head->lc=n;
            n->pt=head;
        }
        else    insert(n,head->lc);
    }
}

void arr_to_bst(int *arr,int n,ll *head)
{
    for(int i=2;i<n+1;i++)
    {
        ll *k=(ll *)malloc(sizeof(ll));
        k->pt=NULL;k->lc=NULL;k->rc=NULL;
        k->val=*(arr+i);

        insert(k,head);
    }
}
void inorder(ll *root)
{
    if(root!=NULL)
    {
        cout<<root->val<<" ";
        inorder(root->lc);
        inorder(root->rc);
    }
}

int main()
{
    int n,*arr;

    cout<<"Enter the size of data: ";
    cin>>n;

    arr=(int*)malloc((n+1)*sizeof(int));

    cout<<"Enter the elements: ";
    for(int i=0;i<n;i++)
    {
        cin>>*(arr+i+1);
    }

    ll *head=(ll *)malloc(sizeof(ll));
    head->val=*(arr+1);
    head->pt=NULL;
    head->lc=NULL;
    head->rc=NULL;
    
    arr_to_bst(arr,n,head);
    //getch();
    inorder(head);
    //getch();
    head =l_r(head);
    //getch();
    cout<<head->val;
    getch();
    inorder(head);

    return 0;
}