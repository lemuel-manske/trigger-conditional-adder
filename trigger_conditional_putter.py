import re


class TriggerConditionalPutter:

    def __init__(self, trigger: str):
        if not trigger:
            raise SyntaxError("Trigger was not provided")
        self.trigger = trigger.strip()

    def add_condition(self, condition: str) -> str:
        begin_index = self.find_trigger_begin_index()
        end_index = self.find_trigger_end_index()

        self.trigger = self.trigger[:end_index] + 'end if;\n' + self.trigger[end_index:]
        self.trigger = self.trigger[:begin_index] + f'begin\nif {condition} then\n' + self.trigger[begin_index:]

        return self.trigger

    def find_trigger_end_index(self) -> int:
        for char in range(len(self.trigger), -1, -1):
            if self.get_end_if_matches(char):
                return char

    def find_trigger_begin_index(self) -> int:
        occurrences = []

        char = 0

        while char < len(self.trigger):
            begin_match = self.get_begin_if_matches(char)
            if begin_match and self.nothing_before(char - 1):
                occurrences.append(char)
                char += begin_match.end()
            else:
                end_match = self.get_end_if_matches(char)
                if end_match:
                    if self.nothing_before(char - 1):
                        try:
                            if not self.is_the_last_end(char, end_match):
                                occurrences.pop()
                            char += end_match.end()
                        except IndexError:
                            self.trigger_could_not_be_read()
                    else:
                        char += 1
                else:
                    char += 1

        if len(occurrences) == 1:
            return occurrences[0]
        else:
            self.trigger_could_not_be_read()

    def trigger_could_not_be_read(self):
        trigger_name_match = re.match("TRIGGER.\S*", self.trigger, re.IGNORECASE)
        trigger_name = trigger_name_match.group() if trigger_name_match else ''
        raise SyntaxError(f"{trigger_name} could not be read")

    def is_the_last_end(self, c: int, end_match):
        return (c + end_match.end()) >= len(self.trigger)

    def get_end_if_matches(self, c: int):
        return re.match(r"END\b(?!.*\bIF\b)(?!.*\bLOOP\b).*?;(?!')", self.trigger[c:], re.IGNORECASE)

    def get_begin_if_matches(self, c: int):
        return re.match(r"BEGIN\b", self.trigger[c:], re.IGNORECASE)

    def nothing_before(self, c: int):
        return re.match(r"\s", self.trigger[c], re.IGNORECASE)