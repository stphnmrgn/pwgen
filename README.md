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

## Warning

It is probably best to not print secrets to the terminal, which this CLI
does by default. If using for this CLI to generate secrets for realz, then pipe
the secret to your clipboard. e.g.

```bash
python pwgen.py password | xclip -select clipboard
```

## Usage

```console
python pwgen.py -h
```

```console
usage: pwgen [-h] [-e] {password,passphrase,token,url-token} ...

Generate cryptographically strong random passwords, phrases, and url tokens

optional arguments:
-h, --help            show this help message and exit
-e, --entropy         print entropy (default: False)

subcommands:
{password,passphrase,token,url-token}
                        subcommand help
    password            Generate random password
    passphrase          Generate random XKCD-style passphrase
    token               Generate random text string
    url-token           Generate random URL-safe text string
```

## Exmaples

### password

Show the `password` command help

```console
python pwgen.py password -h
```

```console
usage: pwgen password [-h] [-l LENGTH] [-p]

Generate cryptographically strong alphanumeric random password with at least
one lowercase character, at least one uppercase character, and at least one 
digit.

optional arguments:
-h, --help            show this help message and exit
-l LENGTH, --length LENGTH
                        Character length of password (default: 40)
-p, --punctuation     Include punctuation in password (default: False)
```

The following `-e` flag will show the entropy (in bits) of the generated 
password and the number of possible passwords combitions.

```console
python pwgen.py -e password

m2lnVsfigpVMpds5dSvvC1paMcFeGAGBbJ07l5PF
entropy: 238 bits
```

The following `-l` flag changes the length of the generated password, which
must be greater than 13 characters (defaults to 40).

```console
python pwgen.py password -l 13

Password length must be greater than 13 characters
```

The following `-p` flag adds punctuation to the password.

```console
python pwgen.py password -p

v7+6S#]+w`U{z,Gj)$Ec3N2|llL9=Tp_O9S3~5k_
```

### passphrase

Show the `passphrase` command help

```console
python pwgen.py passphrase -h
```

```console
usage: pwgen passphrase [-h] [-l LENGTH] [-d] [-f FILE]

Generate a XKCD-style passphrase from randomly selected words from a word-list 
file. On standard Linux systems, it searches in common locations for word files 
to use. Other platforms may need to provide their own word-list. If -d, --delimiter 
is used, then selected words are randomly chosen to be uppercase or lowercase; 
otherwise selected words are Proper Case.

optional arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        Number of words in passphrase (default: 5)
  -d, --delimiter       Delimiter to separate words in passphrase (default: False)
  -f FILE, --file FILE  Word file used to generate passphrase (default: None)
```

Use the `passphrase` command to generate an XKCD-style passphrase with each word
capitolized.

```console
python pwgen.py passphrase

Maestricht_MonitorDullnessWarproofLighteReotrope
```

Use the `-d` flag to generate a passphrase with delimiter between words. Words
are randomnly chosen to be upper or lower case

```console
python pwgen.py passphrase -d

QUARTET-dearn-imperial-oysterling-INDISSOLVABLE
```

### token

```console
python pwgen.py token -h
```

```console
usage: pwgen token [-h] [-l LENGTH]

Generate a random text string, in hexadecimal, with a minimum of 256 bits 
of randomness. The string has nbytes random bytes, each byte converted to 
two hex digits.

optional arguments:
-h, --help            show this help message and exit
-l LENGTH, --length LENGTH
                        Number of random bytes in token (default: 32)
```

Use the `token` command to generate a random token

```console
python pwgen.py token

37de209adf682d65b840672c746eb9f1b2ebc8deeb9c1ababa44d98ea60c11d8
```

### url token

```console
python pwgen.py url-token -h
```

```console
usage: pwgen url-token [-h] [-l LENGTH]

Generate a random, hard-to-guess URL-safe text string with a minimum of 256 
bits of randomness. Could be used as a security token, for example, 
suitable for password recovery applications.

optional arguments:
-h, --help            show this help message and exit
-l LENGTH, --length LENGTH
                        Number of random bytes in token (default: 32)
```

Use the `url-token` command to generate a random url-safe token.

```console
python pwgen.py url-token

oqBVWR7e3strkqmh5TI5vJTJ1X6lCnMl5NTWUpLUZr4
```