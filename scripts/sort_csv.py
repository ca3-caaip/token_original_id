from os import path
from token_original_id.utils import load_csv, save_csv, sort_lines


def sort_csv():
    csv_file = path.join(path.dirname(__file__), "../token_original_id/data.csv")
    lines = load_csv(csv_file)
    updated_lines = sort_lines(lines)
    save_csv(csv_file, "\n".join(updated_lines) + "\n")


if __name__ == '__main__':
    sort_csv()
