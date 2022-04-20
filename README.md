# WBZ
A parallel implementation of the bzip2 data compressor in python, this data compression pipeline is using algorithms like **Burrows–Wheeler transform (BWT)** and **Move to front (MTF)** to improve the **Huffman compression**. For now, this tool only will be focuses on compressing .csv files and other files on tabular format.
 

## Data pipeline compression
![alt text](https://wittline.github.io/wbz/img/wbz.png)

## How to use the tool
The tool is called WBZ, the first version only will be focused in compressing .csv files and I will be adding more features coming soon, the parameters are described as follow:


```linux 
python wbz.py -a encode -f 'C:\Users\...\data.csv' -cs 20000 -ch ';'

python wbz.py -a decode -f 'C:\Users\...\data.wbz' -cs 20000 -ch ';'
```

- **-a** is **action** , there is two actions: encode and decode
- **-f** is **filepath**, if your action is encode make sure that the filepath choosed is a .csv file, if your action is decode make sure that you choosed filepath is a file with extension .wbz
- **-cs** is **chunk size**, the algorithm Burrows–Wheeler transform (BWT) works with chunks sized in bytes, with this parameter you would specify the number of bytes to be processed by each CPU.
- **-ch** is **special character**, each chunk encoded by the algorithm Burrows–Wheeler transform (BWT) will contain an special character inside it, it will help to identify an index for decodeding purposes, The possible column separator characters in your .csv file could work as a special character, it is recommended to use a separator that is not used by your columns and that does not appear in the content of the columns, this feature will be removed in the next versions of this tool.


The same chunk size and special character used for encode the file must be used for decode the file, The idea of keep them as parameters is to be able to get a better trade-off of the speed in the encoding and decoding process and a better compression rate.

## Performance
The tests were done with three .csv files of different sizes and varying the chunk size:

- **data_1000000**: One million records (61mb)
- **data_500000**: Half a million records (31 mb)
- **data_250000**: A quarter of a million records (16 mb)

There is an improvement in the rate compression for larger chunk sizes.

![Imagen1](https://user-images.githubusercontent.com/8701464/164333632-da1a97bd-9438-4065-9d1b-bfd83b54e820.png)


The compression times increase with a logarithmic behavior when the size of the chunk is increased as well.
![Imagen2](https://user-images.githubusercontent.com/8701464/164333652-4e144edf-a8c2-49fc-b9de-3bd4536ea427.png)

Regardless of the size of the file, the decompression times have a constant behavior and tend to be reduced when the size of the chunk increases as well.

![Imagen3](https://user-images.githubusercontent.com/8701464/164333663-6c3aad0d-952e-458d-a230-82f752d626ac.png)


### Future versions of this tool will focus on:

- Improve the compression times of huffman and BWT encoding times.
- Improve the encode of the huffman table
- Compression based on columns
- Compress and decompress specific columns on the .csv file
- Generate compressed chunks automatically for large files
- Distributed compression and decompression

## Contributing and Feedback
Any ideas or feedback about this repository?. Help me to improve it.

## Authors
- Created by <a href="https://www.linkedin.com/in/ramsescoraspe"><strong>Ramses Alexander Coraspe Valdez</strong></a>
- Created on 2022

## License
This project is licensed under the terms of the Apache License.
