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
#include <experimental/filesystem>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;
using namespace rapidjson;

// string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
// string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
// string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
string input_dir_1 = "/home/gaole/tmprepo/largeScaleGraph/cpp/first_layer_extraction";

string output_file = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
vector<string> dir_list = {input_dir_1};
string lastfix = ".txt";

static mutex output_lock;
mutex parselock;
ofstream output;
string tmp = "";
vector<string> filedir_list;
regex id("\"id\": \".*?\"");
regex venue("\"venue\": \".*?\"");
regex references("\"references\": \\[.*\\]");
regex single_id("\".{24}\"");
regex year("\"year\": .*?,");

string references_start = "\"references\"";


void read_and_parse(int indices) {
    
    string filename = filedir_list[indices];
    
    ifstream input(filename.c_str());
    string line = "";
    
    while(getline(input, line)) {
        smatch id_extract;
        if (regex_search(line, id_extract, id)){
            smatch venue_extract;
            if (regex_search(line, venue_extract, venue)) {
                smatch year_extract;

                if (regex_search(line, year_extract, year)) {
                    string reference_string = "";
                    // if (venue_extract[0] != "\"venue\": \"SIGIR\"" && venue_extract[0] != "\"venue\": \"SIGIR Forum\"") {
                    //     continue;
                    // }
                    
                    string id_string = string(id_extract[0]).substr(7, 24);
                    string refer_string = "";
                    string year_string = string(year_extract[0]).substr(8, string(year_extract[0]).length() - 9);

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
                    output << id_string + "\tSIGIR\t" + year_string + "\t" + refer_string << "\n";
                    output_lock.unlock();
                }
            }
        }
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
        thread_list.push_back(thread(read_and_parse, i));
        // read_and_parse(i);
    }

    for (auto& th: thread_list) th.join();
    output.close();
}





