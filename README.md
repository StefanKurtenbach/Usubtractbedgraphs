# Usubstractbedgraphs
Substracts two bedgraph files

Example usage:
python Usubtractbedgraphs.py -f1 test1.bedgraph -f2 test2.bedgraph -o difference.bedgraph

options:
-d Y
deletes every overlap in file1 if file2 has an entry. A BED file can be used insted of a bedgraph. Default: -d N
