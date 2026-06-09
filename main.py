#!/usr/bin/env python3
"""
Particle Life Simulator - Main Entry Point

A Python-based simulation of emergent particle behavior through
attraction and repulsion forces.
"""

import pygame
import numpy as np
import argparse
import os
from datetime import datetime
from simulator import ParticleLifeSimulator
from config_loader import load_config


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Particle Life Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --config configs/chaos.json
  python main.py --particles 500 --width 1280 --height 720
        """
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/three_species.json',
        help='Path to configuration file (default: configs/three_species.json)'
    )
    parser.add_argument(
        '--particles',
        type=int,
        default=None,
        help='Number of particles (overrides config)'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=1200,
        help='Window width in pixels (default: 1200)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=800,
        help='Window height in pixels (default: 800)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=60,
        help='Target frames per second (default: 60)'
    )
    parser.add_argument(
        '--fullscreen',
        action='store_true',
        help='Run in fullscreen mode'
    )
    return parser.parse_args()


def draw_hud(screen, simulator, font, paused, fps):
    """Draw heads-up display with statistics and controls."""
    info_texts = [
        f"Particles: {len(simulator.particles)}",
        f"FPS: {fps:.1f}",
        f"Radius: {simulator.interaction_radius:.1f}",
        f"Strength: {simulator.force_strength:.3f}",
        f"Damping: {simulator.friction_damping:.3f}",
        f"Status: {'PAUSED' if paused else 'RUNNING'}"
    ]
    
    y_offset = 10
    for text in info_texts:
        surface = font.render(text, True, (200, 200, 200))
        screen.blit(surface, (10, y_offset))
        y_offset += 25
    
    # Draw controls
    control_texts = [
        "CONTROLS:",
        "SPACE: Pause/Resume",
        "R: Reset",
        "+/-: Force strength",
        "↑↓: Interaction radius",
        "S: Save screenshot",
        "Q: Quit"
    ]
    
    y_offset = screen.get_height() - 175
    control_font = pygame.font.Font(None, 18)
    for text in control_texts:
        surface = control_font.render(text, True, (150, 150, 150))
        screen.blit(surface, (10, y_offset))
        y_offset += 22


def main():
    """Main simulation loop."""
    args = parse_arguments()
    
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Particle Life Simulator")
    
    # Set up display
    if args.fullscreen:
        screen = pygame.display.set_mode((args.width, args.height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((args.width, args.height))
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)
    
    # Load configuration
    print(f"Loading configuration from {args.config}...")
    config = load_config(args.config)
    
    # Create simulator
    print("Initializing simulator...")
    simulator = ParticleLifeSimulator(
        width=args.width,
        height=args.height,
        config=config,
        num_particles=args.particles or len(config.get('particles', []))
    )
    
    # Create screenshots directory
    os.makedirs('screenshots', exist_ok=True)
    
    # Simulation state
    paused = False
    running = True
    frame_count = 0
    fps_clock = pygame.time.Clock()
    
    print("Starting simulation...")
    print(f"Particles: {len(simulator.particles)}")
    print(f"Species: {len(simulator.species)}")
    print(f"Window: {args.width}x{args.height}")
    print("Press 'H' for help or 'Q' to quit.")
    
    # Main loop
    while running:
        dt = clock.tick(args.fps) / 1000.0  # Convert to seconds
        frame_count += 1
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    simulator.reset()
                    paused = False
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    simulator.force_strength *= 1.1
                elif event.key == pygame.K_MINUS:
                    simulator.force_strength *= 0.9
                elif event.key == pygame.K_UP:
                    simulator.interaction_radius *= 1.1
                elif event.key == pygame.K_DOWN:
                    simulator.interaction_radius *= 0.9
                elif event.key == pygame.K_s:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshots/particle_life_{timestamp}.png"
                    pygame.image.save(screen, filename)
                    print(f"Screenshot saved: {filename}")
        
        # Update simulation
        if not paused:
            simulator.update(dt)
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw particles
        simulator.draw(screen)
        
        # Draw HUD
        current_fps = fps_clock.get_fps()
        draw_hud(screen, simulator, font, paused, current_fps)
        
        # Update display
        pygame.display.flip()
        fps_clock.tick()
    
    print(f"\nSimulation ended. Total frames: {frame_count}")
    pygame.quit()


if __name__ == "__main__":
    main()
