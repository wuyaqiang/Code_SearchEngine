import time
from code_search.tokenize import lex_analysis

def all_substring(code_string):
    token_list = code_string.split(" ")
    length = len(token_list)
    sub_string_list = ["_".join(token_list[i:j + 1]) for i in range(length) for j in range(i,length)]
    return " ".join(sub_string_list)

code_text = '''
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
'''
lex_text = lex_analysis(code_text)
print(lex_text)
time1 = time.time()
all_substring = all_substrings_1(lex_text)
print(time.time()-time1)
print(len(all_substring))
print(all_substring[:100])



