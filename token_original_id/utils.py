from re import search
from pathlib import Path


def load_csv(file_path: str) -> list[str]:
    with Path(file_path).open(mode="r") as file:
        return file.read().strip().splitlines()


def save_csv(file_path: str, csv: str) -> None:
    with Path(file_path).open(mode="w") as file:
        file.write(csv)


def sort_lines(csv_lines: list[str]) -> list[str]:
    [header_line, *body_lines] = csv_lines
    return [header_line, *sorted(body_lines)]

def lint_address(csv_lines: list[str]) -> list[str]:
    [header_line, *body_lines] = csv_lines
    res = [header_line]
    for body_line in body_lines:
        s = body_line.split(",")
        s[2] = s[2].lower()
        res.append(",".join(s))
    return res


def check_whitespaces(csv_lines: list[str]) -> None:
    for idx, line in enumerate(csv_lines):
        if search("\s", line):
            raise Exception(f"Line:{idx+1}: whitespace included")


def check_duplication(csv_lines: list[str]) -> None:
    if len(csv_lines) != len(set(csv_lines)):
        raise Exception("Lines duplicated")


def check_value_format(csv_lines: list[str]) -> None:
    for idx, line in enumerate(csv_lines):
        [uti, platform, original_id] = line.split(",")
        if uti == original_id and platform != "":
            raise Exception(f"Line:{idx+1}: platform should be empty where uti equals original_id")
        if uti != original_id and platform == "":
            raise Exception(f"Line:{idx+1}: platform should not be empty where uti not equals original_id")
