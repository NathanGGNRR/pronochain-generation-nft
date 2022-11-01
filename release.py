# -*- coding: utf-8 -*-
r"""
.-----------------------------------------------------.

______                           _           _
| ___ \                         | |         (_)
| |_/ / __ ___  _ __   ___   ___| |__   __ _ _ _ __
|  __/ '__/ _ \| '_ \ / _ \ / __| '_ \ / _` | | '_ \
| |  | | | (_) | | | | (_) | (__| | | | (_| | | | | |
\_|  |_|  \___/|_| |_|\___/ \___|_| |_|\__,_|_|_| |_|


.-----------------------------------------------------.

 _____                           _   _               _   _ ______ _____
|  __ \                         | | (_)             | \ | ||  ___|_   _|
| |  \/ ___ _ __   ___ _ __ __ _| |_ _  ___  _ __   |  \| || |_    | |
| | __ / _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \  | . ` ||  _|   | |
| |_\ \  __/ | | |  __/ | | (_| | |_| | (_) | | | | | |\  || |     | |
 \____/\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_| \_| \_/\_|     \_/


.------------------------------------------------------------------------.

File: release.py
"""
import argparse
import subprocess

from git import Repo

from app.exceptions import PronochainException

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--patch",
        action="store_true",
        help="Nouvelle version patch.",
    )
    parser.add_argument(
        "-mi",
        "--minor",
        action="store_true",
        help="Nouvelle version mineur.",
    )
    parser.add_argument(
        "-ma",
        "--major",
        action="store_true",
        help="Nouvelle version major.",
    )
    args = parser.parse_args()

    additional_args = (
        "--major"
        if args.major
        else "--minor"
        if args.minor
        else "--patch"
        if args.patch
        else ""
    )

    repo = Repo("./")
    git = repo.git
    if git.status("-b").replace("## ", "").split("\n")[0] != "On branch master":
        raise PronochainException("La nouvelle release doit être crée sur master.")

    p = subprocess.Popen(["semantic-release", "version", additional_args])
    (output, _) = p.communicate()
    _ = p.wait()

    current_tag = f'v{subprocess.check_output(["semantic-release", "print-version", "--current"]).decode("utf-8")}'

    with open("CHANGELOG.md", "r", encoding="utf-8") as in_changelog:
        lines = in_changelog.readlines()
        for line in lines:
            if line.startswith(f"## {current_tag}"):
                raise PronochainException(
                    "Le changelog pour cette version a déjà été généré."
                )

    tag_date = subprocess.check_output(
        [f"git show v{current_tag}", '--pretty="%cs"', "--no-patch"]
    ).decode("utf-8")
    tag_date = git.show(current_tag, '--pretty="%cs"', "--no-patch")
    tag_date = tag_date.replace('"', "")

    release_title = f"""## {current_tag} ({tag_date})\n"""
    release_changelog = (
        subprocess.check_output(["semantic-release", "changelog"])
        .decode("ISO-8859-1")
        .replace("https://github.com", "https://dev.azure.com")
    )

    with open("CHANGELOG.md", "a", encoding="utf-8") as changelog:
        for index, line in enumerate(lines):
            if line.startswith("<!--next"):
                lines.insert(
                    index + 1, f"""{release_title}{release_changelog}\n---\n"""
                )
                break
        content = "".join(lines)

    with open("CHANGELOG.md", "w", encoding="utf-8") as changelog:
        changelog.write(content)

    git.add("CHANGELOG.md")
    git.commit("--amend", "--no-edit")
