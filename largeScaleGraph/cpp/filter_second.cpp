// compiler with 
// g++ -std=c++17  filter_second.cpp -o filter_second -lstdc++fs -pthread
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

// some hyper parameter
int minimum_size = 10;
double ratio_thres = 0.1;



// Configuration: the output file of "filter_first"
string lines_belong_toconf = "/scratch/si699w18_fluxm/gaole/lines_belong_toconf_two.txt";

// Configuration: the three layer output of BFS 
string first_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
string second_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_second.txt";
string third_layer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_third.txt";

// Configuration: the output of this layer of filter
string output_file = "/scratch/si699w18_fluxm/gaole/lines_belong_toconf_smaller.txt";


vector<string> dir_list = {lines_belong_toconf};

vector<string> layer_file_list = {first_layer, second_layer, third_layer};
unordered_set<string> string_pool;
unordered_map<string, int> index_map;
unordered_map<string, int> bfs_index_map;
unordered_set<string> final_conf;
unordered_map<string, string> year_map;


// string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
// string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
// string index_file_output = "/scratch/si699w18_fluxm/gaole/ranking.txt";
// string output_file = "/scratch/si699w18_fluxm/gaole/partial_ranking.txt";

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


// count the total number of papers in each conference
// store result in index_map (conf_name => count)
void count_papers_in_each_conf(int indices) {
    
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
                }
            }
        }
    }
}


// void dump_file(unordered_map<string, int> mapping_file) {
//     ofstream oss(output_file);
//     vector<pair<string, int> > tmp;

//     for (const auto& tmpp: mapping_file) {
//         // cout << (double) bfs_index_map[tmpp.first] / (double) tmpp.second << endl;
//         if ((double) bfs_index_map[tmpp.first] / (double) tmpp.second > ratio_thres && tmpp.second > minimum_size) {
//             tmp.push_back({tmpp.first, tmpp.second});
//         }
//     }

//     sort(tmp.begin(), tmp.end(), pairCompare);
//     for (auto& tt: tmp) {
//         oss << tt.first << "\t" << tt.second << "\n";
//     }

//     oss.close();
// }


// filter out the conference that has lower importance factor
void generate_final_conf(unordered_map<string, int> mapping_file) {
    // ofstream oss(output_file);
    vector<pair<string, double> > generate_list;

    for (const auto& tmpp: mapping_file) {
        // cout << (double) bfs_index_map[tmpp.first] / (double) tmpp.second << endl;
        if ((double) bfs_index_map[tmpp.first] / (double) tmpp.second > ratio_thres) //&& tmpp.second > minimum_size) {
            // tmp.push_back({tmpp.first, tmpp.second});
            final_conf.insert(tmpp.first);
            generate_list.push_back({tmpp.first, (double) bfs_index_map[tmpp.first] / (double) tmpp.second});
        }
    }

    final_conf.insert("SIGIR");
    final_conf.insert("SIGIR Forum");

    for (const auto&ele: generate_list) {
        cout << ele.first << " " << ele.second << "\n";
    }
    cout << "total elements number is: " << generate_list.size() << endl;

}


void generate_smaller_file(int indices) {
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
                    // index_map[venue_string] += 1;

                    if (final_conf.count(venue_string)) {
                        output << line << "\n";
                    }

                    // if (!string_pool.count(venue_string)) continue;
                    // output_lock.lock();
                    // output << line << "\n";
                    // output_lock.unlock();
                }
            }
        }
    }
}



// "venue": "Saudi journal of anaesthesia"

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
                // string_pool.insert(segment);
                bfs_index_map[segment] += 1;
                counter += 1;
                break;
            }
        }   
    }
    // string_pool.insert("SIGIR Forum");
    cout << string_pool.size() << endl;
    string_pool_stream.close();
}



int main() {
    vector<thread> thread_list;
    


    for (int i = 1; i < layer_file_list.size(); i++) {
        create_stringpool(i);
    }


    // for (string dir: dir_list) {
    //     // for (auto & p : fs::directory_iterator(dir)) {
    //     //     if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
    //     //         filedir_list.push_back(p.path());                
    //     //     }
    //     // }
    // }

    filedir_list.push_back(lines_belong_toconf);

    for (int i = 0; i < filedir_list.size(); i++) {
        thread_list.push_back(thread(count_papers_in_each_conf, i));
        // count_papers_in_each_conf(i);
    }

    for (auto& th: thread_list) th.join();
    // 

    thread_list.clear();


    generate_final_conf(index_map);

    output.open(output_file);
    for (int i = 0; i < filedir_list.size(); i++) {
        thread_list.push_back(thread(generate_smaller_file, i));
        // count_papers_in_each_conf(i);
    }

    for (auto& th: thread_list) th.join();
    output.close();
    // dump_file(index_map);
}

