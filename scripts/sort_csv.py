from os import path
from pathlib import Path


def sort_csv():
    csv_file = Path(path.join(path.dirname(__file__), "../token_original_id/data.csv"))

    header_line: str
    body_lines: list[str]
    with csv_file.open(mode="r") as file:
        [header_line, *body_lines] = file.read().strip().splitlines()

    updated = "\n".join([header_line, *sorted(body_lines)]) + "\n"
    print(header_line)
    print(body_lines)
    print(updated)

    with csv_file.open(mode="w") as file:
        file.write(updated)


if __name__ == '__main__':
    sort_csv()
