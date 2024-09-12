# OvertoneDB

 Program to supply information about the overtones of musical notes

## Installing
Download and install python [here](https://www.python.org/downloads/)

## Setup

__Clone the repo__
```sh
git clone https://github.com/j-weatherwax/OvertoneDB.git
cd OvertoneDB
```
__Running the project__  
Use createDB.py to generate the database.  User is prompted for the amount of overtones written per note.

```python
main.py [Reference Notes] [flag] [Notes to Check]
```

__Command Line Arguments__
|Argument Command|Example Usage|Description|
|----|----|----|
|-h, --help|main.py -h|Shows help message and usage information|
|-l, --list-overtones|main.py C1 -l|Lists the overtones for the given notes|
|-c, --check-overtones|main.py C1 -c C4 D2 G5|Checks if any of the notes after -c are overtones of the notes before the flag|
|-s, --share-overtones|main.py C1 -s C4 D2 G5|Checks if any of the notes after -s share overtones with the notes before the flag|

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
