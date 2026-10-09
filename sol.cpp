#include <bits/stdc++.h>
using namespace std;

struct Token {
    int offset;
    int length;
    char nextChar;
    bool hasNextChar;
};

vector<Token> compressLZ77(const string& s) {
    vector<Token> result;
    int pos = 0;

    while (pos < (int)s.size()) {
        int bestOffset = 0;
        int bestLength = 0;

        for (int start = pos - 1; start >= 0; --start) {
            int length = 0;

            while (pos + length < (int)s.size() &&
                   s[start + length] == s[pos + length]) {
                ++length;
            }

            if (length > bestLength) {
                bestLength = length;
                bestOffset = pos - start;
            }
        }

        int nextPos = pos + bestLength;

        if (nextPos < (int)s.size()) {
            result.push_back({bestOffset, bestLength, s[nextPos], true});
            pos = nextPos + 1;
        } else {
            result.push_back({bestOffset, bestLength, '\0', false});
            pos = nextPos;
        }
    }

    return result;
}

string decompressLZ77(const vector<Token>& tokens) {
    string out;

    for (const Token& t : tokens) {
        for (int i = 0; i < t.length; ++i) {
            out += out[out.size() - t.offset];
        }

        if (t.hasNextChar) {
            out += t.nextChar;
        }
    }

    return out;
}

int main() {
    string input;
    cout << "Enter the string: ";
    getline(cin, input);

    vector<Token> compressed = compressLZ77(input);

    cout << "Compressed tokens:\n";
    for (const Token& t : compressed) {
        if (t.hasNextChar) {
            cout << "(" << t.offset << ", " << t.length << ", '" << t.nextChar << "')\n";
        } else {
            cout << "(" << t.offset << ", " << t.length << ", null)\n";
        }
    }

    cout << "Decompressed string: " << decompressLZ77(compressed) << "\n";

    return 0;
}
