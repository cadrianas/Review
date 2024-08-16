# Explanation of the process

Aim: take all files in an input directory, apply some processing to them, saving them as files with the same name prefix and a suffix indicating the type of processing carried out, in an output directory.

The input and output directory should be arguments to the program.

The code must list all files in the input directory and all files in the output directory with the required suffix.

If I is the set of input files and O is the set of output files, then there remains to process files in the set P=setdiff(O,I). Take a random file in P and process it.

Advantage of proceeding that way: if I and O are shared between machines (i.e., on the NAS), then taking random entries in P means that different machines are very likely to pick up different files, especially when there remains a lot of files to process.

So the computation loop should be as follows:
- Get list of files in I and O and compute P.
- Take a random element in P, process it and save the result in O.
- If need be, pause for a few seconds to let temperature go down (have a flag for that).
- Repeat.