package main
import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

type Coordinate struct {
	X int
	Y int
}

type Pipe struct {
	Type       rune
	Coordinate Coordinate
	Connection []Coordinate
}

type NeighborType func(coord Coordinate) Coordinate

func NorthOf(coord Coordinate) Coordinate {
	return Coordinate{coord.X, coord.Y - 1}
}

func SouthOf(coord Coordinate) Coordinate {
	return Coordinate{coord.X, coord.Y + 1}
}

func EastOf(coord Coordinate) Coordinate {
	return Coordinate{coord.X + 1, coord.Y}
}

func WestOf(coord Coordinate) Coordinate {
	return Coordinate{coord.X - 1, coord.Y}
}

var pipeTypes = map[int32][]NeighborType{
	'|': []NeighborType{NorthOf, SouthOf},
	'-': []NeighborType{EastOf, WestOf},
	'L': []NeighborType{NorthOf, EastOf},
	'J': []NeighborType{NorthOf, WestOf},
	'F': []NeighborType{SouthOf, EastOf},
	'7': []NeighborType{SouthOf, WestOf},
	'.': []NeighborType{},
}

func Parse(puzzleInput []string) (start Pipe, area map[Coordinate]Pipe) {
	area = make(map[Coordinate]Pipe)
	// find the start pipe
	// loop through puzzle_input
	for y, s := range puzzleInput {
		for x, c := range s {
			if c == '.' {
				continue
			}
			here := Coordinate{x, y}
			pipe := Pipe{c, here, []Coordinate{}}
			if c == 'S' {
				start = pipe
			} else {
				for _, n := range pipeTypes[c] {
					pipe.Connection = append(pipe.Connection, n(here))
				}
			}
			area[here] = pipe
		}
	}

	for _, n := range []NeighborType{NorthOf, SouthOf, EastOf, WestOf} {
		where, exist := area[n(start.Coordinate)]
		if exist {
			for _, c := range where.Connection {
				if c == start.Coordinate {
					start.Connection = append(start.Connection, where.Coordinate)
				}
			}
		}
	}

	return
}

type Head struct {
	Here Pipe
	Visited map[Coordinate]bool
}

func Farthest(start Pipe, pipes map[Coordinate]Pipe) int {
	head1 := Head{pipes[start.Connection[0]], map[Coordinate]bool{start.Coordinate: true}}
	head2 := Head{pipes[start.Connection[1]], map[Coordinate]bool{start.Coordinate: true}}
	step := 1
	for {
		head1.Here = MoveHead(head1, pipes)
		head2.Here = MoveHead(head2, pipes)
		step += 1

		if head1.Here.Coordinate == head2.Here.Coordinate {
			return step
		}
	}
	return -1
}

func MoveHead(head Head, pipes map[Coordinate]Pipe) (next Pipe) {
	head.Visited[head.Here.Coordinate] = true
	if head.Visited[head.Here.Connection[0]] {
		next = pipes[head.Here.Connection[1]]
	} else {
		next = pipes[head.Here.Connection[0]]
	}
	return
}


func main() {
    // ファイルを開く
    file, err := os.Open("puzzle_input.txt")
    if err != nil {
        panic(err)
    }
    defer file.Close()

    var lines []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()           // 1行読み込む
        line = strings.TrimSpace(line)   // 改行を取り除く
        lines = append(lines, line)      // スライスに追加する
    }

    if err := scanner.Err(); err != nil {
        panic(err)
    }

	start, pipes := Parse(lines)
	farthest := Farthest(start, pipes)

	fmt.Println(farthest)
}
