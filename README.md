## How it works

GenUserList is a tool that allows you to generate a list of usernames based on the collected full names of employees of a target organization or any other group of people. Specify suggested patterns, make a list of people's names and get suggested logins, usernames or parts of emails.

The most typical use case for this tool is to generate lists of users for resources that are associated with Active Directory.

## Install GUL

Download project:

```sh
git clone https://github.com/letsIG0rAWAY/GenUserList.git
```

Go to folder:

```sh
cd GenUserList
```

Install virtualenv

```sh
pip3 install virtualenv
```

Create virtualenv

```sh
virtualenv <env_name>
```

Activate virtualenv:

```sh
source <env_name>/bin/activate
```

Install deps:

```sh
pip3 install -r requirements.txt
```
## Usage

```sh
python3 gul.py --help
```

This will display help for the tool. Here are all the switches it supports.


```console
usage: gul.py [-h] -tfile TEMPLATEFILE -sufile SEARCHEDUSERSFILE -enusfile ENUMERATEDUSERSFILE

Generate userlist to brute force Active Directory environmen

options:
  -h, --help            show this help message and exit
  -tfile TEMPLATEFILE, --templatefile TEMPLATEFILE
                        path to file with username templates
  -sufile SEARCHEDUSERSFILE, --searchedusersfile SEARCHEDUSERSFILE
                        path to file with searched users
  -enusfile ENUMERATEDUSERSFILE, --enumeratedusersfile ENUMERATEDUSERSFILE
                        path to file to store enumerated usernames
```

Find people related to the organization and make a list of their names `searched_users/searched_users_template.txt` (surname name middlename):

```sh
Морозов Константин Петрович
Петрова Светлана Е
Евдокимова А П
Аминов Емиль
Петров М
```

Make a list of username patterns `templates/templates_template.txt` (each line is a pattern in which a space is used as a delimiter):

- surname - surname
- s - first letter of surname
- name - name
- n - first letter of name
- middlename - middlename
- m - first letter of middlename
- `'-,_,."` - delimiter

```sh
surname
surname name
surname . name
surname - name
surname _ name
surname n
surname . n
surname - n
surname _ n
surname n m
surname . n m
surname . n . m
surname - n m
surname - n - m
surname _ n m
surname _ n _ m
name surname
name . surname
name - surname
name _ surname
name s
name . s
name - s
name _ s
n m surname
n m . surname
n . m . surname
n m - surname
n - m - surname
n m _ surname
n _ m _ surname
```

## Running GUL

Run GUL to create a brute force list `enumerated_usernames/enumerated_usernames.txt`:

```sh
python3 gul.py -sufile ./searched_users/searched_users_template.txt -tfile ./templates/templates_template.txt -enusfile ./enumerated_usernames/enumerated_usernames.txt
```

If we cannot find people associated with an organization, or we are considering a large organization, it is effective to compile a list of the most common names and surnames. Below is a one-liner for generating a potential list of names:

```sh
for surname in $(cat wordlists/surnames/surnames_woman_zhuravlev.txt | tr "\n" " "); do for name in $(cat wordlists/names/names_woman_top100.txt); do echo "$surname $name" >> searched_users/searched_users_ribbon_woman_surname_top500_name_top100.txt; done; done
```

The `gen_mutations.py` script can be used for the same purpose.

```sh
python3 gen_mutations.py > searched_users/searched_users_mutations.txt
```