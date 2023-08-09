import argparse
import collections
import math
from pathlib import Path
import secrets
import string


def generate_token(args) -> str:
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
    if args.length <= 8:
        raise ValueError("Token length must be greater than 8")
    byte_length = int(args.length // 1.3)
    print(f"secret: {secrets.token_urlsafe(byte_length)}")


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
    if args.length <= 8:
        raise ValueError("Password length must be greater than 8")
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
    print(f"secret: {secret}")


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
    print(f"secret: {secret}")


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
    print(f"entropy: {sum(e_x)}")


def main():
    parser = argparse.ArgumentParser(
        prog="secret",
        description="Generate cryptographically strong random password",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        required=True, title="subcommands", help="sub-command help"
    )

    parser_password = subparsers.add_parser("password", help="Generate random password")
    parser_password.add_argument(
        "-l",
        "--length",
        type=int,
        default=32,
        help="Character length of password, default is 32",
    )
    parser_password.add_argument(
        "-p",
        "--punctuation",
        action="store_true",
        help="Include punctuation in password, default is False",
    )
    parser_password.set_defaults(func=generate_password)

    parser_passphrase = subparsers.add_parser(
        "passphrase", help="Generate random XKCD-style passphrase"
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
        help="Delimiter to separate words in passphrase, default `-`",
    )
    parser_passphrase.add_argument(
        "-f",
        "--file",
        type=str,
        help="Word file used to generate passphrase",
    )
    parser_passphrase.set_defaults(func=generate_passphrase)

    parser_token = subparsers.add_parser("token", help="Generate random token")
    parser_token.add_argument(
        "-l",
        "--length",
        type=int,
        default=32,
        help="Number of characters in token",
    )
    parser_token.set_defaults(func=generate_token)

    parser_entropy = subparsers.add_parser("entropy", help="Calculate entropy of string")
    parser_entropy.add_argument(
        "string",
        # "--string",
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
