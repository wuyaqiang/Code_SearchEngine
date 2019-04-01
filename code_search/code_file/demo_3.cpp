using namespace std;

int main(){
    vector<int>;v(1000,1);
    int x;
    while(cin>;>;x){
        for (int i=2;i<1000;i++){
            for(int j=2;i*j<1000;j++){
                if(v[i]){
                    v[i*j]=0;
                }
            }
        }
    }
    int res=0;
    for (int i=2;i<=x/2;i++){
        if(v[i]&amp;&amp;v[x-i]){
            res++;
        }
    }
    cout<<res<<endl;
}