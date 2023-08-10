# pwgen

A command-line tool to generate cryptogrpahically strong passwords, passphrases, 
and tokens in pure python.

## Dependencies

python +3.9

## Randomness of password, phrase, token

To be secure against brute-force attacks, tokens need to have sufficient 
randomness. Unfortunately, what is considered sufficient will necessarily 
increase as computers get more powerful and able to make more guesses in a 
shorter period. As of 2015, it is believed that 32 bytes (256 bits) of 
randomness is sufficient for the typical use-case expected for the secrets 
module.

## Usage

```bash
python pwgen.py -h
```

    usage: pwgen [-h] {password,passphrase,token,url-token,entropy} ...

    Generate cryptographically strong random passwords, phrases, and url tokens

    optional arguments:
    -h, --help            show this help message and exit

    subcommands:
    {password,passphrase,token,url-token,entropy}
                            sub-command help
        password            Generate random password
        passphrase          Generate random XKCD-style passphrase
        token               Generate random text string
        url-token           Generate random URL-safe text string

```bash
python pwgen.py password -h
```

    usage: pwgen password [-h] [-l LENGTH] [-p]

    Generate cryptographically strong alphanumeric random password with at least
    one lowercase character, at least one uppercase character, and at least one 
    digit.

    optional arguments:
    -h, --help            show this help message and exit
    -l LENGTH, --length LENGTH
                          Character length of password (default: 40)
    -p, --punctuation     Include punctuation in password (default: False)

```bash
python pwgen.py passphrase -h
```

    usage: pwgen passphrase [-h] [-l LENGTH] [-d {-,@,#,!,$,&}] [-f FILE]

    Generate a XKCD-stype passphrase from randomly selected words from a 
    word-list file. On standard Linux systems, it searches in common locations 
    for word files to use. Other platforms may need to provide their
    own word-list. The selected words are randomly chosen to be uppercase or 
    lowercase.

    optional arguments:
    -h, --help            show this help message and exit
    -l LENGTH, --length LENGTH
                          Number of words in passphrase (default: 4)
    -d {-,@,#,!,$,&}, --delimiter {-,@,#,!,$,&}
                          Delimiter to separate words in passphrase (default: -)
    -f FILE, --file FILE  Word file used to generate passphrase (default: None)

```bash
python pwgen.py token -h
```

    usage: pwgen token [-h] [-l LENGTH]

    Generate a random text string, in hexadecimal, with a minimum of 256 bits 
    of randomness. The string has nbytes random bytes, each byte converted to 
    two hex digits.

    optional arguments:
    -h, --help            show this help message and exit
    -l LENGTH, --length LENGTH
                          Number of random bytes in token (default: 32)

```bash
python pwgen.py url-token -h
```

    usage: pwgen url-token [-h] [-l LENGTH]

    Generate a random, hard-to-guess URL-safe text string with a minimum of 256 
    bits of randomness. Could be used as a security token, for example, 
    suitable for password recovery applications.

    optional arguments:
    -h, --help            show this help message and exit
    -l LENGTH, --length LENGTH
                          Number of random bytes in token (default: 32)
