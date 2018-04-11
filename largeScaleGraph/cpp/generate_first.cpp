// compiler with 
// g++ -std=c++17  generate_first.cpp -o generate_first -lstdc++fs -pthread
// the first round of the multithread version of the processing file

#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <experimental/filesystem>
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;


string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};

void read_and_parse(const char* filename) {
    cout << filename << endl;
}



int main() {
    vector<thread> thread_list;

    for (string dir: dir_list) {
        for (auto & p : fs::directory_iterator(dir)) {
            // ifstream ifs(p);
            thread_list.push_back(thread(read_and_parse, 
                p.path().c_str()));
        }
    }

    for (auto& th: thread_list) th.join();
}





