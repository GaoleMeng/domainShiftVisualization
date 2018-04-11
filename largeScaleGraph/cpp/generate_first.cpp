// compiler with 
// g++ -std=c++17  generate_first.cpp -o generate_first -lstdc++fs -pthread
// the first round of the multithread version of the processing file

#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <experimental/filesystem>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;


string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};
string lastfix = ".txt";


void read_and_parse(const char* filename) {
    // cout << string(filename) << endl;
    ifstream file_c(filename);
    // cout << "f" << endl;
    string line = "";
    while(getline(file_c, line)) {
        cout << line << endl;
        break;
    }
}


int main() {
    vector<thread> thread_list;

    for (string dir: dir_list) {
        for (auto & p : fs::directory_iterator(dir)) {
            if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
                thread_list.push_back(thread(read_and_parse, 
                    p.path().c_str()));
            }
        }
    }

    for (auto& th: thread_list) th.join();
}





