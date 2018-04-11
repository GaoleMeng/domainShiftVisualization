// compiler with g++ -std=c++17 -lboost_system  generate_first.cpp -o generate_first

#include <iostream>
#include <vector>
#include <string>
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

using namespace std;
namespace fs = boost::filesystem;

path input_dir_1("/scratch/si699w18_fluxm/gaole/aminer_papers_0");
path input_dir_2("/scratch/si699w18_fluxm/gaole/aminer_papers_1");
path input_dir_3("/scratch/si699w18_fluxm/gaole/aminer_papers_2");
vector<path> dir_list = {input_dir_1, input_dir_2, input_dir_3};

int main() {

    for (path dir: dir_list) {

        directory_iterator end_itr;

        for (directory_iterator itr(dir); it != end_itr; ++it)
        {
            string current_file = itr->path().string();
            cout << current_file << endl;
        }
    }
}





