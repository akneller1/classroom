# Provisional item format: `"format": "plot"` (drag-and-drop graphing)

Status: **provisional**. Claude proposed it on Nov 15, and the user approved drag-and-drop for all grades. Codex owns the final schema, widget, and checker. If you change field names, keep the meaning so the items in this package can be migrated mechanically.

## Item shape (an addition to schemaVersion 1)

```json
{
  "id": "alg1-rf-s10-cp1-p004", "skillId": "relations-functions-skill-10", "level": "cp1",
  "format": "plot",
  "prompt": "Graph y = −|x − 2| + 3. Drag the vertex first, then drag a second point on the graph.",
  "answer": "y = −|x − 2| + 3; vertex (2, 3); passes through (3, 2)",      // human-readable, for keys and printables
  "solutionSteps": ["…"], "standards": ["F-IF.C.7b"], "sourceNotes": "…",
  "plot": {
    "tool": "abs",                                   // see the tools table
    "grid": {"xmin": -8, "xmax": 8, "ymin": -8, "ymax": 8, "step": 1, "snap": 1},   // or "numberLine": {...}
    "target": {"a": "-1", "h": 2, "k": 3},          // numbers as JSON numbers or exact fraction strings
    "check": {"type": "exact-after-snap"},
    "feedback": {"h-sign": "Check the horizontal shift: …", "...": "…"},
    "testVectors": {"correct": {"anchor": [2, 3], "point": [3, 2]},
                    "wrong": [{"response": {"anchor": [-2, 3], "point": [3, 2]}, "expectCode": "h-sign"}]},
    "answerKey": {"src": "question-banks/assets/plot-keys/abs-123.png", "alt": "…"}
  }
}
```

The production adapter currently accepts only four formats (`question-bank-adapter.js` line 9). Add `"plot"`. Then add a rule for consumers that cannot render it: treat it as **print-only** (Worksheet/Assessment generators print the prompt on a blank grid, with `answerKey.src` on the teacher key), or skip it in text-only games (Connect 4, Tic-Tac-Toe).

## Tools and the response each widget records

| tool | What the student does | response | target |
|---|---|---|---|
| `number-line-point` | drag 1+ dots onto ticks | `{"values": ["3/4"]}` | `{"values": [...]}` |
| `points` | drop labeled points on the grid | `{"points": [[x,y], …]}` (order-free) | `{"points": [...]}` |
| `number-line-inequality` | set the boundary, toggle open/closed, choose the arrow direction | `{"boundary":v,"closed":bool,"direction":"left"\|"right"}` | same |
| (compound) | two boundaries + "between" or "outside" | `{"between":bool,"left":{"value","closed"},"right":{…}}` | same |
| `line` | drag 2 points | `{"points": [[x1,y1],[x2,y2]]}` | `{"m":"1/2","b":"-3"}` |
| `system` | two lines + the intersection | `{"lines":[[p,q],[p,q]],"solution":[x,y]}` (line order = equation order) | `{"lines":[{m,b},{m,b}],"solution":[x,y]}` |
| `region` | 2 points + dashed/solid + shade side | `{"points":[p,q],"dashed":bool,"shade":"above"\|"below"}` | `{"m","b","op"}` |
| `abs`, `parabola`, `sqrt`, `cbrt` | drag the vertex/start/center, then a second point; the widget draws the curve through them | `{"anchor":[h,k],"point":[x,y]}` | `{"a","h","k"}` |
| `exponential` | drag 2 points; the widget draws y = a·bˣ through them | `{"points":[p,q]}` | `{"a","b"}` |

All responses are recorded **after snapping** (integer grid, or the number-line tick). The check is exact, using rational arithmetic, because snapping removes rounding error.

## Error codes (→ `plot.feedback`)

`position, count, swapped-coordinates, boundary, direction, closed-open, and-or, same-point, intercept, slope-sign, slope-reciprocal, slope, points-off-curve, h-sign, k-sign, swapped-hk, anchor, same-x, a-sign, stretch, boundary-line, dashed-solid, shade-side, solution, line-*`.

The detection order is defined in `plot_check_reference.py`. The JS port must return the same code for every `testVectors.wrong` entry: 1,177 vectors across 413 items, all passing in Python.

## Widget requirements (acceptance)

- Works with mouse, touch (375 px phones), and keyboard: arrow keys move the selected point by one snap step, Tab switches points, and Enter submits. Points announce their coordinates to screen readers ("Point A at negative 2, 3").
- Uses the Classroom graph style (`core/graph.js`): integer grid, axes labeled every 2, closed dots filled, open dots ringed.
- After the student submits, it shows the feedback message for the returned code. After 2 misses, it can show the `solutionSteps` and draw the answer key.
- Student links (`student=1`) and Picture Reveal/Practice Test can use plot items. Showdown shows the item on the projector, and the teacher reveals `answerKey`.
