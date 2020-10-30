import math
import textwrap

from quiz import get_quiz
import pygame

TRANSP_GREEN_LIGHT = (14, 213, 41, 210)
TRANSP_GREEN_HIGHL = (14, 213, 41, 150)
TRANSP_GREEN = (5, 85, 15, 150)
TRANSP_RED = (215, 2, 30, 210)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (2, 215, 30)
DARKGREEN = (10, 150, 25)
DARKGREEN_2 = (40, 120, 5)
LIGHT_GREEN = (18, 255, 50)
GREY = (220, 220, 220)
RED = (255, 0, 0)
FONT_ROBOTO = "fonts/RobotoSlab-Medium.ttf"
screen_size = (800, 600)


class TextBox:
    def __init__(self, rel_pos, font_name, font_size, font_bold, color, text, line_width=100):
        self.position = (screen_size[0] * rel_pos[0], screen_size[1] * rel_pos[1])
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, font_size)
        self.font.set_bold(font_bold)
        self.color = color
        self.text_lines = []
        self.text_lines_shadow = []
        self.line_width = line_width
        self.set_text(text)

    def set_text(self, text):
        lines_specified_width = textwrap.fill(text, self.line_width)
        chopped_lines = lines_specified_width.split('\n')
        self.text_lines = []
        self.text_lines_shadow = []
        for line in chopped_lines:
            line_surface = self.font.render(line, True, self.color)
            self.text_lines.append(line_surface)
            line_surface_shadow = self.font.render(line, True, BLACK)
            self.text_lines_shadow.append(line_surface_shadow)

    def render(self, screen):
        # time = pygame.time.get_ticks()
        # x_off = 2 * math.cos(time*3.14/1000)
        # y_off = 2 * math.sin(time*3.14/1000)

        # shadow
        for idx, text_surface_shadow in enumerate(self.text_lines_shadow):
            text_rect_shadow = text_surface_shadow.get_rect()
            text_rect_shadow.center = self.position[0] + 1, self.position[1] + 2 + idx * (self.font_size + 15)
            screen.blit(text_surface_shadow, text_rect_shadow)

        for idx, text_surface in enumerate(self.text_lines):
            text_rect = text_surface.get_rect()
            text_rect.center = self.position[0], self.position[1] + idx * (self.font_size + 15)
            screen.blit(text_surface, text_rect)


class Button:
    def __init__(self, rel_pos, rel_size, color, highlight, font_size, font_color, text):
        self.position = (screen_size[0] * rel_pos[0], screen_size[1] * rel_pos[1])
        self.size = (screen_size[0] * rel_size[0], screen_size[1] * rel_size[1])
        self.color = color
        self.highlight = highlight
        self.text = TextBox(rel_pos=rel_pos, font_name=FONT_ROBOTO,
                            font_size=font_size, font_bold=False, color=font_color, text=text, line_width=25)
        self.button_rect = pygame.Rect(self.position[0], self.position[1], self.size[0] - 3, self.size[1] - 3)
        self.button_rect.center = self.position[0], self.position[1]
        self.button_frame_rect = pygame.Rect(0, 0, self.size[0], self.size[1])  # x, y, width, height
        self.button_frame_rect.center = self.position[0], self.position[1]
        self.enabled = True

    def handle_keydown(self, key):
        pass

    def handle_mouse_button(self, mouse_button):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and mouse_button == 1 and self.enabled:
            return True
        else:
            return False

    def render(self, screen):
        pygame.draw.rect(screen, DARKGREEN, self.button_frame_rect, 4)  # button frame

        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and self.enabled:  # If mouse on button - highlight button
            if len(self.highlight) == 4:
                s = pygame.Surface((self.button_rect.width, self.button_rect.height),
                                   pygame.SRCALPHA)  # per-pixel alpha
                s.fill(self.highlight)  # notice the alpha value in the color
                screen.blit(s, self.button_rect)
            else:
                pygame.draw.rect(screen, self.highlight, self.button_rect)
        else:
            if len(self.color) == 4:
                s = pygame.Surface((self.button_rect.width, self.button_rect.height),
                                   pygame.SRCALPHA)  # per-pixel alpha
                s.fill(self.color)  # notice the alpha value in the color
                screen.blit(s, self.button_rect)
            else:
                pygame.draw.rect(screen, self.color, self.button_rect)

        self.text.render(screen)


