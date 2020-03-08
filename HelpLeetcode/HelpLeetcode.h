//
// Created by YunLambert.
//

#ifndef INC_20200201_HELPLEETCODE_H
#define INC_20200201_HELPLEETCODE_H

#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <sstream>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <type_traits>>

class TreeNode {
public:
    int val;
    TreeNode *left;
    TreeNode *right;

    TreeNode(int x) : val(x), left(NULL), right(NULL) {}

//    TreeNode(const TreeNode &obj) {
//        //std::cout<<obj.val<<std::endl;
//        ptr = new TreeNode(obj.val);
//        *ptr = *obj.ptr;
//    }
    ~TreeNode() {
        std::cout << "destroy a tree..." << std::endl;
        delete ptr;
    }

private:
    TreeNode *ptr;
};
namespace hlc {
    /*
     * To parse string into a vector.
     * Example:
     * Input: (string)[1, null, 2, 3]
     * Output: (vector<int>){1, INT_MAX, 2, 3}
     * */
    template<typename T>
    std::vector<T> parseString(std::string &s) {
        auto itor = std::remove_if(s.begin(), s.end(), isspace);
        s.erase(itor, s.end());
        std::vector<T> result;
        if (s.size() <= 2) return result;
        s = s.substr(1, s.size() - 2);   // delete '[' and ']'
        std::vector<std::string> t;
        std::stringstream s_stream(s);    // create string stream from the string
        while (s_stream.good()) {
            std::string x;
            getline(s_stream, x, ','); // get first string delimited by comma
            t.push_back(x);
        }

        for (int i = 0; i < t.size(); ++i) {
            T num = 0;
            if (t[i] == "null") num = INT_MAX;
            else {
                for (int j = 0; j < t[i].size(); ++j) {
                    num = num * 10 + t[i][j] - '0';
                }
            }
            result.push_back(num);
        }
        return result;
    }


    void SubTreePrint(TreeNode *node, int level) {
        if (!node)
            return;

        SubTreePrint(node->right, level + 1);
        for (int i = 0; i < level; i++) {
            std::cout << "    ";
        }
        std::cout << std::setw(4) << node->val << std::endl;
        SubTreePrint(node->left, level + 1);
    }

    void Print(TreeNode *root) {
        std::cout << "------------------------------------" << std::endl;
        SubTreePrint(root, 0);
        std::cout << "------------------------------------" << std::endl;
    }

    /*
     * Make a tree according with string s.
     * Example:
     * Input: "[1, null, 2, 3, 4]"
     * Output: TreeNode*  1
     *                   / \
     *                 null 2
     *                     /  \
     *                    3    4
     * */
    TreeNode *makeTreeTest2(std::string &s) {
        std::vector<int> nums;
        std::vector<TreeNode *> t;

        nums = parseString<int>(s);
        for (auto it : nums) {
            if (it == INT_MAX) t.push_back(NULL);
            else {
                TreeNode *node = new TreeNode(it);
                t.push_back(node);
                //delete (node); // avoid memory leak
            }
        }
        //for (auto it : t) std::cout<<it->val<<std::endl;
        if (t.empty()) return NULL;
        int index = 1;
        while (index * 2 + 1 <= t.size()) {
            if (index * 2 <= t.size() && t[index * 2 - 1] != NULL) t[index - 1]->left = t[index * 2 - 1];
            if (index * 2 + 1 <= t.size() && t[index * 2] != NULL) t[index - 1]->right = t[index * 2];
            ++index;
        }
        TreeNode *testNode = t[0];
        //for (int i = 0; i < t.size(); ++i) delete t[i];
        return testNode;
    }

    TreeNode *makeTreeTest(std::string &s) {
        std::vector<int> nums;
        nums = parseString<int>(s);
        size_t count = nums.size();
        TreeNode **treeArr = new TreeNode *[count];
        for (size_t i = 0; i < count; i++) {
            if (INT_MAX == nums[i]) {
                treeArr[i] = NULL;
            } else {
                treeArr[i] = new TreeNode(nums[i]);
            }
        }

        size_t curr = 1;
        for (size_t i = 0; i < count; i++) {
            if (!treeArr[i]) {
                continue;
            }

            if (curr < count) {
                treeArr[i]->left = treeArr[curr++];
            }
            if (curr < count) {
                treeArr[i]->right = treeArr[curr++];
            }
        }

        TreeNode *root = treeArr[0];
        //std::cout<<treeArr[0]->val<<" "<<treeArr[1]->val<<std::endl;
        delete[] treeArr;
        return root;
    }
}


#endif //INC_20200201_HELPLEETCODE_H
