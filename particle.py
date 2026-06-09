#!/usr/bin/env python3
"""
Particle Class

Defines individual particle behavior and state.
"""

import numpy as np


class Particle:
    """Represents a single particle in the simulation."""
    
    def __init__(self, pos, vel, species):
        """
        Initialize a particle.
        
        Args:
            pos: Initial position as numpy array [x, y]
            vel: Initial velocity as numpy array [vx, vy]
            species: Species index (int)
        """
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.species = species
        self.age = 0
    
    def update_age(self, dt):
        """Update particle age (optional for future features)."""
        self.age += dt
    
    def get_speed(self):
        """Get current speed magnitude."""
        return np.linalg.norm(self.vel)
    
    def reset_velocity(self):
        """Reset velocity to zero."""
        self.vel = np.zeros(2)
    
    def __repr__(self):
        return f"Particle(pos={self.pos}, vel={self.vel}, species={self.species})"