class QuizScreen:

    def __init__(self):
        background_image_raw = pygame.image.load("Background_forest.jpg").convert()
        self.background_image = pygame.transform.scale(background_image_raw, screen_size)

        self.title = None
        self.question_text = None
        self.quiz_answer_buttons = []

        self.current_question = 0

        # questions, correct_answer, answer_options = get_quiz()
        # print(questions)
        # print(correct_answer)
        # print(answer_options)

        self.questions = ""
        self.correct_answer = ""
        self.answer_options = ""
        #self.correct_answer_idx = answer_options.index(correct_answer)
        self.correct_answer_idx = None

        self.button_positions = [(0.3, 0.6),
                                 (0.7, 0.6),
                                 (0.3, 0.8),
                                 (0.7, 0.8)]
        self.set_question()
        self.next_question_timeout = 0

        # for question in questions:
        #     self.current_question_number += 1
        #     self.set_question(self.current_question)
        #     self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
        #                      font_size=25, font_bold=False, color=WHITE, text=f"Question {self.current_question}")
        #
        #     self.question_text = TextBox(rel_pos=(0.5, 0.25), font_name=FONT_ROBOTO,
        #                                  font_size=25, font_bold=False, color=WHITE, text=question, line_width=55)
        #
        #     self.quiz_answer_buttons = []
        #     for idx, answer_option in enumerate(answer_options):
        #         quiz_button = Button(rel_pos=button_positions[idx], rel_size=(0.4, 0.2),
        #                              color=TRANSP_GREEN, highlight=TRANSP_GREEN_HIGHL,
        #                              font_size=22, font_color=WHITE, text=answer_option)
        #         self.quiz_answer_buttons.append(quiz_button)

    def set_question(self):
        self.next_question_timeout = 0
        question, correct_answer, answer_options = get_quiz()
        print(question)
        print(correct_answer)
        print(answer_options)
        self.questions = question
        self.correct_answer = correct_answer
        self.answer_options = answer_options
        self.current_question += 1


        #question = self.questions[self.current_question]
        self.correct_answer_idx = self.answer_options.index(self.correct_answer)

        self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                             font_size=25, font_bold=False, color=WHITE, text=f"Question {self.current_question}")

        self.question_text = TextBox(rel_pos=(0.5, 0.25), font_name=FONT_ROBOTO,
                                     font_size=25, font_bold=False, color=WHITE, text=question, line_width=55)
        self.quiz_answer_buttons = []
        for idx, answer_option in enumerate(self.answer_options):
            quiz_button = Button(rel_pos=self.button_positions[idx], rel_size=(0.4, 0.2),
                                 color=TRANSP_GREEN, highlight=TRANSP_GREEN_HIGHL,
                                 font_size=22, font_color=WHITE, text=answer_option)
            self.quiz_answer_buttons.append(quiz_button)


    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            #return QuizFinishedScreen()
            self.set_question()
        return self

    def handle_mouse_button(self, mouse_button):
        clicked_button_idx = None
        quiz_button = None
        print("handle mus button")
        for quiz_button in self.quiz_answer_buttons:
            if quiz_button.handle_mouse_button(mouse_button):
                clicked_button_idx = self.quiz_answer_buttons.index(quiz_button)
                print(clicked_button_idx, "the_clicked_button")
                break

        if clicked_button_idx is not None:

            self.next_question_timeout = pygame.time.get_ticks()

            print("correct_answer_idx", self.correct_answer_idx)
            if clicked_button_idx == self.correct_answer_idx:
                print("Rätt svar!")
                quiz_button.color = TRANSP_GREEN_LIGHT
            else:
                quiz_button.color = TRANSP_RED
                self.quiz_answer_buttons[self.correct_answer_idx].color = TRANSP_GREEN_LIGHT
                print("Det var fel, rätt svar var knapp", self.correct_answer_idx)

            for quiz_button in self.quiz_answer_buttons:
                quiz_button.enabled = False

    def render(self, screen, font):
        screen.fill(BLACK)
        screen.blit(self.background_image, (0, 0))

        time_now = pygame.time.get_ticks()
        if time_now - self.next_question_timeout > 2000 and self.next_question_timeout != 0:
            self.set_question()

        self.title.render(screen)

        self.question_text.render(screen)

        for quiz_answer_button in self.quiz_answer_buttons:
            quiz_answer_button.render(screen)


