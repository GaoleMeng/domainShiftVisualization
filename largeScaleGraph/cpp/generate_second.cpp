// g++ -std=c++17  generate_second.cpp -o generate_second -lstdc++fs -pthread


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


// Configuration: all the aminer input files, changable directory (not files!)
string input_dir_1 = "/storage6/foreseer/users/zhuofeng/evolution_of_words/experiment/da/test/dblp-ref/";
// string input_dir_2 = "/scratch/si699w18_fluxm/gaole/aminer_papers_1";
// string input_dir_3 = "/scratch/si699w18_fluxm/gaole/aminer_papers_2";

// Configuration: input file, change to the first layer output file
string input_lastlayer = "/home/zhuofeng/cpp_largevis_first.txt";

// Configuration: changable second layer output representation file
string output_file = "/home/zhuofeng/cpp_largevis_second.txt";


// vector<string> dir_list = {input_dir_1, input_dir_2, input_dir_3};
vector<string> dir_list = {input_dir_1};

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
regex year("\"year\": .*?,");

string id_start = "\"id\": ";
string venue_start = "\"venue\": ";
string year_start = "\"year\": ";
string references_start = "\"references\": ";

string extract_id(string org_string) {
    return org_string.substr(7, org_string.length() - 8);
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
    string id_string = "";
    string venue_string = "";
    string year_string = "";


    while(getline(input, line)) {
        // cout << line << endl;
        found = line.find(id_start);
        // cout << line << endl;
        if (found != std::string::npos) {
            id_string = line.substr(found + 7, 24);
            if (!string_pool.count(id_string)) continue;
            smatch venue_extract;
            if (regex_search(line, venue_extract, venue)) {
                string refer_string = "";
                smatch year_extract;
                if (regex_search(line, year_extract, year)) {
                    venue_string = string(venue_extract[0]).substr(10, venue_extract[0].length() - 11);
                    string year_string = string(year_extract[0]).substr(8, string(year_extract[0]).length() - 9);

                    size_t found = line.find(references_start);
                    if (found != std::string::npos) {
                        string input_string = "";
                        int start = 15 + found;
                        while (line[start] != ']') {
                            input_string.push_back(line[start]);
                            start++;
                        }
                        // cout << "input string is " << input_string << endl; 
                        refer_string = get_ref_string(input_string);
                    }

                    output_lock.lock();
                    output << id_string + "\t" + venue_string + "\t" + year_string + "\t" + refer_string << "\n";
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
                istringstream ref_ss(segment);
                string tmp = "";
                while (ref_ss >> tmp) {
                    string_pool.insert(tmp);
                }
            }
        }
    }

    for (const auto& elem: prev_strings) {
        if (string_pool.count(elem)) {
            string_pool.erase(elem);
        }
    }
    cout << string_pool.size() << endl;

    // for (string tmp: string_pool) {
    //     cout << tmp << endl;
    // }
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
    cout << "filedir length: " << filedir_list.length() << endl;
    for (int i = 0; i < filedir_list.size(); i++) {
        thread_list.push_back(thread(read_and_parse, i));
        // read_and_parse(i);
    }

    for (auto& th: thread_list) th.join();
    output.close();
}








