import re

from trigger_conditional_putter import TriggerConditionalPutter


triggers = []

def file_could_not_be_found(file: str):
    print(f"The {file} file could not be found.")


def read_triggers_from_file(file: str):
    condition = "WHEB_USUARIO_PCK.GET_IE_EXECUTAR_TRIGGER = 'S'"
    try:
        with open(file, 'r', encoding='utf-8') as f:
            split_triggers = re.split(r'/\s*endoffile', f.read())
            split_triggers.pop()
            for trigger in split_triggers:
                if trigger: triggers.append(TriggerConditionalPutter(trigger)
                                .add_condition(condition) + '\n/')
    except FileNotFoundError:
        file_could_not_be_found(file)


def write_triggers(file: str):
    try:
        with open(file, "w", encoding='utf-8') as f:
            for trigger in triggers:
                f.write("".join(trigger) + "\n\n")
    except FileNotFoundError:
        file_could_not_be_found(file)


if __name__ == "__main__":
    read_triggers_from_file("triggers.txt")
    write_triggers("output.txt")
    print("done")
