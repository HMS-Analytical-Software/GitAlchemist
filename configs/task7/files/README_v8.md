# Motivation behind the project

We wanted to have a simple tool to generate a password based on adjustable parameters.
Some other generic motivation text...

# Usage

Execute main.py via
```bash
python main.py
```
to generate a password. The default is set to a length of 12 without digits and special characters. 
This can be adjusted via command line arguments.
To print a password containing digits and special characters use
```bash
python main.py --digits --special_characters
```

To adjust the length of the password the keyword length can be used. 
Print a password with length 20 with the following command 
```bash
python main.py --length 20
```

For further help use 
```bash
python main.py -h
```