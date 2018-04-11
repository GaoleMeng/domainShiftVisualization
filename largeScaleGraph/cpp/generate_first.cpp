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

static mutex output_lock;
mutex parselock;
ofstream output;
string tmp = "";
vector<string> filedir_list;


void read_and_parse(int indices) {
    // cout << filename << "\n";
    
    string filename = filedir_list[indices];
    
    ifstream input(filename.c_str());
    string line = "";
    
    while(getline(input, line)) {
        // parselock.lock();
        Document d;
        d.Parse(line.c_str());
        if (!d.HasMember("id")) {
            // parselock.unlock();
            continue;
        }
        if (!d.HasMember("venue")) {
            // parselock.unlock();
            continue;
        }
        Value& s = d["venue"];

        string reference_string = "";
        if (d.HasMember("references")) {
            Value& a = d["references"];
            for (auto& v : a.GetArray()) {
                reference_string.append(string(v.GetString()) + " ");
            }
        }

        // parselock.unlock();
        // output_lock.lock();
        output << string(d["id"].GetString()) + " SIGIR " + reference_string << "\n";
        // output_lock.unlock();
        break;
    }
}


int main() {
    vector<thread> thread_list;
    output.open(output_file);

    for (string dir: dir_list) {
        for (auto & p : fs::directory_iterator(dir)) {
            if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
                filedir_list.push_back(p.path());                
            }
        }
    }

    for (int i = 0; i < filedir_list.size(); i++) {
        // thread_list.push_back(thread(read_and_parse, i));
        read_and_parse(i);
    }

    for (auto& th: thread_list) th.join();
    cout << tmp;
    output.close();
}





