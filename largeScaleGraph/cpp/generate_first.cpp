// compiler with 
// g++ -std=c++17  generate_first.cpp -o generate_first -lstdc++fs -pthread
// the first round of the multithread version of the processing file

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <experimental/filesystem>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;
using namespace rapidjson;

string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
string output_file = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};
string lastfix = ".txt";

mutex output_lock;
mutex parselock;
ofstream output;


void read_and_parse(const char* filename) {
    // cout << filename << "\n";
    ifstream input(filename);
    string line = "";
    output_lock.lock();
    while(getline(input, line)) {
        
        // Document d;
        // // parselock.lock();
        // d.Parse(line.c_str());
        // // parselock.unlock();
        // if (!d.HasMember("id")) {
        //     output_lock.unlock();
        //     continue;
        // }
        // if (!d.HasMember("venue")) {
        //     output_lock.unlock();
        //     continue;
        // }
        // Value& s = d["venue"];
        // // if (s.GetString() != "SIGIR") continue;
        // string reference_string = "";
        // if (d.HasMember("references")) {
        //     Value& a = d["references"];
        //     for (auto& v : a.GetArray()) {
        //         reference_string.append(string(v.GetString()) + " ");
        //     }
        // }

        
        // cout << string(d["id"].GetString()) + " SIGIR " + reference_string << "\n";
        cout << "ddd" << endl;
        break;
    }
    output_lock.unlock();
}


int main() {
    vector<thread> thread_list;
    output.open(output_file);
    // cout << "ddd" << endl;
    for (string dir: dir_list) {
        for (auto & p : fs::directory_iterator(dir)) {
            if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
                // cout << p.path().filename() << endl;
                thread_list.push_back(thread(read_and_parse, 
                    p.path().c_str()));
            }
        }
    }
    // cout << thread_list.size() << endl;
    for (auto& th: thread_list) th.join();
    output.close();
}





