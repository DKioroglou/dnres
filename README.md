# dnres: data n results

`dnres` is a python package for managing and sharing data and results generated from any type of data analysis. It facilitates modular type of analysis by allowing easy storing and loading of python objects or files across different python scripts.

## Usage

### Configuation file

`dnres` requires a configuration file. In this file, three sections should be specified: **STRUCTURE**, **DATABASE** and **INFO**. 

Example of configuration file with filename `config.ini`:
```python
[STRUCTURE]
dir1 = foo/bar
dir2 = foo/foo/bar

[DATABASE]
filename = data.db

[INFO]
description = "This is the description of the analysis related to the data and results."
```

The configuration file is passed as argument upon instantiation of the `DnRes`
```python
from dnres import DnRes

res = DnRes('config.ini')
```

Upon instantiation, the following are checked/performed:

* STRUCTURE section exists and it's not empty.  
* Paths in STRUCTURE exist. If not, they are created.  
* DATABASE section and filename key exist. Otherwise, database gets initialized.  
* INFO section exists and description is provided. If not, user gets a warning.


### Storing and loading of python objects

Example of storing a list in analytical script `script_01.py` 

```python
from dnres import DnRes

res = DnRes('config.ini')

# Create some data
x = [1,2,3]

# Store data to use in another analytical script
res.store(data=x,
          directory='dir1',
          filename='x_var.json',
          description='List with three numbers',
          source='script_01.py',
          serialization='json'
         )
```

Example of loading stored data from `script_01.py` in `script_02.py`:

```python
from dnres import DnRes

res = DnRes('config.ini')

# Show available stored data
print(res)

# Load stored data
x = res.load('dir1', 'x_var.json')
```

### Storing and loading of files

Example of storing a `.csv` file in analytical script `script_01.py`

```python
from dnres import DnRes

res = DnRes('config.ini')

# Example of saving a pandas dataframe to csv
filepath = 'foo.csv'
df.to_csv(filepath, sep='\t')

# file will be moved to corresponding path in STRUCTURE
res.store(data=filepath,
          directory='dir2',
          filename='foo.csv',
          description='A pandas dataframe stored as csv.',
          source='script_01.py',
          isfile=True
         )
```

Load stored `.csv` file in analytical script `script_02.py`

```python
from dnres import DnRes
import pandas as pd

res = DnRes('config.ini')

# load() method returns string when stored data is not python object.
filepath = res.load('dir2', 'foo.csv')
df = pd.read_csv(filepath, sep='\t')
```

## Installation

```bash
pip install dnres
```

## License

BSD 3

