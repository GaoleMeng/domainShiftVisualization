// compiler with g++ -std=c++17 -lboost_system  generate_first.cpp -o generate_first

#include <iostream>
#include <vector>
#include <string>
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

using namespace std;
namespace fs = boost::filesystem;

string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};

int main() {

    for (string dir: dir_list) {

        std::vector<directory_entry> v;
        for(auto& entry : boost::make_iterator_range(directory_iterator(dir), {})) {
            std::cout << entry << "\n";
        }
    }
}





