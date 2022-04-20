# WBZ
A parallel implementation of the bzip2 data compressor in python, this data compression pipeline is using algorithms like **Burrows–Wheeler transform (BWT)** and **Move to front (MTF)** to improve the **Huffman compression**. For now, this tool only will be focuses on compressing .csv files and other files on tabular format.

When we talk about computation time we are also talking about money, data compression represents the most appropriate economic way to shorten the gap between content creators and content consumers, compressed files are obviously smaller, it is necessary less money and time to transfer them and cost less money to store them, content creators pay less money to distribute their content, and content consumers pay less money to consume content. On the other hand, companies in all sectors need to find new ways to control the rapidly growing volume of their heterogeneous data generated every day, data compression and data decompression tools are related as one of the most viable solutions to these problems. In fact, data compression and data decompression techniques are the DNA of many famous distributed systems and part of their success is due to the proper use of these techniques. 

## Data pipeline compression

![alt text](https://wittline.github.io/wbz/img/wbz.png)

## How to use the tool
The tool is called WBZ, the first version only will be focused in compressing .csv files and I will be adding more features coming soon, the parameters are described as follow:

python wbz.py -a encode -f 'C:\Users\...\data.csv' -cs 20000 -ch ';'
python wbz.py -a decode -f 'C:\Users\...\data.wbz' -cs 20000 -ch ';'

-a is action , there is two actions: encode and decode
-f is filepath, if your action is encode make sure that the filepath choosed is a .csv file, if your action is decode make sure that you choosed filepath is a file with extension .wbz
-cs is chunk size, the algorithm Burrows–Wheeler transform (BWT) works with chunks sized in bytes, with this parameter you would specify the number of bytes to be processed by each CPU.
-ch is special character, each chunk encoded by the algorithm Burrows–Wheeler transform (BWT) will contain an special character inside it, it will help to identify an index for decodeding purposes, The possible column separator characters in your .csv file could work as a special character, it is recommended to use a separator that is not used by your columns and that does not appear in the content of the columns, this feature will be removed in the next versions of this tool.



