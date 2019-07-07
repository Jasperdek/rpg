# Risk plot generator (rpg)

This tool takes a CSV file with your observations and outputs either a ring plot, or grid plot.

## Rationale

I was fed-up with having to manually create these graphs for a client and I wanted to make my life easier.
And since I want to increase my Python skills some more, this would be a fun little project to catch two birds with one stone.

## Usage

```
$ ./rpg.py -h
usage: rpg.py [-h] [-g] [-d] [-r] -iC INPUT_CSV_FILE [-oP OUTPUT_PNG_FILE]

Converting scanning reports to a tabular format

optional arguments:
  -h, --help            show this help message and exit
  -g, --grid            generate a risk grid plot.
  -d, --donut           generate a risk donut.
  -r, --recommendations
                        generate a risk recommendations plot.
  -iC INPUT_CSV_FILE, --input-csv-file INPUT_CSV_FILE
                        specify an input CSV file (e.g. data.csv).
  -oP OUTPUT_PNG_FILE, --output-png-file OUTPUT_PNG_FILE
                        specify an output PNG file (e.g. risk.png).
```

## Example

To generate a risk grid plot: `$ ./rpg.py -iC example/input/observations.csv -oP example/output/grid.png -g`

![Risk grid](example/output/grid.png "Risk grid")

To generate a risk donut: `$ ./rpg.py -iC example/input/observations.csv -oP example/output/donut.png -r`

![Risk donut](example/output/donut.png "Risk donut")

To generate a recommendations plot: `$ ./rpg.py -iC example/input/recommendations.csv -oP example/output/ring.png -r`

![Risk recommendations](example/output/recommendations.png "Risk recommendations")

## Dependencies

1. argparse (dev-python/argparse);
2. matplotlib (dev-python/matplotlib);
3. numpy (dev-python/numpy);
4. python (dev-lang/python).

## To do

1. Figure out a way to replace markers with numbers.
2. Figure out a way to plot markers without potentially overlapping.
   The randomise function still causes collisions when adding when plotting multiple markers in the same box.
