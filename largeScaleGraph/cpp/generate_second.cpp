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

string id_start = "\"id\": ";
string venue_start = "\"venue\": ";
string year_start = "\"year\": ";
string references_start = "\"references\"";

void read_and_parse(int indices) {
    
    string filename = filedir_list[indices];
    
    ifstream input(filename.c_str());
    string line = "";
    size_t found;
    string id_string = "";
    string venue_string = "";
    string year_string = "";
    string refer_string = "";
    
    while(getline(input, line)) {
        // cout << line << endl;
        found = line.find(id_start);
        if (found != std::string::npos) {
            id_string = line.substr(found + 7, 24);
            if (!string_pool.count(id_string)) continue;

            smatch venue_extract;
            if (regex_search(line, venue_extract, venue)) {
                smatch year_extract;
                if (regex_search(line, year_extract, venue)) {
                    venue_string = string(venue_extract[0]).substr(10, venue_extract[0].length() - 11);
                    
                    size_t found = line.find(references_start);
                    if (found != std::string::npos) {
                        int start = 16 + found;
                        while (true) {
                            refer_string.append(line.substr(start, 24) + " ");
                            if (line[start + 25] == ']') break;
                            start += 28;
                        }
                    }

                    output_lock.lock();
                    cout << id_string + "\t" + venue_string + "\t" + year_string + "\t" + refer_string << "\n";
                    output_lock.unlock();
                }
            }
        }
    }
}

// "venue": "Saudi journal of anaesthesia"

void create_stringpool() {
    string line = "";
    unordered_set<string> prev_strings;

    while(getline(string_pool_stream, line)) {

        string segment = "";
        istringstream segment_ss(line);

        int counter = 0;
        while(getline(segment_ss, segment, '\t')) {
            if (counter == 0) {
                counter += 1;
                prev_strings.insert(segment);
                continue;
            }
            else if (counter == 1) {
                counter += 1;
                continue;
            }
            else if (counter == 2) {
                counter += 1;
                continue;
            }
            else {
                string_pool.insert(segment);
            }
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





