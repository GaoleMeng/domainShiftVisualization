// compiler with 
// g++ -std=c++17  generate_ranking.cpp -o generate_ranking -lstdc++fs -pthread
// the second layer bfs generator, take the output of last layer and output the next layer

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <regex>
#include <unordered_set>
#include <iostream>
#include <unordered_map>
#include <experimental/filesystem>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;
using namespace rapidjson;


// Configuration: all the aminer input files, changable directory (not files!)
string input_dir_1 = "/scratch/si699w18_fluxm/gaole/aminer_papers_0";
string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";

// Configuration: input file, change to the first layer output file
string input_lastlayer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";


string first_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
string second_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_second.txt";
string third_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_third.txt";

vector<string> layer_file_list = {first_layer, second_layer, third_layer};

// Configuration: changable second layer output representation file 
// string output_file = "/scratch/si699w18_fluxm/gaole/cpp_largevis_second.txt";
string output_file = "/scratch/si699w18_fluxm/gaole/ranking.txt";

unordered_set<string> pool;


vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};
unordered_set<string> string_pool;
unordered_map<string, int> counter;

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
regex year("\"year\": .*?,");

string id_start = "\"id\": ";
string venue_start = "\"venue\": ";
string year_start = "\"year\": ";
string references_start = "\"references\": ";



void read_and_parse(int indices) {
    
    string filename = filedir_list[indices];
    
    ifstream input(filename.c_str());
    string line = "";
    size_t found;
    string id_string = "";
    string venue_string = "";
    string year_string = "";
    
    
    while(getline(input, line)) {
        // cout << line << endl;
        found = line.find(id_start);
        // cout << line << endl;
        smatch venue_extract;
        if (regex_search(line, venue_extract, venue)) {
            venue_string = string(venue_extract[0]).substr(10, venue_extract[0].length() - 11);
                // cout << "finish" << "\n";
            if (!string_pool.count(venue_string)) continue;
            output_lock.lock();
            counter[venue_string] += 1; 
            output_lock.unlock(); 
        }
    }
}

void create_stringpool(int i) {
    string line = "";
    unordered_set<string> prev_strings;
    cout << layer_file_list[i] << endl;
    string_pool_stream.open(layer_file_list[i]);

    while(getline(string_pool_stream, line)) {

        string segment = "";
        istringstream segment_ss(line);

        int counter = 0;
        // cout << line << endl;
        while(getline(segment_ss, segment, '\t')) {
            if (counter == 0) {
                counter += 1;
                prev_strings.insert(segment);
                continue;
            }
            else if (counter == 1) {
                string_pool.insert(segment);
                counter += 1;
                break;
            }
        }   
    }
    string_pool.insert("SIGIR Forum");
    string_pool.insert("SIGIR");
    cout << string_pool.size() << endl;
    string_pool_stream.close();
}


void dump_file(unordered_map<string, int> mapping_file) {
    for (const auto& tmp: mapping_file) {
        output << tmp.first << " " << tmp.second << "\n";
    }
}



int main() {
    vector<thread> thread_list;
    output.open(output_file);
    string_pool_stream.open(input_lastlayer);

    for (int i = 1; i < 3; i++) {
        create_stringpool(i);
    }

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
    cout << counter.size() << endl;
    dump_file(counter);
    output.close();
}

