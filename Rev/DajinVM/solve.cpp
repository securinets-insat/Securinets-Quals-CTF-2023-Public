#include <bits/stdc++.h> 

using namespace std;

const int N = 3 * 1000 * 1000 + 13;

/* 
	Author : IronByte
	Securinets Quals 2023
*/
vector<int> lst(N);
vector<int> num(N);

void sieve() {
    for (int i = 0; i < N; ++i)
        lst[i] = i;
    
    for (int i = 2; i < N; ++i) {
        if (lst[i] != i) {
            lst[i] = i / lst[i];
            continue;
        }
        for (long long j = i * 1ll * i; j < N; j += i)
            lst[j] = std::min(lst[j], i);
    }

    int cur = 0;
    for (int i = 2; i < N; ++i) {
        if (lst[i] == i)
            num[i] = ++cur;
    }
}

int main() {
    int n = 32;
    vector<int> t = { 7, 7, 7, 7, 7, 13, 17, 17, 17, 17, 24, 24, 24, 24, 25, 25, 25, 25, 25, 26, 27, 27, 33, 48,
                            48, 48, 48, 49, 49, 49, 49, 49, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 52, 54, 54,
                            65, 97, 97, 99, 100, 101, 101, 101, 101, 102, 102, 509, 509, 547, 547, 547, 547 };

    vector<int> cnt(N, 0);
    for (int i = 0; i < 2 * n; ++i) {
        int x = t[i];
        ++cnt[x];
    }

    sieve();

    vector<int> res;
    for (int i = N - 1; i >= 0; --i) {
        while (cnt[i] > 0) {
            if (lst[i] == i) {
                --cnt[num[i]];
                res.push_back(num[i]);
            } else {
                --cnt[lst[i]];
                res.push_back(i);
            }
            --cnt[i];
        }
    }

    sort(res.begin(), res.end());
    for (auto it : res)
        cout << char(it);

    return 0;
}
