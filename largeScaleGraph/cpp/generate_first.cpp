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


// all the lines belongs to SIGIR has already in this input dir.
// no need to change this
string input_dir_1 = "./first_layer_extraction";

// Configuration: output file of the first layer
string output_file = "/home/wuzhuofeng/raw_data/cpp_largevis_first.txt";


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
regex single_id("\".{36}\"");
regex year("\"year\": .*?,");

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
        if (content[start] == '\"') {
            buffer = "";
            allow = true;
        }
        if (content[start] == '\"') {
            ans.append(buffer + " ");
            allow = false;
        }
        else if (allow) {
            buffer.push_back(content[start]);
        }
        start++;
    }
    cout << ans << endl;
    return ans;
}




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
                    cout << line << endl;
                    string id_string = extract_id(string(id_extract[0]));
                    cout << "pass" << endl;

                    string refer_string = "";
                    string year_string = string(year_extract[0]).substr(8, string(year_extract[0]).length() - 9);
                    cout << "pass2" << endl;
                    size_t found = line.find(references_start);
                    if (found != std::string::npos) {
                        string input_string = "";
                        
                        cout << "enter" << endl;
                        int start = 15 + found;
                        while (line[start] != ']') {
                            input_string.push_back(line[start]);
                            start++;
                        }
                        cout << "input string is " << input_string << endl; 
                        refer_string = get_ref_string(input_string);
                    }
                    cout << "pass3" << endl;

                    output_lock.lock();
                    output << id_string + "\tinternational acm sigir conference on research and development in information retrieval\t" + year_string + "\t" + refer_string << "\n";
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





