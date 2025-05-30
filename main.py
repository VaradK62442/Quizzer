import json
import random
import math
import sys
import os
from glob import glob
from datetime import datetime
from collections import defaultdict

from similarityChecker import mark_answer


class Colours:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    ORANGE = '\033[93m'
    END = '\033[0m'


def print_results(data, user_answers, user_data):
    COLUMN_WIDTH = 60
    TABLE_WIDTH = COLUMN_WIDTH * 3

    def get_result_string(strings, correct, score):
        def process_string(s, result):
            offset = s[0]
            s = s[1].split()
            result = append_till_full(result, s, offset=offset)
            return result

        def append_till_full(result, words, offset=1):
            for word in words:
                if len(result) + len(word) <= COLUMN_WIDTH * offset:
                    result += word + ' '
                else:
                    break

            result = result.ljust((COLUMN_WIDTH + 1) * offset)
            if offset < 3:
                result += '|'
            return result

        result = ''
        for i, s in enumerate(strings):
            result = process_string((i + 1, s), result)

        print(f"{Colours.GREEN if correct else Colours.RED}{result}[{round(score, 4)}]{Colours.END}")

    def reset_string(s):
        size = 0
        last_word = -1
        for i, word in enumerate(s.split()):
            if size + len(word) <= COLUMN_WIDTH:
                size += len(word) + 1
                last_word = i
            else:
                break
        return ' '.join(s.split()[last_word + 1:])

    reset_strings = lambda strings: [reset_string(s) for s in strings]
    check_size = lambda strings: any([len(s) > COLUMN_WIDTH for s in strings])

    print("-" * (COLUMN_WIDTH + 2))
    print(f'You answered {user_data["questions_answered"]} out of {user_data["total_questions"]} questions'.ljust(COLUMN_WIDTH + 1) + "|")
    print(f'You got {user_data["correct_answers"]} out of {user_data["questions_answered"]} correct'.ljust(COLUMN_WIDTH + 1) + "|")
    print(f'Time taken: {datetime.now() - user_data["start_time"]}'.ljust(COLUMN_WIDTH + 1) + "|")
    print("-" * TABLE_WIDTH)

    print('Question'.ljust(COLUMN_WIDTH + 1) + '|Actual Answer'.ljust(COLUMN_WIDTH + 1) + '|Your Answer'.ljust(COLUMN_WIDTH + 1))
    print('-' * TABLE_WIDTH)

    for question in data:
        strings = [question['question'], question['answer'], user_answers[question['question']]]
        correct, score = mark_answer(question['answer'], user_answers[question['question']])

        while check_size(strings):
            get_result_string(strings, correct, score)
            strings = reset_strings(strings)
        get_result_string(strings, correct, score)
        print('-' * TABLE_WIDTH)


def setup():
    GLOB_PATH = "quizFiles/**/*.json"  # Recursive pattern

    print(f"{Colours.BLUE}QUIZZER{Colours.END}")
    print("\nSETUP\n")

    file_paths = glob(GLOB_PATH, recursive=True)

    # Group files by folder
    grouped_files = defaultdict(list)
    for path in file_paths:
        rel_path = path.replace("quizFiles/", "")
        folder = os.path.dirname(rel_path) or "Root"
        grouped_files[folder].append(path)

    # Display files grouped by folder, and store index -> path map
    file_index_map = {}
    index = 1
    for folder in sorted(grouped_files):
        print(f"\n{Colours.ORANGE}{folder}{Colours.END}")
        for file in sorted(grouped_files[folder]):
            rel_file = file.replace("quizFiles/", "")
            print(f"[{index}] {rel_file}")
            file_index_map[index] = file
            index += 1

    def get_valid_input(prompt: str, min_val: int, max_val: int):
        validate_input_digit = lambda inp, minv, maxv: inp.isdigit() and (minv <= int(inp) <= maxv)
        user_input = input(prompt)
        while not validate_input_digit(user_input, min_val, max_val):
            user_input = input(prompt)
        return int(user_input)

    fileIndex = get_valid_input('\nSelect a file: ', 1, len(file_index_map))

    data = []
    with open(file_index_map[fileIndex]) as f:
        data = json.load(f)

    range = (0, len(data))
    if len(sys.argv) > 2 and sys.argv[1].isdigit() and sys.argv[2].isdigit():
        range = (
            math.floor(int(sys.argv[1]) / 100 * len(data)),
            math.floor(int(sys.argv[2]) / 100 * len(data))
        )

    data = data[range[0]:range[1]]

    print("\n[1] In-order\n[2] Shuffled\n")
    inOrder = get_valid_input('Select an ordering: ', 1, 2)
    if inOrder != 1:
        random.shuffle(data)

    numberOfQuestions = int(get_valid_input(f"\nSelect a number of questions from 1 to {len(data)}: ", 1, len(data))) if len(data) > 1 else 1

    return numberOfQuestions, data


def main():
    numberOfQuestions, data = setup()
    startTime = datetime.now()

    user_answers = {}
    user_data = {
        'questions_answered': 0,
        'total_questions': numberOfQuestions,
        'correct_answers': 0,
        'start_time': startTime,
    }

    print("\nQUESTIONS\n")
    for index, question in enumerate(data[:numberOfQuestions]):
        print(f"{index + 1}) {question['question']}")
        user_answer = input('Your answer: ')
        user_answers[question['question']] = user_answer
        user_data['questions_answered'] += len(user_answer) and 1

        correct, score = mark_answer(question['answer'], user_answers[question['question']])
        user_data['correct_answers'] += 1 if correct else 0

        print(f"{Colours.GREEN if correct else Colours.RED}Correct answer was: {question['answer']} [{round(score, 4)}]{Colours.END}\n")

    print("\nRESULTS\n")
    print_results(data[:numberOfQuestions], user_answers, user_data)


if __name__ == '__main__':
    main()