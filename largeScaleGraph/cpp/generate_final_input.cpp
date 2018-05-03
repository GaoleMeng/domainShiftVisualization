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

string input_dir_1 = "/scratch/si699w18_fluxm/gaole/lines_belong_toconf_smaller.txt";
// string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
// string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
// string input_lastlayer = "/scratch/si699w18_fluxm/gaole/cpp_largevis_first.txt";
string output_file = "/scratch/si699w18_fluxm/gaole/non_bias_edges_withauthors.txt";
string split_location = "/home/gaole/tmprepo/largeScaleGraph/cpp/final_visulization/";


bool pairCompare(const std::pair<string, int>& firstElem, const std::pair<string, int>& secondElem) {
  return firstElem.second < secondElem.second;

}

vector<string> dir_list = {input_dir_1};
unordered_set<string> string_pool;
unordered_set<string> conf_pool;


unordered_map<int, string> index_to_loc;

unordered_map<string, vector<int>> year_to_indexlist;
unordered_map<int, vector<int>> layer_list;
unordered_map<string, int> id_to_index;
unordered_map<int, unordered_set<string>> id_to_ref;
unordered_map<int, string> index_to_conf;
unordered_map<string, int> conf_to_index;

unordered_set<int> sigir_pool;

unordered_map<string, int> year_counter;
// unordered_map<string,>

string lastfix = ".txt";

static mutex output_lock;
mutex parselock;
ofstream output;
ifstream string_pool_stream;

int index_count = 0;
int total_sigir = 0;
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
        if (found != std::string::npos) {
            id_string = line.substr(found + 7, 24);
            // if (!string_pool.count(id_string)) continue;
            smatch venue_extract;
            if (regex_search(line, venue_extract, venue)) {
                string refer_string = "";
                smatch year_extract;
                if (regex_search(line, year_extract, year)) {
                    venue_string = string(venue_extract[0]).substr(10, venue_extract[0].length() - 11);
                    string year_string = string(year_extract[0]).substr(8, string(year_extract[0]).length() - 9);


                    // cout << venue_string << endl;
                    id_to_index[id_string] = index_count;
                    conf_pool.insert(venue_string);

                    size_t found = line.find(references_start);
                    if (found != std::string::npos) {
                        int start = 16 + found;
                        while (true) {
                            id_to_ref[index_count].insert(line.substr(start, 24));
                            // refer_string.append(line.substr(start, 24) + " ");
                            if (line[start + 25] == ']') break;
                            start += 28;
                        }
                    }

                    // cout << index_count << endl;
                    if (venue_string == "SIGIR" || venue_string == "SIGIR Forum"){
                        year_counter[year_string]++;
                        sigir_pool.insert(index_count);
                        total_sigir += 1;
                    }

                    year_to_indexlist[year_string].push_back(index_count);
                    index_count++;

                    // output_lock.lock();
                    // output << id_string + "\t" + venue_string + "\t" + year_string + "\t" + refer_string << "\n";
                    // output_lock.unlock();
                }
            }
        }
    }
}

size_t split(const std::string &txt, std::vector<std::string> &strs, char ch)
{
    size_t pos = txt.find( ch );
    size_t initialPos = 0;
    strs.clear();

    // Decompose statement
    while( pos != std::string::npos ) {
        strs.push_back( txt.substr( initialPos, pos - initialPos ) );
        initialPos = pos + 1;

        pos = txt.find( ch, initialPos );
    }

    // Add the last one
    strs.push_back( txt.substr( initialPos, std::min( pos, txt.size() ) - initialPos + 1 ) );

    return strs.size();
}


void dump_file(unordered_map<string, int> mapping_file) {
    for (const auto& tmp: mapping_file) {
        cout << tmp.first << " " << tmp.second << "\n";
    }
}

void dump_file(unordered_map<int, string> mapping_file) {
    for (const auto& tmp: mapping_file) {
        cout << tmp.first << " " << tmp.second << "\n";
    }
}



void generate_conf_index() {
    for (const string& tmp: conf_pool) {
        conf_to_index[tmp] = index_count++;
    }
}


void generate_edges() {

    for (const auto& tmp: id_to_ref) {
        int ii = tmp.first;
        for (const string& ref: tmp.second) {
            if (!id_to_index.count(ref)) continue;
            output << ii << " " << id_to_index[ref] << " " << "1\n";
        }
    }

    for (const auto& tmp: index_to_conf) {
        output << tmp.first << " " << conf_to_index[tmp.second] << " 2" <<"\n";
    }
}


void generate_files() {
    int threshold = 1100;
    int cur_layer = 1;
    int cur_count = 0;
    vector<pair<string, int>> year_extract_list;

    for (const auto& tmp: year_counter) {
        year_extract_list.push_back({tmp.first, tmp.second});
    }


    sort(year_extract_list.begin(), year_extract_list.end(), pairCompare);

    // ofstream oss();
    
    for (const auto& tmp: year_extract_list) {

        vector<int>& index_list = year_to_indexlist[tmp.first];

        int cc = 0;
        for (int index: index_list) {
            if (!index_to_loc.count(index)) continue;
            if (sigir_pool.count(index)) cc++;
            layer_list[cur_layer].push_back(index);
        }

        // layer_list[cur_layer].push_back(tmp.second);

        cur_count += cc;
        if (cur_count > threshold) {
            cur_layer += 1;
            cur_count = 0;
        }
    }

    for (const auto& tmp: layer_list) {
        
        ofstream point_file(split_location + to_string(tmp.first) + "_points.txt");
        ofstream label_file(split_location + to_string(tmp.first) + "_labels.txt");

        point_file << tmp.second.size() << "\n";
        for (int index: tmp.second) {

            point_file << index_to_loc[index] << "\n";
            if (sigir_pool.count(index)) {
                label_file << "10" << "\n";
            }
            else {
                label_file << "0" << "\n";
            }

        }
        point_file.close();
        label_file.close();
    }

    // oss.close();

}





// "venue": "Saudi journal of anaesthesia"

void create_index_loc() {
    string tmp_file = "./citation_qiaozhu.txt";
    ifstream input(tmp_file.c_str());
    string line = "";
    int flag = 0;

    while(getline(input, line)) {
        if (!flag) {
            flag = 1;
            continue;
        }

        string tmp_line = line;

        vector<string> line_list;
        istringstream iss(line);
        string s;

        iss >> s;
        int index = stoi(s);
        index_to_loc[index] = line;
        // cout << line << endl;
        // while ( getline( iss, s, ' ' )) {
        //     int index = stoi(s);
        //     index_to_loc[index] = tmp_line;
        //     cout << tmp_line;
        //     break;
        // }
    }
}





int main() {
    vector<thread> thread_list;
    output.open(output_file);
    // string_pool_stream.open(input_lastlayer);
    // create_stringpool();


    // for (string dir: dir_list) {
    //     // for (auto & p : fs::directory_iterator(dir)) {
    //         // if (strstr(p.path().filename().c_str(), lastfix.c_str())) {
    //     filedir_list.push_back(p.path());                
    //         // }
    //     // }
    // }
    filedir_list.push_back(input_dir_1);
    for (int i = 0; i < filedir_list.size(); i++) {
        thread_list.push_back(thread(read_and_parse, i));
        // read_and_parse(i);
    }

    for (auto& th: thread_list) th.join();

    create_index_loc();
    generate_conf_index();
    generate_edges();


    // dump_file(year_counter);


    generate_files();
    // dump_file(index_to_loc);

    output.close();
}