class QuizFinishedScreen:
    def __init__(self):
        background_image_raw = pygame.image.load("Background_forest.jpg").convert()
        self.background_image = pygame.transform.scale(background_image_raw, screen_size)

        incorrectly_aswered_questions = ["Vad heter jag?", "Vad heter du?"]
        success = False
        if success:
            self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                                 font_size=25, font_bold=False, color=WHITE,
                                 text="You answered all questions correctly!")
            info_text_success = "WOW you're awesome! You get a bonus in award!"
            self.info_text = TextBox(rel_pos=(0.5, 0.3), font_name=FONT_ROBOTO,
                                     font_size=25, font_bold=False, color=WHITE, text=info_text_success, line_width=60)
        else:
            self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                                 font_size=25, font_bold=False, color=WHITE, text="Do. Or do not. There is no try.")
            info_text_failure = "You didn't answer all questions correctly, so you won't get a bonus. Better luck next time!"
            self.info_text = TextBox(rel_pos=(0.5, 0.3), font_name=FONT_ROBOTO,
                                     font_size=25, font_bold=False, color=WHITE, text=info_text_failure, line_width=60)
            for idx, question in enumerate(incorrectly_aswered_questions):
                self.questions_text_failure = TextBox(rel_pos=(0.5, 0.3 + idx), font_name=FONT_ROBOTO,
                                                      font_size=25, font_bold=False, color=WHITE, text=question)

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            return QuizScreen()
        return self

    def handle_mouse_button(self, mouse_button):
        pass

    def render(self, screen, font):
        screen.fill(BLACK)
        screen.blit(self.background_image, (0, 0))
        self.title.render(screen)
        self.info_text.render(screen)


class QuizStartScreen:
    def __init__(self):
        quiz_start = """If you answer all four quiz questions correctly, you get a bonus.
The question categories are computers, mathematics and science / nature. The categories are selected at random. Good luck!"""

        background_image_raw = pygame.image.load("Background_forest.jpg").convert()
        self.background_image = pygame.transform.scale(background_image_raw, screen_size)
        self.title = TextBox(rel_pos=(0.5, 0.1), font_name=FONT_ROBOTO,
                             font_size=30, font_bold=False, color=WHITE, text="It's quiz time!")
        self.info_text = TextBox(rel_pos=(0.5, 0.32), font_name=FONT_ROBOTO,
                                 font_size=25, font_bold=False, color=WHITE, text=quiz_start, line_width=50)

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            return QuizScreen()
        return self

    def handle_mouse_button(self, mouse_button):
        pass

    def render(self, screen, font):
        screen.fill(BLACK)
        screen.blit(self.background_image, (0, 0))
        self.title.render(screen)
        self.info_text.render(screen)


def mainloop(screen, font):
    # Initial state
    current_screen = QuizScreen()

    clock = pygame.time.Clock()
    while True:

        # Event handling
        ev = pygame.event.poll()

        if ev.type == pygame.KEYDOWN:
            state = current_screen.handle_keydown(ev.key)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            current_screen.handle_mouse_button(ev.button)

        elif ev.type == pygame.QUIT:
            break

        # Render
        current_screen.render(screen, font)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("PokeMood")
    font = FONT_ROBOTO
    mainloop(screen, font)
    pygame.quit()
