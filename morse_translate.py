import pygame
import sys
import pyperclip

# Initialize Pygame
pygame.init()

# Initial screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)

# Set up display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Morse Code Translator")

# Morse code dictionaries
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

TEXT_TO_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def translate_morse_to_text(morse_code):
    words = morse_code.split(' / ')
    translation = ''
    for word in words:
        letters = word.split(' ')
        for letter in letters:
            translation += MORSE_CODE_DICT.get(letter, '')
        translation += ' '
    return translation.strip()

def translate_text_to_morse(text):
    text = text.upper()
    translation = ''
    for char in text:
        if char == ' ':
            translation += ' / '
        else:
            translation += TEXT_TO_MORSE_DICT.get(char, '') + ' '
    return translation.strip()

def draw_text(surface, text, position, size=24, color=GREEN):
    font = pygame.font.Font(pygame.font.match_font('courier', bold=True), size)
    label = font.render(text, 1, color)
    surface.blit(label, position)

def calculate_font_size(text, max_width, max_height, max_font_size=36):
    font_size = max_font_size
    font = pygame.font.Font(pygame.font.match_font('courier', bold=True), font_size)
    while font_size > 10:
        width, height = font.size(text)
        if width <= max_width and height <= max_height:
            break
        font_size -= 1
        font = pygame.font.Font(pygame.font.match_font('courier', bold=True), font_size)
    return font_size

class Dropdown:
    def __init__(self, surface, position, options, default_index=0):
        self.surface = surface
        self.position = position
        self.options = options
        self.selected_index = default_index
        self.showing_options = False

    def draw(self):
        main_rect = pygame.Rect(self.position, (200, 30))
        option_rects = [pygame.Rect((self.position[0], self.position[1] + 30 * (i + 1)), (200, 30)) for i in range(len(self.options))]

        pygame.draw.rect(self.surface, GRAY, main_rect)
        draw_text(self.surface, self.options[self.selected_index], (self.position[0] + 10, self.position[1] + 5), 24, WHITE)

        if self.showing_options:
            for i, rect in enumerate(option_rects):
                pygame.draw.rect(self.surface, LIGHT_GRAY if i == self.selected_index else GRAY, rect)
                draw_text(self.surface, self.options[i], (rect.x + 10, rect.y + 5), 24, WHITE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                main_rect = pygame.Rect(self.position, (200, 30))
                option_rects = [pygame.Rect((self.position[0], self.position[1] + 30 * (i + 1)), (200, 30)) for i in range(len(self.options))]

                if main_rect.collidepoint(x, y):
                    self.showing_options = not self.showing_options
                elif self.showing_options:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(x, y):
                            self.selected_index = i
                            self.showing_options = False
                            break

def main():
    global win
    run = True
    clock = pygame.time.Clock()
    input_text = ""
    translated_text = ""
    scroll_offset = 0
    scroll_speed = 20

    dropdown = Dropdown(win, (10, 10), ["Morse to Text", "Text to Morse"])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if dropdown.selected_index == 1:
                        translated_text = translate_text_to_morse(input_text)
                    else:
                        translated_text = translate_morse_to_text(input_text)
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    input_text += pyperclip.paste()
                elif event.key == pygame.K_SPACE:
                    input_text += " "
                elif event.key == pygame.K_SLASH:
                    input_text += "/"
                else:
                    input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_offset = min(scroll_offset + scroll_speed, 0)
                if event.button == 5:  # Scroll down
                    scroll_offset -= scroll_speed

            dropdown.handle_event(event)

        max_text_width = SCREEN_WIDTH - 40  # Padding of 20px on each side
        max_text_height = SCREEN_HEIGHT // 3  # Roughly 1/3 of the screen height per text block

        input_font_size = calculate_font_size(input_text, max_text_width, max_text_height)
        translated_font_size = calculate_font_size(translated_text, max_text_width, max_text_height)
        font_size = min(input_font_size, translated_font_size)

        win.fill(BLACK)
        dropdown.draw()
        draw_text(win, "Enter Morse Code:" if dropdown.selected_index == 0 else "Enter Text:", (20, 60 + scroll_offset), 24)
        draw_text(win, input_text, (20, 100 + scroll_offset), font_size)
        draw_text(win, "Translation:", (20, 160 + scroll_offset), 24)
        draw_text(win, translated_text, (20, 200 + scroll_offset), font_size)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
