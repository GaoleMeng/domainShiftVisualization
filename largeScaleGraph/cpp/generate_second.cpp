// compiler with 
// g++ -std=c++17  generate_first.cpp -o generate_first -lstdc++fs -pthread
// the first round of the multithread version of the processing file

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <regex>
#include <unordered_set>
#include <iostream>
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
string input_lastlayer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
string output_file = "/scratch/si699w18_fluxm/gaole/cpp_largevis_second.txt";

vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};
unordered_set<string> string_pool;

string lastfix = ".txt";

static mutex output_lock;
mutex parselock;
ofstream output;
ifstream string_pool_stream;


string tmp = "";
vector<string> filedir_list;
regex id("\"id\": \".*?\"");
regex venue("\"venue\": \".*?\"");
regex references("\"references\": \\[.*?\\]");
regex single_id("\".{24}\"");

void read_and_parse(int indices) {
    
    string filename = filedir_list[indices];
    
    ifstream input(filename.c_str());
    string line = "";
    
    while(getline(input, line)) {
        smatch id_extract;
        if (regex_search(line, id_extract, id)){
            smatch venue_extract;
            if (regex_search(line, venue_extract, venue)) {
                string id_string = string(id_extract[0]).substr(7, 24);
                // if (!string_pool.count(id_string)) continue;

                string reference_string =  venue_extract[0].substr(10, venue_extract[0].length() - 11);
                
                string refer_string = "";
                smatch references_extract;
                if (regex_search(line, references_extract, references)) {
                    string whole_string = references_extract[0];
                    int start = 16;
                    while (start < whole_string.length()) {
                        refer_string.append(whole_string.substr(start, 24) + " ");
                        start += 28;
                    }
                }
                output_lock.lock();
                cout << id_string + " " + reference_string + " " + refer_string << "\n";
                output_lock.unlock();
            }
        }

        break;
    }
}

void create_stringpool() {
    string line = "";
    unordered_set<string> prev_strings;

    while(getline(string_pool_stream, line)) {
        istringstream ss(line);
        string word;
        ss >> word;
        prev_strings.insert(word);
        ss >> word;

        while (ss >> word) {
            string_pool.insert(word);
        }
    }

    for (const auto& elem: prev_strings) {
        if (string_pool.count(elem)) {
            string_pool.erase(elem);
        }
    }
    cout << string_pool.size() << endl;
}



int main() {
    vector<thread> thread_list;
    output.open(output_file);
    string_pool_stream.open(input_lastlayer);
    create_stringpool();

    for (string dir: dir_list) {
        for (auto & p : fs::directory_iterator(dir)) {
            if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
                filedir_list.push_back(p.path());                
            }
        }
    }

    for (int i = 0; i < filedir_list.size(); i++) {
        thread_list.push_back(thread(read_and_parse, i));
        // read_and_parse(i);
    }

    for (auto& th: thread_list) th.join();
    output.close();
}





