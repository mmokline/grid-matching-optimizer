"""
visual_game.py — Interactive Pygame Interface for Matching Game
----------------------------------------------------------------
This script implements the visual interface for the grid matching game.
It supports three modes: 2-player, solo (vs. optimal solver), and vs. AI (Minimax).

Developed as part of ENSAE Paris Programming Project (2025) — Mohamed Iyed Mokline & Olivier de Boissieu
"""

import pygame
from grid import Grid
from solver import *
from minmax import Minmax
data_path = "../input/"

file_name = data_path + "grid06.in"
grid = Grid.grid_from_file(file_name, read_values=True)

# === Initialisation Pygame ===
pygame.init()
cell_size = 100
screen_width = grid.m * cell_size + 100
screen_height = grid.n * cell_size + 200  # Espace pour 2 boutons + scores
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid Pairing Game")
font = pygame.font.SysFont(None, 28)

# === Initialisation AI and solver ===
AI = Minmax(grid)
solver = SolverMaxWeightMatching(grid)

# === Boutons ===
button_terminer = pygame.Rect(10, grid.n * cell_size + 10, 150, 40)
button_annuler = pygame.Rect(10, grid.n * cell_size + 60, 150, 40)
button_mode1 = pygame.Rect(10, grid.n * cell_size + 10, 150, 40)
button_mode2 = pygame.Rect(10, grid.n * cell_size + 60, 150, 40)
button_mode3 = pygame.Rect(10, grid.n * cell_size + 110, 150, 40)
button_color = pygame.Color("gray")
button_hover = pygame.Color("darkgray")

# === Joueurs ===
current_player = 2  # The one who starts: 1 the player, 2 the AI if that mode is chosen
player1_pairs = []
player2_pairs = []

# === Scores ===
user_score_1 = None
user_score_2 = None
winner = ""

# === Fonctions d'affichage ===


def draw_grid():
    for i in range(grid.n):
        for j in range(grid.m):
            x = j * cell_size
            y = i * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)

            color = grid.colors_list[grid.color[i][j]]
            value = grid.value[i][j]
            pygame_color = pygame.Color("white")
            if color == 'r': pygame_color = pygame.Color("red")
            elif color == 'b': pygame_color = pygame.Color("blue")
            elif color == 'g': pygame_color = pygame.Color("green")
            elif color == 'k': pygame_color = pygame.Color("black")

            pygame.draw.rect(screen, pygame_color, rect)
            pygame.draw.rect(screen, pygame.Color("black"), rect, 1)

            text = font.render(str(value), True, pygame.Color("black"))
            screen.blit(text, (x + 5, y + 5))


def draw_pair(cell1, cell2, color):
    x1 = cell1[1] * cell_size + cell_size // 2
    y1 = cell1[0] * cell_size + cell_size // 2
    x2 = cell2[1] * cell_size + cell_size // 2
    y2 = cell2[0] * cell_size + cell_size // 2
    pygame.draw.line(screen, pygame.Color(color), (x1, y1), (x2, y2), 3)


def draw_button(rect, label):
    color = button_hover if rect.collidepoint(pygame.mouse.get_pos()) else button_color
    pygame.draw.rect(screen, color, rect)
    text = font.render(label, True, pygame.Color("white"))
    screen.blit(text, (rect.x + 10, rect.y + 8))


def get_cell_from_mouse(pos):
    x, y = pos
    if y >= grid.n * cell_size:
        return None
    i = y // cell_size
    j = x // cell_size
    if 0 <= i < grid.n and 0 <= j < grid.m:
        return (i, j)
    return None

# === Boucle principale ===
running = True
game_ended = False
selected_cells = []
paired_cells = []
used_cells = set()
GAME_MODE = 0

