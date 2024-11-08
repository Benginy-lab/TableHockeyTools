# TableHockeyTools

**TableHockeyTools** is a Python package designed to gather, analyze, and manipulate data related to Table Hockey. Whether you're tracking player performance, managing scores, or analyzing historical data, TableHockeyTools provides convenient functions to make working with Table Hockey data straightforward.

## Features

- **Data Gathering:** Easily gather data related to Table Hockey players, scores, and statistics.
- **Data Analysis:** Perform calculations, statistics, and summaries on collected data.
- **Customizable Workflows:** Use the modular functions to tailor the package to various Table Hockey-related tasks.
- **Examples Provided:** The `examples` folder demonstrates usage for various functions.

## Installation

Clone this repository and install using `pip`:

```bash
git clone https://github.com/yourusername/TableHockeyTools.git
cd TableHockeyTools
pip install .
```

Alternatively, you can add the package to your project by installing directly from GitHub:

```bash
pip install git+https://github.com/
```

## Usage

Import the package and use the functions as needed:

```python
import THTools as tht

# Example usage
player_names = ['Evigeny Matansev', 'Rainers Kalnins']
player_ids = []
for player_name in player_names:
    player_ids.append(tht.GetPlayerID(player_name))
for player_id, player_name in zip(player_ids, player_names):
    player_points = tht.GetPlayerPoints(player_id)
    print(f"{player_name} has {player_points} points.")
    
```

Check out the `examples` folder for more detailed usage.

## Documentation

For full documentation of functions, see the function docstrings in `mainFunctions` or visit the [online documentation](link-to-documentation) if available.

### Example Functions

- **load_data(file_path):** Load data from a file.
- **calculate_statistics(data):** Calculate statistics on player performance data.
- **manage_scores(scores):** Manage and update scores during a game.
  
Each function is thoroughly documented in `mainFunctions.py` and `examples/`.

## Development

Feel free to contribute! To install the package in development mode:

```bash
pip install -e .
```

### Running Tests

Ensure all functions work as expected by running tests:

```bash
python -m unittest discover tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions, reach out via GitHub issues or contact the maintainer directly.
