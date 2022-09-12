from os import path
from token_original_id.utils import load_csv, check_whitespaces, check_duplication, check_value_format

def check_csv():
    csv_file = path.join(path.dirname(__file__), "../token_original_id/data.csv")
    lines = load_csv(csv_file)
    check_whitespaces(lines)
    check_duplication(lines)
    check_value_format(lines)


if __name__ == '__main__':
    check_csv()
