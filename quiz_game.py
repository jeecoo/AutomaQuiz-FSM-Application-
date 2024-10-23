import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AutomaQuiz (A Sequential Quiz Game)")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLORS = [(215, 0, 64), (255, 191, 0), (0, 163, 108), (65, 105, 225)]  # Red, Yellow, Green, Blue

# samsung font
question_font = pygame.font.Font('samsungsharpsans-bold.otf', 36) 
button_font = pygame.font.Font('samsungsharpsans-bold.otf', 24) 

# heart image
heart_image = pygame.image.load('heart.png') 
heart_image = pygame.transform.scale(heart_image, (50, 50))

def draw_rounded_rect(surface, color, rect, radius):
    shape = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape, color, (0, 0, rect.width, rect.height), border_radius=radius)
    surface.blit(shape, rect.topleft)

# buttons
class Button:
    def __init__(self, x, y, width, height, text, color, radius=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.radius = radius

    def draw(self, screen):
        draw_rounded_rect(screen, self.color, self.rect, self.radius)
        shadow_surf = button_font.render(self.text, True, BLACK)
        shadow_rect = shadow_surf.get_rect(center=self.rect.center)
        shadow_rect.move_ip(2, 2)
        screen.blit(shadow_surf, shadow_rect)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# finite state machine
class AutomaQuizFSM:
    def __init__(self):
        self.questions = {
            'Question 1': {
                'prompt': "What does DFA stand for?",
                'options': [('Deterministic Finite Automaton', 'a'), ('Deterministic Finite Algorithm', 'b'), ('Dynamic Finite Automaton', 'c'), ('Determined Finite Automaton', 'd')],
                'correct': 'a'
            },
            'Question 2': {
                'prompt': "What does NFA stand for?",
                'options': [('Non-deterministic Finite Algorithm', 'a'), ('Nondetermined Finite Automaton', 'b'), ('Nondeterministic Finite Automaton', 'c'), ('Non-functional Finite Automaton', 'd')],
                'correct': 'c'
            },
            'Question 3': {
                'prompt': "What is an automaton?",
                'options': [('Mathematical Model', 'a'), ('Programming Language', 'b'), ('Data Structure', 'c'), ('Algorithm', 'd')],
                'correct': 'a'
            },
            'Question 4': {
                'prompt': "What type of languages can DFAs accept?",
                'options': [('Context-Free', 'a'), ('Regular', 'b'), ('Context-Sensitive', 'c'), ('Recursive', 'd')],
                'correct': 'b'
            },
            'Question 5': {
                'prompt': "What is a regular expression?",
                'options': [('State Machine', 'a'), ('Data Structure', 'b'), ('Algorithm', 'c'), ('Language Definition', 'd')],
                'correct': 'd'
            }
        }
        self.current_question = 'Question 1'
        self.correct_answers = 0
        self.lives = 3
        self.game_over = False
        self.perfect_score = False

    def transition(self, answer):
        correct_answer = self.questions[self.current_question]['correct']
        if answer == correct_answer:
            self.correct_answers += 1
            self.next_question()
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True

    def next_question(self):
        if self.current_question == 'Question 1':
            self.current_question = 'Question 2'
        elif self.current_question == 'Question 2':
            self.current_question = 'Question 3'
        elif self.current_question == 'Question 3':
            self.current_question = 'Question 4'
        elif self.current_question == 'Question 4':
            self.current_question = 'Question 5'
        else:
            self.perfect_score = self.correct_answers == 5
            self.game_over = True

    def is_game_over(self):
        return self.game_over

    def get_current_question(self):
        return self.questions[self.current_question]

    def get_lives(self):
        return self.lives

# Quiz
quiz = AutomaQuizFSM()

# Try again button
def try_again():
    global quiz
    quiz = AutomaQuizFSM()

# Loop
def game_loop():
    running = True
    while running:
        if not quiz.is_game_over():
            screen.fill(BLACK)
            current_question = quiz.get_current_question()

            margin_top = 160
            margin_sides = 40

            # rendering
            question_text = question_font.render(current_question['prompt'], True, WHITE)
            screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, margin_top))

            # lives
            for i in range(quiz.get_lives()):
                screen.blit(heart_image, (WIDTH - (i + 1) * (heart_image.get_width() + 5), 10))

            # buttons
            buttons = []
            button_width = 450
            button_height = 100
            vertical_spacing = 20
            horizontal_spacing = 20
            start_x = margin_sides
            start_y = margin_top + 100

            for i, (option_text, option_value) in enumerate(current_question['options']):
                row = i // 2
                col = i % 2
                button_x = start_x + col * (button_width + horizontal_spacing)
                button_y = start_y + row * (button_height + vertical_spacing)
                color = BUTTON_COLORS[i % len(BUTTON_COLORS)]
                button = Button(button_x, button_y, button_width, button_height, option_text, color)
                button.draw(screen)
                buttons.append((button, option_value))

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button, option_value in buttons:
                        if button.is_clicked(mouse_pos):
                            quiz.transition(option_value)

            pygame.display.flip()

        else:
            # gameover or congrats
            screen.fill(BLACK)
            if quiz.perfect_score:
                end_message = "Congratulations! You got a perfect score!"
            else:
                end_message = "Game Over!"

            end_text1 = question_font.render(end_message, True, WHITE)
            screen.blit(end_text1, (WIDTH // 2 - end_text1.get_width() // 2, HEIGHT // 2 - 100))

            if not quiz.perfect_score:
                score_text = question_font.render(f"Correct answers: {quiz.correct_answers}/5", True, WHITE)
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))

            # try again
            try_again_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60, "Try Again", (113, 121, 126))
            try_again_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if try_again_button.is_clicked(mouse_pos):
                        try_again()  # restart game

            pygame.display.flip()

game_loop()


