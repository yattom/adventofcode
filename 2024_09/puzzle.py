class Drive:
    def __init__(self):
        self.empty_blocks = []
        self.file_blocks = []
        self.block_index = 0
        self.file_id_index = 0

    def add_empty_block(self, length: int):
        if length == 0:
            return
        self.empty_blocks.append((self.block_index, length))
        self.block_index += length

    def add_file_block(self, length: int):
        self.file_blocks.append((self.file_id_index, self.block_index, length))
        self.file_id_index += 1
        self.block_index += length

    @staticmethod
    def calculate_checksum(file_id, block_index, length) -> int:
        return file_id * length * (block_index + block_index + length - 1) // 2

    def rearrange_and_checksum(self) -> int:
        checksum = 0
        empty = self.empty_blocks.pop(0)
        for file_id, block_index, length in self.file_blocks[::-1]:
            while length > 0:
                if block_index < empty[0] or not empty:
                    # print(f'{file_id=} {block_index=} {length=} checksum={self.calculate_checksum(file_id, block_index, length)}')
                    checksum += self.calculate_checksum(file_id, block_index, length)
                    length = 0
                elif empty[1] >= length:
                    # print(f'{file_id=} {empty[0]=} {length=} checksum={self.calculate_checksum(file_id, empty[0], length)}')
                    checksum += self.calculate_checksum(file_id, empty[0], length)
                    empty = empty[0] + length, empty[1] - length
                    length = 0
                else:
                    # print(f'{file_id=} {empty[0]=} {empty[1]=} {length=} checksum={self.calculate_checksum(file_id, empty[0], empty[1])}')
                    checksum += self.calculate_checksum(file_id, empty[0], empty[1])
                    length -= empty[1]
                    empty = self.empty_blocks.pop(0) if self.empty_blocks else None

        return checksum

    def move_file_and_checksum(self) -> int:
        checksum = 0
        empty_blocks = self.empty_blocks[:]
        for file_id, block_index, length in self.file_blocks[::-1]:
            for empty_idx, empty in enumerate(empty_blocks):
                if block_index > empty[0] and empty[1] >= length:
                    checksum += self.calculate_checksum(file_id, empty[0], length)
                    empty_blocks[empty_idx] = empty[0] + length, empty[1] - length
                    break
            else:
                checksum += self.calculate_checksum(file_id, block_index, length)

        return checksum


def puzzle1(lines: list[str]):
    drive = Drive()
    for i, c in enumerate(lines[0].strip()):
        if i % 2 == 0:
            drive.add_file_block(int(c))
        else:
            drive.add_empty_block(int(c))

    return drive.rearrange_and_checksum()


def puzzle2(lines: list[str]):
    drive = Drive()
    for i, c in enumerate(lines[0].strip()):
        if i % 2 == 0:
            drive.add_file_block(int(c))
        else:
            drive.add_empty_block(int(c))

    return drive.move_file_and_checksum()



def main():
    import sys
    if len(sys.argv) == 1:
        lines = sys.stdin.readlines()
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    print(puzzle1(lines))
    print(puzzle2(lines))


if __name__ == "__main__":
    main()
