
# coding: utf-8

# In[2]:


def findGraphPath(key_value, start, end):
    dic = {}
    result = []
    for i in range(int(len(key_value)/2)):
        if key_value[2*i] not in dic:
            dic[key_value[2*i]] = {}
        dic[key_value[2*i]][key_value[2*i+1]] = 0
    myDFS(dic, start, end)
    return paths


# In[3]:


paths = []


def myDFS(dic, start, end, path = []):
    path = path + [start]
    if start == end or start not in dic:
        paths.append(path)
    if start not in dic:
        return
    for node in dic[start]:
        if dic[start][node] == 0:
            dic[start][node] = 1
            myDFS(dic, node, end, path)
            dic[start][node] = 0

# In[8]:


if __name__ == "__main__":
    print(findGraphPath([1,2,1,3,1,4], 1, -1))