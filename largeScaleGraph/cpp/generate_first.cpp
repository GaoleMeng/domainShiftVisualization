// compiler with g++ -std=c++17 -lboost_system  generate_first.cpp -o generate_first

#include <iostream>
#include <vector>
#include <string>
#include <boost/filesystem.hpp>

using namespace std;
namespace fs = boost::filesystem;

string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};

int main() {

    // for (string dir: dir_list) {
    cout << input_dir_1 << endl;
        // for (auto& p: fs::directory_iterator(input_dir_1)) {
        //     cout << p << endl;
        // }
    // }
}





