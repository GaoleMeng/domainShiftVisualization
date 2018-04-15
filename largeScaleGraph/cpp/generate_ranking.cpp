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
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <experimental/filesystem>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;
using namespace rapidjson;

string input_dir_1 = "/scratch/si699w18_fluxm/gaole/lines_belong_toconf.txt";
// string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
// string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
// string first_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
// string second_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_second.txt";
// string third_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_third.txt";
// string index_file_output = "/scratch/si699w18_fluxm/gaole/ranking.txt";
string output_file = "/scratch/si699w18_fluxm/gaole/ranking.txt";

vector<string> dir_list = {input_dir_1};
// vector<string> layer_file_list = {first_layer, second_layer};
unordered_set<string> string_pool;
unordered_map<string, int> index_map;
unordered_map<string, string> year_map;

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


bool pairCompare(const std::pair<string, int>& firstElem, const std::pair<string, int>& secondElem) {
  return firstElem.second < secondElem.second;

}



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
        if (found != std::string::npos) {
            id_string = line.substr(found + 7, 24);
            // if (!string_pool.count(id_string)) continue;
            smatch venue_extract;
            if (regex_search(line, venue_extract, venue)) {

                string refer_string = "";
                smatch year_extract;
                if (regex_search(line, year_extract, year)) {

                    venue_string = string(venue_extract[0]).substr(10, venue_extract[0].length() - 11);
                    index_map[venue_string] += 1;
                    // if (!string_pool.count(venue_string)) continue;
                    // output_lock.lock();
                    // output << line << "\n";
                    // output_lock.unlock();
                }
            }
        }
    }


}

void dump_file(unordered_map<string, int> mapping_file) {
    ofstream oss(output_file);
    vector<pair<string, int> > tmp;

    for (const auto& tmpp: mapping_file) {
        tmp.push_back({tmpp.first, tmpp.second});
    }

    sort(tmp.begin(), tmp.end(), pairCompare);
    for (auto& tt: tmp) {
        oss << tt.first << " " << tt.second << "\n";
    }

    oss.close();
}


// "venue": "Saudi journal of anaesthesia"

// void create_stringpool(int i) {
//     string line = "";
//     unordered_set<string> prev_strings;
//     cout << layer_file_list[i] << endl;
//     string_pool_stream.open(layer_file_list[i]);

//     while(getline(string_pool_stream, line)) {

//         string segment = "";
//         istringstream segment_ss(line);

//         int counter = 0;
//         // cout << line << endl;
//         while(getline(segment_ss, segment, '\t')) {
//             if (counter == 0) {
//                 counter += 1;
//                 prev_strings.insert(segment);
//                 continue;
//             }
//             else if (counter == 1) {
//                 string_pool.insert(segment);
//                 counter += 1;
//                 break;
//             }
//         }   
//     }
//     string_pool.insert("SIGIR Forum");
//     cout << string_pool.size() << endl;
//     string_pool_stream.close();


// }



int main() {
    vector<thread> thread_list;
    // output.open(output_file);


    // for (int i = 0; i < layer_file_list.size(); i++) {
    //     create_stringpool(i);
    // }


    // for (string dir: dir_list) {
    //     // for (auto & p : fs::directory_iterator(dir)) {
    //     //     if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
    //     //         filedir_list.push_back(p.path());                
    //     //     }
    //     // }

    // }

    filedir_list.push_back(input_dir_1);

    for (int i = 0; i < filedir_list.size(); i++) {
        thread_list.push_back(thread(read_and_parse, i));
        // read_and_parse(i);
    }

    for (auto& th: thread_list) th.join();
    // output.close();

    dump_file(index_map);
}

