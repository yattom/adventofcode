package main

import "testing"

func TestParse(t *testing.T) {
	t.Run("simple and non loop", func(t *testing.T) {
		t.Run("starting position", func(t *testing.T) {
			puzzleInput := []string{"---", "JS-", ".J|"}
			start, _ := Parse(puzzleInput)

			if start.Coordinate != (Coordinate{1, 1}) {
				t.Errorf("got %v", start)
			}
		})
		t.Run("connections from start", func(t *testing.T) {
			puzzleInput := []string{"---", "JS-", ".J|"}
			start, _ := Parse(puzzleInput)

			if start.Connection[0] != (Coordinate{1, 2}) {
				t.Errorf("got %v", start.Connection[0])
			}
			if start.Connection[1] != (Coordinate{2, 1}) {
				t.Errorf("got %v", start.Connection[1])
			}
		})
	})
	t.Run("complex and includes non-main-loop pipes", func(t *testing.T) {
		puzzleInput := []string{
			"7-F7-",
			".FJ|7",
			"SJLL7",
			"|F--J",
			"LJ.LJ",
		}
		start, pipes := Parse(puzzleInput)
		farthest := Farthest(start, pipes)

		if farthest != 8 {
			t.Errorf("got %v", farthest)
		}
	})
	t.Run("test how structure is passed to function", func(t *testing.T) {
		sut := MyStruct{10, make(map[string]int)}
		ModiftStruct(sut)

		if sut.Value != 10 {
			t.Errorf("got %v", sut.Value)
		}
		if sut.Map["key"] != 100 {
			t.Errorf("got %v", sut.Map["key"])
		}
	})
}

type MyStruct struct {
	Value int
	Map map[string]int
}

func ModiftStruct(val MyStruct) {
	val.Value += 1
	val.Map["key"] = 100
}
