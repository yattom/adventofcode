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

func Parse(puzzleInput []string) (start Pipe, area map[Coordinate]Pipe, maxX int, maxY int) {
	area = make(map[Coordinate]Pipe)
	maxX = 0
	maxY = 0
	// find the start pipe
	// loop through puzzle_input
	for y, s := range puzzleInput {
		if y > maxY {
			maxY = y
		}
		for x, c := range s {
			if y > maxX {
				maxX = y
			}
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
	Here    Pipe
	Visited map[Coordinate]bool
}

func Farthest(start Pipe, pipes map[Coordinate]Pipe) (int, map[Coordinate]bool) {
	head1 := Head{pipes[start.Connection[0]], map[Coordinate]bool{start.Coordinate: true}}
	head2 := Head{pipes[start.Connection[1]], map[Coordinate]bool{start.Coordinate: true}}
	step := 1
	for {
		head1.Here = MoveHead(head1, pipes)
		head2.Here = MoveHead(head2, pipes)
		step += 1

		if head1.Here.Coordinate == head2.Here.Coordinate {
			loop := map[Coordinate]bool{head1.Here.Coordinate: true}
			for k, v := range head1.Visited {
				loop[k] = v
			}
			for k, v := range head2.Visited {
				loop[k] = v
			}
			return step, loop
		}
	}
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

func PaintOutside(loop map[Coordinate]bool, maxX int, maxY int) (outside map[Coordinate]bool) {
	outside = map[Coordinate]bool{}
	toVisit := []Coordinate{{X: 0, Y: 0}}

	for {
		if len(toVisit) == 0 {
			break
		}
		here := toVisit[0]
		toVisit = toVisit[1:]
		if outside[here] {
			continue
		}
		outside[here] = true
		for _, n := range []NeighborType{NorthOf, SouthOf, EastOf, WestOf} {
			neighbor := n(here)
			// if neighbor is outside the puzzle, skip
			// make 1 width margin outside the actual area
			if neighbor.X < -1 || neighbor.X > maxX+1 || neighbor.Y < -1 || neighbor.Y > maxY+1 {
				continue
			}

			if !loop[neighbor] && !outside[neighbor] {
				toVisit = append(toVisit, neighbor)
			}
		}
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
		line := scanner.Text()         // 1行読み込む
		line = strings.TrimSpace(line) // 改行を取り除く
		lines = append(lines, line)    // スライスに追加する
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}

	start, pipes, _, _ := Parse(lines)
	farthest, _ := Farthest(start, pipes)

	fmt.Println(farthest)
}
