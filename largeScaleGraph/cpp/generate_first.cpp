// compiler with 
// g++ -std=c++11 -pedantic -lboost_system -lboost_filesystem  generate_first.cpp -o generate_first

#include <iostream>
#include <vector>
#include <string>
#include <experimental/filesystem>
// #include <boost/range/iterator_range.hpp>
namespace fs = std::filesystem;
using namespace std;
// using namespace boost::filesystem;

string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};

int main() {

    for (auto & p : fs::directory_iterator(input_dir_1))
        std::cout << p << std::endl;
}





