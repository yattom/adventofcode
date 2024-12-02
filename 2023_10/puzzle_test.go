package main

import "testing"

func TestParse(t *testing.T) {
	t.Run("simple and non loop", func(t *testing.T) {
		t.Run("starting position", func(t *testing.T) {
			puzzleInput := []string{"---", "JS-", ".J|"}
			start, _, _, _ := Parse(puzzleInput)

			if start.Coordinate != (Coordinate{1, 1}) {
				t.Errorf("got %v", start)
			}
		})
		t.Run("connections from start", func(t *testing.T) {
			puzzleInput := []string{"---", "JS-", ".J|"}
			start, _, _, _ := Parse(puzzleInput)

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
		start, pipes, _, _ := Parse(puzzleInput)
		farthest, _ := Farthest(start, pipes)

		if farthest != 8 {
			t.Errorf("got %v", farthest)
		}
	})
}

func TestCountInside(t *testing.T) {
	t.Run("paint outside", func(t *testing.T) {
		puzzleInput := []string{
			"7-F7-",
			".FJ|7",
			"SJLL7",
			"|F--J",
			"LJ.LJ",
		}
		start, pipes, maxX, maxY := Parse(puzzleInput)
		_, loop := Farthest(start, pipes)
		outside := PaintOutside(loop, maxX, maxY)

		if len(outside) != 8+6*4 {
			t.Errorf("got %v", len(outside))
			t.Errorf("got %v", outside)
		}
	})

	t.Run("paint outside", func(t *testing.T) {
		puzzleInput := []string{
			"7-F7-",
			".FJ|7",
			"SJLL7",
			"|F--J",
			"LJ.LJ",
		}
		start, pipes, maxX, maxY := Parse(puzzleInput)
		_, loop := Farthest(start, pipes)
		outside := PaintOutside(loop, maxX, maxY)

		if len(outside) != 8+6*4 {
			t.Errorf("got %v", len(outside))
			t.Errorf("got %v", outside)
		}
	})

}

func TestStruct(t *testing.T) {
	t.Run("test how structure is passed to function", func(t *testing.T) {
		sut := MyStruct{10, make(map[string]int)}
		ModifyStruct(sut)

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
	Map   map[string]int
}

func ModifyStruct(val MyStruct) {
	val.Value += 1
	val.Map["key"] = 100
}
