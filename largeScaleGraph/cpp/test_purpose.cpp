#include <iostream>
#include <vector>

using namespace std;
vector<string> tmp;



void test() {
    tmp.emplace_back("0.0.0.0");
}


void test2() {
    cout << tmp.at(0) << endl;
}




int main() {
    test();
    test2();
}