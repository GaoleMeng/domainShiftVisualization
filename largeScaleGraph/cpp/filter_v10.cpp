// compiler with 
// g++ -std=c++17  generate_third.cpp -o generate_third -lstdc++fs -pthread
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
#include <iostream>
#include <experimental/filesystem>
// #include <boost/range/iterator_range.hpp>
namespace fs = std::experimental::filesystem;
using namespace std;



// Congiguration: input aminer directory
string input_dir_1 = "/storage6/foreseer/users/zhuofeng/evolution_of_words/experiment/da/test/dblp-ref/";
// string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
// string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";
// Configuration: input comes from the output of the second layer

// Configuration: output the final layer o
string output_file = "/storage6/foreseer/users/zhuofeng/visualization_of_conference_evolution/tmp_files/lines_belong_toconf_smaller.txt";

string list_file_name = "./csranking_list.txt";

vector<string> dir_list = {input_dir_1};
unordered_set<string> string_pool;
unordered_map<string, string> conf_name_mapping;

string lastfix = ".json";

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


string extract_id(string org_string) {
    return org_string.substr(7, org_string.length() - 8);
}


bool pairCompare(const std::pair<string, int>& firstElem, const std::pair<string, int>& secondElem) {
  return firstElem.second < secondElem.second;
}

void create_map_name_mapping() {
    ifstream input(list_file_name.c_str());
    string line = "";
    while(getline(input, line)) {
        string segment = "";
        istringstream segment_ss(line);

        int counter = 0;
        string conf = "";
        while(getline(segment_ss, segment, '\t')) {
            if (counter == 0) {
                counter += 1;
                conf = segment;
                continue;
            }
            else {
                conf_name_mapping[segment] = conf;
            }
        }
    }
}




string get_ref_string(string& content) {
    if (content == "") return "";
    string buffer = "";
    int start = 0;
    bool allow = false;
    string ans = "";
    
    while (start < content.length()) {
        if (content[start] == '\"' && !allow) {
            buffer = "";
            allow = true;
        }
        else if (content[start] == '\"' && allow) {
            ans.append(buffer + " ");
            allow = false;
        }
        else if (allow) {
            buffer.push_back(content[start]);
        }
        start++;
    }
    return ans;
}



void read_and_parse(int indices) {
    
    string filename = filedir_list[indices];
    
    ifstream input(filename.c_str());
    string line = "";
    size_t found;
    string venue_string = "";
    string year_string = "";
    
    
    while(getline(input, line)) {
        // cout << line << endl;
        // cout << line << endl;
        smatch id_extract;
        found = line.find(id_start);
        // cout << line << endl;

        if (regex_search(line, id_extract, id)){
            if (found != std::string::npos) {
                smatch venue_extract;
                if (regex_search(line, venue_extract, venue)) {

                    string refer_string = "";
                    smatch year_extract;
                    venue_string = string(venue_extract[0]).substr(10, venue_extract[0].length() - 11);
                    if (conf_name_mapping.count(venue_string)) {
                        output_lock.lock();
                        output << line << "\n";
                        output_lock.unlock();
                    }
                }
            }
        }
    }
}

// "venue": "Saudi journal of anaesthesia"

int main() {
    vector<thread> thread_list;
    output.open(output_file);
    // string_pool_stream.open(input_lastlayer);
    // create_stringpool();
    create_map_name_mapping();
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


