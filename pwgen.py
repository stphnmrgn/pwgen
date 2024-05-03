#!/usr/bin/env python3
import argparse
import math
from pathlib import Path
import secrets
import string


def entropy(l: int, n: int) -> int:
    """
    Information entropy, measured in bits.

    Parameters
    ----------

    l : int
        the number of symbols in the password
    n : int
        the number of possible symbols

    Returns
    -------
    int
        entropy in bits
    """
    return int(l * math.log2(n))


def generate_password(args) -> str:
    """
    Generate cryptographically strong alphanumeric random password with at least
    one lowercase character, at least one uppercase character, and at least one
    digit.

    Parameters
    ----------
    length : int
        password length
    use_punctuation : bool, optional
        punctuation, by default False

    Returns
    -------
    str
        alphanumeric password

    Raises
    ------
    ValueError
        password length error
    """
    if args.length <= 13:
        raise ValueError("Password length must be greater than 13 characters")

    chars = string.ascii_letters + string.digits
    if args.punctuation:
        chars += "!#$%&()*+,-.:;<=>?@[\\]^_`{|}~"

    while True:
        secret = "".join(secrets.choice(chars) for _ in range(args.length))
        if (
            any(c.islower() for c in secret)
            and any(c.isupper() for c in secret)
            and any(c.isdigit() for c in secret)
        ):
            break
    print(secret)

    if args.entropy:
        l = len(secret)
        # possible symbols = 62 (a–z, A–Z, 0–9), or 91 (a–z, A–Z, 0–9, punctuation)
        n = len(chars)
        e = entropy(l, n)
        print(f"entropy: {e} bits")
        print(f"possible combinations: {float(n**l)}")


def generate_passphrase(args) -> str:
    """
    Generate an XKCD-style passphrase (https://xkcd.com/936)

    Parameters
    ----------
    length : int
        number of words in passphrase

    Returns
    -------
    str
        passphrase

    Raises
    ------
    ValueError
        passphrase length error
    """
    if args.length <= 3:
        raise ValueError("Passphrase must be greater than 3 words")

    if args.file and Path(args.file).is_file() == False:
        raise FileNotFoundError("Word list does not exist")
    elif args.file and Path(args.file).is_file():
        fp = args.file
    elif args.file is None:
        wordlists = (
            "words.txt",
            "/usr/share/dict/words",
            "/usr/dict/words",
            "/etc/dictionaries-common/words",
        )
        fps = [path for path in wordlists if Path(path).is_file()]
        if len(fps) == 0:
            raise FileNotFoundError("Word list not found. Please provide word-list file")
        fp = fps[0]

    if args.delimiter:
        delimiter = secrets.choice(["-", "@", "#", "!", "$", "&"])
        l = args.length + 1
        with open(fp) as f:
            words = [
                secrets.choice((str.upper, str.lower))(word.strip()) for word in f.readlines()
            ]
        # possible delimiter symbols: 6 (-, @, #, !, $, &)
        # possible word symbols: word-list x2 (upper, lower)
        n = (len(words) * 2) + 6
    else:
        delimiter = ""
        l = args.length
        with open(fp) as f:
            words = [word.title().strip() for word in f.readlines()]
        # possible word symbols: word-list
        n = len(words)

    secret = f"{delimiter}".join(secrets.choice(words) for _ in range(args.length))
    print(secret)

    if args.entropy:
        e = entropy(l, n)
        print(f"entropy: {e} bits")
        print(f"possible combinations: {float(n**l)}")


def generate_token(args) -> str:
    """
    Return a random text string, in hexadecimal. The string has nbytes random
    bytes, each byte converted to two hex digits.

    Parameters
    ----------
    length : int
        url length

    Returns
    -------
    str
        Return a random URL-safe text string
    """
    if args.length <= 31:
        raise ValueError("Token length must be greater than 31")

    secret = secrets.token_hex(args.length)
    print(secret)

    if args.entropy:
        l = len(secret)
        # possible symbols for hex: 16
        n = 16
        e = entropy(l, n)
        print(f"entropy: {e} bits")
        print(f"possible combinations: {float(n**l)}")


def generate_token_url(args) -> str:
    """
    Return a random URL-safe text string, containing nbytes random bytes. The
    text is Base64 encoded, so on average each byte results in approximately
    1.3 characters.

    Parameters
    ----------
    length : int
        url length

    Returns
    -------
    str
        Return a random URL-safe text string
    """
    if args.length <= 31:
        raise ValueError("Token length must be greater than 31")

    secret = secrets.token_urlsafe(args.length)
    print(secret)

    if args.entropy:
        l = len(secret)
        # possible symbols for url safe characters: a-z, A-Z, 0-9, and _ -
        n = len(string.ascii_letters) + len(string.digits)
        e = entropy(l, n)
        print(f"entropy: {e} bits")
        print(f"possible combinations: {float(n**l)}")


def main():
    parser = argparse.ArgumentParser(
        prog="pwgen",
        description="Generate cryptographically strong random passwords, phrases, and url tokens",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-e", "--entropy", action="store_true", help="print entropy")

    subparsers = parser.add_subparsers(required=True, title="subcommands", help="subcommand help")

    parser_password = subparsers.add_parser(
        "password",
        help="Generate random password",
        description="""Generate cryptographically strong alphanumeric random 
        password with at least one lowercase character, at least one uppercase 
        character, and at least one digit.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_password.add_argument(
        "-l",
        "--length",
        default=40,
        type=int,
        help="Character length of password",
    )
    parser_password.add_argument(
        "-p",
        "--punctuation",
        action="store_true",
        help="Include punctuation in password",
    )
    parser_password.set_defaults(func=generate_password)

    parser_passphrase = subparsers.add_parser(
        "passphrase",
        help="Generate random XKCD-style passphrase",
        description="""Generate a XKCD-style passphrase from randomly selected
        words from a word-list file. On standard Linux systems, it searches in
        common locations for word files to use. Other platforms may need to 
        provide their own word-list. If -d, --delimiter is used, then selected 
        words are randomly chosen to be uppercase or lowercase; otherwise 
        selected words are Proper Case.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_passphrase.add_argument(
        "-l",
        "--length",
        default=5,
        type=int,
        help="Number of words in passphrase",
    )
    parser_passphrase.add_argument(
        "-d",
        "--delimiter",
        action="store_true",
        help="Delimiter to separate words in passphrase",
    )
    parser_passphrase.add_argument(
        "-f",
        "--file",
        type=str,
        help="Word file used to generate passphrase",
    )
    parser_passphrase.set_defaults(func=generate_passphrase)

    parser_token = subparsers.add_parser(
        "token",
        help="Generate random text string",
        description="""Generate a random text string, in hexadecimal, with a 
        minimum of 256 bits of randomness. The string has nbytes random bytes, 
        each byte converted to two hex digits.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_token.add_argument(
        "-l",
        "--length",
        default=32,
        type=int,
        help="Number of random bytes in token",
    )
    parser_token.set_defaults(func=generate_token)

    parser_token_url = subparsers.add_parser(
        "url-token",
        help="Generate random URL-safe text string",
        description="""Generate a random, hard-to-guess URL-safe text string 
        with a minimum of 256 bits of randomness. Could be used as a security 
        token, for example, suitable for password recovery applications""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_token_url.add_argument(
        "-l",
        "--length",
        default=32,
        type=int,
        help="Number of random bytes in token",
    )
    parser_token_url.set_defaults(func=generate_token_url)

    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, FileNotFoundError) as e:
        print(e)


if __name__ == "__main__":
    main()
