#include <iostream>
#include <vector>

using namespace std;
vector<string> tmp;

int main() {
    tmp.emplace_back("0.0.0.0");
    cout << tmp.at(0) << endl;


}