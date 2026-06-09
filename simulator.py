#!/usr/bin/env python3
"""
Particle Life Simulator Engine

Handles physics calculations and particle updates.
"""

import numpy as np
import pygame
from particle import Particle


class ParticleLifeSimulator:
    """Main simulator class for particle life dynamics."""
    
    def __init__(self, width, height, config, num_particles=100):
        """
        Initialize the simulator.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            config: Configuration dictionary with species and parameters
            num_particles: Number of particles to create
        """
        self.width = width
        self.height = height
        self.config = config
        
        # Parse species
        self.species = config.get('species', [])
        if not self.species:
            self.species = [
                {'name': 'Red', 'color': [255, 0, 0]},
                {'name': 'Green', 'color': [0, 255, 0]},
                {'name': 'Blue', 'color': [0, 0, 255]}
            ]
        
        # Parse interaction matrix
        interaction_matrix = config.get('interaction_matrix', [])
        if not interaction_matrix:
            # Default: weak same-species attraction
            n = len(self.species)
            interaction_matrix = [[0.1 if i == j else -0.05 for j in range(n)] for i in range(n)]
        
        self.interaction_matrix = np.array(interaction_matrix, dtype=float)
        
        # Simulation parameters
        params = config.get('parameters', {})
        self.interaction_radius = params.get('interaction_radius', 80.0)
        self.force_strength = params.get('force_strength', 0.1)
        self.friction_damping = params.get('friction_damping', 0.98)
        self.softening_distance = params.get('softening_distance', 5.0)
        self.particle_radius = params.get('particle_radius', 3)
        
        # Initialize particles
        self.particles = []
        self._create_particles(num_particles)
        
        # Store initial config for reset
        self.initial_config = config.copy()
        self.initial_num_particles = num_particles
    
    def _create_particles(self, num_particles):
        """Create particles with random positions and velocities."""
        self.particles = []
        num_species = len(self.species)
        
        for _ in range(num_particles):
            # Random position
            pos = np.array([
                np.random.uniform(0, self.width),
                np.random.uniform(0, self.height)
            ], dtype=float)
            
            # Random velocity
            vel = np.array([
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1)
            ], dtype=float)
            
            # Random species
            species = np.random.randint(0, num_species)
            
            # Create particle
            particle = Particle(pos, vel, species)
            self.particles.append(particle)
    
    def compute_forces(self):
        """
        Compute forces on all particles.
        
        Returns:
            List of force vectors for each particle
        """
        n = len(self.particles)
        forces = [np.zeros(2, dtype=float) for _ in range(n)]
        
        # For each particle
        for i in range(n):
            p1 = self.particles[i]
            
            # Check interaction with all other particles
            for j in range(n):
                if i == j:
                    continue
                
                p2 = self.particles[j]
                
                # Vector from p1 to p2
                diff = p2.pos - p1.pos
                dist_sq = np.dot(diff, diff)
                dist = np.sqrt(dist_sq)
                
                # Check if within interaction radius
                if dist > self.interaction_radius or dist < 0.1:
                    continue
                
                # Get interaction strength from matrix
                interaction = self.interaction_matrix[p1.species, p2.species]
                
                if interaction == 0:
                    continue
                
                # Calculate force using inverse square law with softening
                softened_dist = dist + self.softening_distance
                force_magnitude = interaction * self.force_strength / (softened_dist ** 2)
                
                # Direction vector
                if dist > 0:
                    direction = diff / dist
                    forces[i] += direction * force_magnitude
        
        return forces
    
    def update(self, dt):
        """
        Update particle positions and velocities.
        
        Args:
            dt: Time delta in seconds
        """
        # Compute forces
        forces = self.compute_forces()
        
        # Update each particle
        for particle, force in zip(self.particles, forces):
            # Update velocity with force
            particle.vel += force * dt
            
            # Apply friction/damping
            particle.vel *= self.friction_damping
            
            # Update position
            particle.pos += particle.vel * dt
            
            # Handle boundaries (wrap around)
            particle.pos[0] %= self.width
            particle.pos[1] %= self.height
    
    def draw(self, screen):
        """
        Draw all particles on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        for particle in self.particles:
            color = self.species[particle.species]['color']
            pos = particle.pos.astype(int)
            pygame.draw.circle(screen, color, pos, self.particle_radius)
    
    def reset(self):
        """Reset simulator to initial state."""
        self._create_particles(self.initial_num_particles)
        self.force_strength = self.initial_config.get('parameters', {}).get('force_strength', 0.1)
        self.interaction_radius = self.initial_config.get('parameters', {}).get('interaction_radius', 80.0)
        self.friction_damping = self.initial_config.get('parameters', {}).get('friction_damping', 0.98)
    
    def get_stats(self):
        """Get simulation statistics."""
        stats = {
            'total_particles': len(self.particles),
            'particles_by_species': {},
            'interaction_radius': self.interaction_radius,
            'force_strength': self.force_strength,
            'friction_damping': self.friction_damping
        }
        
        # Count particles by species
        for species_info in self.species:
            species_name = species_info['name']
            count = sum(1 for p in self.particles if p.species == self.species.index(species_info))
            stats['particles_by_species'][species_name] = count
        
        return stats
