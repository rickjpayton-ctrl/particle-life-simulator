# Particle Life Simulator

A Python-based particle life simulator that visualizes emergent behavior from simple attraction and repulsion forces between different particle types.

## Features

- **Multiple Particle Species**: Create up to 10 different types of particles with customizable interactions
- **Interactive Visualization**: Real-time rendering using Pygame
- **Physics-Based Forces**: Attraction and repulsion governed by distance-based inverse square law
- **Interactive Controls**: 
  - **SPACE**: Pause/Resume simulation
  - **R**: Reset simulation
  - **+/-**: Increase/Decrease force strength
  - **Arrow Up/Down**: Adjust interaction radius
  - **S**: Save current frame as PNG
  - **Q**: Quit
- **Configuration System**: JSON-based configuration for easy customization
- **Performance Optimized**: Efficient force calculations with spatial awareness

## Installation

### Requirements
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/rickjpayton-ctrl/particle-life-simulator.git
cd particle-life-simulator

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Run with default configuration
python main.py

# Run with a specific configuration
python main.py --config configs/three_species.json

# Run with custom parameters
python main.py --particles 200 --width 1024 --height 768
```

## Configuration

Configurations are stored in JSON format. Each configuration defines:

- **species**: List of particle types (name, color)
- **interaction_matrix**: How each species affects others (attraction/repulsion)
- **parameters**: Simulation parameters (radius, strength, damping, etc.)

### Example Configuration

```json
{
  "species": [
    {"name": "Red", "color": [255, 0, 0]},
    {"name": "Green", "color": [0, 255, 0]},
    {"name": "Blue", "color": [0, 0, 255]}
  ],
  "interaction_matrix": [
    [1, -1, 0],
    [-1, 1, 1],
    [0, -1, 1]
  ],
  "parameters": {
    "interaction_radius": 80,
    "force_strength": 0.1,
    "friction_damping": 0.98,
    "softening_distance": 5.0
  }
}
```

### Creating Your Own Configuration

1. Copy an existing config: `cp configs/three_species.json configs/my_config.json`
2. Edit the interaction matrix:
   - Positive values = attraction
   - Negative values = repulsion
   - Zero = no interaction
3. Adjust species colors and simulation parameters
4. Run: `python main.py --config configs/my_config.json`

## How It Works

### Physics Model

Each particle experiences forces from all other particles within the interaction radius:

```
F = k * direction / (distance + softening)²
```

Where:
- `k` is the interaction strength (from the interaction matrix)
- `direction` is the unit vector from particle A to particle B
- `distance` is the Euclidean distance between particles
- `softening` prevents infinite forces at very close distances

### Simulation Loop

1. **Force Calculation**: For each particle, sum forces from all nearby particles
2. **Velocity Update**: `velocity = (velocity + force * dt) * damping`
3. **Position Update**: `position = position + velocity * dt`
4. **Boundary Handling**: Particles wrap around screen edges
5. **Rendering**: Draw all particles with their species color

## Tips for Interesting Behaviors

- **Flocking**: Use weak attraction between same species
- **Predator-Prey**: Have one species attract/repel others asymmetrically
- **Clustering**: Strong same-species attraction, weak cross-species repulsion
- **Oscillating Groups**: Mix strong attraction and repulsion between species
- **Phase Separation**: High-strength opposite charges with boundary interaction

## Performance Tips

- Reduce particle count for slower systems
- Increase `interaction_radius` to reduce computation
- Adjust `softening_distance` for stability at different force strengths
- Use smaller window size for better performance

## Project Structure

```
.
├── main.py                 # Entry point and simulation loop
├── particle.py             # Particle class definition
├── simulator.py            # Simulation engine and physics
├── config_loader.py        # Configuration management
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── configs/               # Configuration files
    ├── three_species.json
    ├── chaos.json
    ├── predator_prey.json
    └── clusters.json
```

## Customization

### Add More Particles Dynamically

Edit `configs/three_species.json` and increase the number of particles in the particle generation loop (or use the `--particles` flag).

### Change Window Size

```bash
python main.py --width 1920 --height 1080
```

### Export Frames

Press 'S' during simulation to save the current frame. Frames are saved to `screenshots/`.

## Troubleshooting

**"ModuleNotFoundError: No module named 'pygame'"**
- Run `pip install -r requirements.txt`

**Simulation runs slowly**
- Reduce particle count: `python main.py --particles 100`
- Increase interaction radius to skip far-away particles
- Reduce window size

**Particles moving too fast/slow**
- Adjust `force_strength` in configuration
- Modify `friction_damping` (closer to 1.0 = less friction)

## References

- [Particle Life - Original Inspiration](https://www.youtube.com/watch?v=ZQ08F-RAq6w)
- [Tom Mohr's Particle Life](https://github.com/tom-mohr/particle-life)
- [Carykh's Particle Life](https://github.com/carykh/Particle-Life)

## License

MIT License - Feel free to use, modify, and distribute

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