while running:
    if GAME_MODE == 0:
        screen.fill((255, 255, 255))
        draw_button(button_mode1, "2 Players")
        draw_button(button_mode2, "AI Versus")
        draw_button(button_mode3, "Solo mode")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_mode1.collidepoint(event.pos):
                    GAME_MODE = 2
                    pygame.display.set_caption("Grid Pairing Game - 2 Player Mode")
                elif button_mode2.collidepoint(event.pos):
                    GAME_MODE = 1
                    pygame.display.set_caption("Grid Pairing Game - AI Versus Mode")
                elif button_mode3.collidepoint(event.pos):
                    GAME_MODE = 3
                    pygame.display.set_caption("Grid Pairing Game - Solo Mode")

    elif GAME_MODE == 1:  # SELECTED MODE IS VS AI
        screen.fill((255, 255, 255))
        draw_grid()

        def next_moves(grid, used_cells):
            return [(c1, c2) for (c1, c2) in grid.all_pairs() if
                    grid.valid_pair(c1, c2) and (c1 not in used_cells) and (c2 not in used_cells)]

        game_ended = next_moves(grid, used_cells) == []

        # Affichage des paires
        for pair in player1_pairs:
            draw_pair(pair[0], pair[1], "yellow")

        for pair in player2_pairs:
            draw_pair(pair[0], pair[1], "black")

        if not game_ended:
            if current_player == 1:
                joueur = "Your turn"
            else:
                joueur = "AI Playing"
            msg_turn = font.render(joueur, True, pygame.Color("blue"))
            screen.blit(msg_turn, (200, grid.n * cell_size + 10))

        # Affichage scores finaux
        if game_ended:
            def compute_score(pairs):
                return sum(abs(grid.value[c1[0]][c1[1]] - grid.value[c2[0]][c2[1]]) for c1, c2 in pairs)
            user_score_1 = compute_score(player1_pairs)
            user_score_2 = compute_score(player2_pairs)
            winner = "You" if user_score_1 < user_score_2 else "AI" if user_score_1 > user_score_2 \
                else "Draw"
            msg1 = font.render(f"Your score : {user_score_1}", True, pygame.Color("black"))
            msg2 = font.render(f"AI's score : {user_score_2}", True, pygame.Color("black"))
            msg3 = font.render(f"Winner : {winner}", True, pygame.Color("green"))
            screen.blit(msg1, (200, grid.n * cell_size + 10))
            screen.blit(msg2, (200, grid.n * cell_size + 40))
            screen.blit(msg3, (200, grid.n * cell_size + 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == 1:  # Human is playing
                cell = get_cell_from_mouse(event.pos)
                if cell and cell not in used_cells:
                    selected_cells.append(cell)
                    if len(selected_cells) == 2:
                        c1, c2 = selected_cells
                        if c1 == c2:
                            print("Vous avez cliqué deux fois sur la même cellule.")
                        elif grid.valid_pair(c1, c2):
                            print(f"Paire valide Joueur {current_player} :", c1, c2)
                            paired_cells.append((c1, c2))
                            used_cells.update([c1, c2])
                            player1_pairs.append((c1, c2))
                            current_player = 2
                        else:
                            print("Paire invalide :", c1, c2)
                        selected_cells = []
            elif current_player == 2: # AI's turn
                if not game_ended:
                    (c1, c2) = AI.move(used_cells, player2_pairs, player1_pairs)
                    paired_cells.append((c1, c2))
                    used_cells.update([c1, c2])
                    player2_pairs.append((c1, c2))
                    current_player = 1

    elif GAME_MODE == 2:  # SELECTED MODE IS 2 PLAYER GAME
        screen.fill((255, 255, 255))
        draw_grid()
        draw_button(button_terminer, "Terminer")
        draw_button(button_annuler, "Annuler")

        # Affichage des paires
        for pair in player1_pairs:
            draw_pair(pair[0], pair[1], "yellow")

        for pair in player2_pairs:
            draw_pair(pair[0], pair[1], "black")
        # Affichage tour de joueur
        if not game_ended:
            msg_turn = font.render(f"Tour du Joueur {current_player}", True, pygame.Color("blue"))
            screen.blit(msg_turn, (200, grid.n * cell_size + 10))

        # Affichage scores finaux
        if game_ended:
            msg1 = font.render(f"Player 1 : {user_score_1}", True, pygame.Color("black"))
            msg2 = font.render(f"Player 2 : {user_score_2}", True, pygame.Color("black"))
            msg3 = font.render(f"Winner : {winner}", True, pygame.Color("green"))
            screen.blit(msg1, (200, grid.n * cell_size + 10))
            screen.blit(msg2, (200, grid.n * cell_size + 40))
            screen.blit(msg3, (200, grid.n * cell_size + 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_terminer.collidepoint(event.pos) and not game_ended:
                    def compute_score(pairs):
                        return sum(abs(grid.value[c1[0]][c1[1]] - grid.value[c2[0]][c2[1]]) for c1, c2 in pairs)

                    user_score_1 = compute_score(player1_pairs)
                    user_score_2 = compute_score(player2_pairs)
                    winner = "Player 1" if user_score_1 < user_score_2 else "Player 2" if user_score_1 > user_score_2 \
                        else "Draw"
                    game_ended = True

                elif button_annuler.collidepoint(event.pos) and not game_ended:
                    if paired_cells:
                        last_pair = paired_cells.pop()
                        used_cells.discard(last_pair[0])
                        used_cells.discard(last_pair[1])
                        if current_player == 1:
                            player2_pairs.pop()
                            current_player = 2
                        else:
                            player1_pairs.pop()
                            current_player = 1
                        print("Paire annulée :", last_pair)

                elif not game_ended:
                    cell = get_cell_from_mouse(event.pos)
                    if cell and cell not in used_cells:
                        selected_cells.append(cell)
                        if len(selected_cells) == 2:
                            c1, c2 = selected_cells
                            if c1 == c2:
                                print("Vous avez cliqué deux fois sur la même cellule.")
                            elif grid.valid_pair(c1, c2):
                                print(f"Paire valide Joueur {current_player} :", c1, c2)
                                paired_cells.append((c1, c2))
                                used_cells.update([c1, c2])
                                if current_player == 1:
                                    player1_pairs.append((c1, c2))
                                    current_player = 2
                                else:
                                    player2_pairs.append((c1, c2))
                                    current_player = 1
                            else:
                                print("Paire invalide :", c1, c2)
                            selected_cells = []

    elif GAME_MODE == 3:
        screen.fill((255, 255, 255))
        draw_grid()
        draw_button(button_terminer, "Terminer")
        draw_button(button_annuler, "Annuler")

        # Affichage des paires
        for pair in paired_cells:
            draw_pair(pair[0], pair[1], "yellow")

        if game_ended:
            msg1 = font.render(f"Votre score : {user_score}", True, pygame.Color("black"))
            msg2 = font.render(f"Score optimal : {optimal_score}", True, pygame.Color("black"))
            screen.blit(msg1, (200, grid.n * cell_size + 10))
            screen.blit(msg2, (200, grid.n * cell_size + 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_terminer.collidepoint(event.pos) and not game_ended:
                    # Score utilisateur
                    user_solver = Solver(grid)
                    user_solver.pairs = paired_cells
                    user_score = user_solver.score()

                    # Score optimal
                    solver.run()
                    optimal_score = solver.score()
                    game_ended = True

                elif button_annuler.collidepoint(event.pos) and not game_ended:
                    # Annuler la dernière paire
                    if paired_cells:
                        last_pair = paired_cells.pop()
                        used_cells.discard(last_pair[0])
                        used_cells.discard(last_pair[1])
                        print("Paire annulée :", last_pair)

                elif not game_ended:
                    cell = get_cell_from_mouse(event.pos)
                    if cell and cell not in used_cells:
                        selected_cells.append(cell)
                        if len(selected_cells) == 2:
                            c1, c2 = selected_cells
                            if c1 == c2:
                                print("Vous avez cliqué deux fois sur la même cellule.")
                            elif grid.valid_pair(c1, c2):
                                print("Paire valide :", c1, c2)
                                paired_cells.append((c1, c2))
                                used_cells.update([c1, c2])
                            else:
                                print("Paire invalide :", c1, c2)
                            selected_cells = []

    pygame.display.flip()

pygame.quit()
