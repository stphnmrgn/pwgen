import argparse
import collections
import math
from pathlib import Path
import secrets
import string


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
    print(secrets.token_hex(args.length))


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
    # byte_length = int(args.length // 1.3)
    print(secrets.token_urlsafe(args.length))


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
        puncuation, by default False

    Returns
    -------
    str
        alphanumeric password

    Raises
    ------
    ValueError
        password length error
    """
    if args.length <= 23:
        raise ValueError("Password length must be greater than 23 characters")
    chars = string.ascii_letters + string.digits
    if args.punctuation:
        chars += string.punctuation
    while True:
        secret = "".join(secrets.choice(chars) for _ in range(args.length))
        if (
            any(c.islower() for c in secret)
            and any(c.isupper() for c in secret)
            and any(c.isdigit() for c in secret)
        ):
            break
    print(secret)


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

    if args.file and Path(args.file).exists() == False:
        raise FileNotFoundError("Word list does not exist")
    elif args.file and Path(args.file).exists():
        fp = args.file
    elif args.file is None:
        wordlists = (
            "words.txt",
            "/usr/share/dict/words",
            "/usr/dict/words",
            "/etc/dictionaries-common/words",
        )
        fps = [path for path in wordlists if Path(path).exists()]
        if len(fps) == 0:
            raise FileNotFoundError("Word list not found. Please provide word-list file")
        fp = fps[0]

    with open(fp) as f:
        words = [secrets.choice((str.upper, str.lower))(word.strip()) for word in f]
    secret = f"{args.delimiter}".join(secrets.choice(words) for _ in range(args.length))
    print(secret)


def entropy(args) -> float:
    """
    Shannon entropy calculation

    Parameters
    ----------
    s : str
        Calculate entropy of string

    Returns
    -------
    float
        entropy
    """
    if args.string is None:
        raise ValueError("String cannot be None. Please provide input string")
    # calculate probability for each byte as number of occurrences / array length
    probabilities = [
        n_x / len(args.string) for x, n_x in collections.Counter(args.string).items()
    ]
    # calculate per-character entropy fractions
    e_x = [-p_x * math.log(p_x, 2) for p_x in probabilities]
    # sum fractions to obtain Shannon entropy
    print(sum(e_x))


def main():
    parser = argparse.ArgumentParser(
        prog="pwgen",
        description="Generate cryptographically strong random passwords, phrases, and url tokens",
    )
    subparsers = parser.add_subparsers(
        required=True, title="subcommands", help="sub-command help"
    )

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
        type=int,
        default=32,
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
        description="""Generate a XKCD-stype passphrase from randomly selected
        words from a word-list file. On standard Linux systems, it searches in
        common locations for word files to use. Other platforms may need to 
        provide their own word-list. The selected words are randomly chosen to 
        be uppercase or lowercase.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_passphrase.add_argument(
        "-l",
        "--length",
        type=int,
        default=4,
        help="Number of words in passphrase, default is 4",
    )
    parser_passphrase.add_argument(
        "-d",
        "--delimiter",
        type=str,
        default="-",
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
        type=int,
        default=32,
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
        type=int,
        default=32,
        help="Number of random bytes in token",
    )
    parser_token_url.set_defaults(func=generate_token_url)

    parser_entropy = subparsers.add_parser("entropy", help="Calculate entropy of string")
    parser_entropy.add_argument(
        "string",
        type=str,
        help="String to calculate entropy from",
    )
    parser_entropy.set_defaults(func=entropy)

    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, FileNotFoundError) as e:
        print(e)


if __name__ == "__main__":
    main()
