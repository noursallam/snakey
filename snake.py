import pygame
import random
import os

# تهيئة مكتبة Pygame
pygame.init()

# أبعاد الشاشة
WIDTH = 800  # عرض الشاشة
HEIGHT = 600  # ارتفاع الشاشة
GRID_SIZE = 20  # حجم كل خلية في الشبكة
GRID_WIDTH = WIDTH // GRID_SIZE  # عدد الأعمدة في الشبكة
GRID_HEIGHT = HEIGHT // GRID_SIZE  # عدد الصفوف في الشبكة

# الألوان (RGB)
BLACK = (0, 0, 0)  # لون أسود
WHITE = (255, 255, 255)  # لون أبيض
RED = (255, 0, 0)  # لون أحمر
GREEN = (0, 255, 0)  # لون أخضر
BLUE = (0, 0, 255)  # لون أزرق
GRID_COLOR = (50, 50, 50)  # لون الشبكة (رمادي غامق)

# إعداد شاشة اللعبة
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # إنشاء نافذة بحجم العرض والارتفاع
pygame.display.set_caption('Snake Game')  # تعيين عنوان النافذة

# ساعة للتحكم في سرعة اللعبة
clock = pygame.time.Clock()

# تعريف كائن الثعبان
class Snake:
    def __init__(self):
        # جسم الثعبان يبدأ بمربع واحد في منتصف الشبكة
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # اتجاه الثعبان (يمين)
        self.grow_to = 0  # عدد المربعات التي سينمو بها الثعبان

    def move(self):
        # حساب موقع الرأس الجديد للثعبان
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)  # إضافة الرأس الجديد إلى الجسم

        # إذا كان الثعبان سينمو، نخفض عداد النمو
        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.body.pop()  # إزالة آخر جزء في الجسم

    def grow(self):
        # زيادة عدد المربعات التي سينمو بها الثعبان
        self.grow_to += 1

    def check_collision(self):
        # الحصول على رأس الثعبان
        head = self.body[0]

        # التحقق من الاصطدام بالجدار
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True

        # التحقق من الاصطدام بجسم الثعبان نفسه
        if head in self.body[1:]:
            return True

        return False  # لا يوجد اصطدام

    def draw(self, screen):
        # رسم أجزاء جسم الثعبان
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                             (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                              GRID_SIZE-1, GRID_SIZE-1))

# تعريف كائن الطعام
class Food:
    def __init__(self, snake):
        # تحديد موقع عشوائي للطعام بعيداً عن الثعبان
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        # توليد موقع جديد للطعام
        while True:
            position = (random.randint(0, GRID_WIDTH-1), 
                        random.randint(0, GRID_HEIGHT-1))
            if position not in snake.body:
                return position

    def draw(self, screen):
        # رسم الطعام
        pygame.draw.rect(screen, RED, 
                         (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE, 
                          GRID_SIZE-1, GRID_SIZE-1))

# رسم الشبكة
def draw_grid(screen):
    # رسم الخطوط العمودية
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    
    # رسم الخطوط الأفقية
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

# تحميل صورة الخلفية
def load_background_image(image_path):
    try:
        # تحميل صورة الخلفية
        background = pygame.image.load(image_path)
        # تغيير حجم الصورة لتتناسب مع الشاشة
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        return background
    except pygame.error:
        print(f"Cannot load image: {image_path}")
        # إرجاع سطح فارغ إذا فشل تحميل الصورة
        return pygame.Surface((WIDTH, HEIGHT))

# الدالة الرئيسية للعبة
def main(background_image_path=None):
    # تحميل صورة الخلفية إذا تم تحديدها
    background = load_background_image(background_image_path) if background_image_path else None
    
    snake = Snake()  # إنشاء كائن الثعبان
    food = Food(snake)  # إنشاء كائن الطعام
    score = 0  # النقاط
    font = pygame.font.Font(None, 36)  # إعداد الخط لعرض النقاط

    running = True
    while running:
        # التعامل مع الأحداث
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # الخروج من اللعبة
                running = False
            
            if event.type == pygame.KEYDOWN:  # عند الضغط على أزرار الاتجاهات
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        snake.move()  # تحريك الثعبان

        # التحقق من تناول الطعام
        if snake.body[0] == food.position:
            snake.grow()  # زيادة طول الثعبان
            food = Food(snake)  # إنشاء طعام جديد
            score += 1  # زيادة النقاط

        # التحقق من انتهاء اللعبة
        if snake.check_collision():
            running = False

        # الرسم
        if background:
            screen.blit(background, (0, 0))  # رسم الخلفية
        else:
            screen.fill(BLACK)  # ملء الشاشة باللون الأسود

        draw_grid(screen)  # رسم الشبكة
        snake.draw(screen)  # رسم الثعبان
        food.draw(screen)  # رسم الطعام

        # عرض النقاط
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()  # تحديث الشاشة

        clock.tick(10)  # التحكم في سرعة اللعبة

    # شاشة انتهاء اللعبة
    screen.fill(BLACK)  # مسح الشاشة باللون الأسود
    game_over_text = font.render('Game Over!', True, WHITE)  # رسالة انتهاء اللعبة
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)  # عرض النقاط النهائية
    screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
    screen.blit(final_score_text, (WIDTH//2 - 100, HEIGHT//2 + 50))
    pygame.display.flip()

    pygame.time.wait(2000)  # انتظار قبل الإغلاق
    pygame.quit()

# تشغيل اللعبة مع صورة خلفية
if __name__ == "__main__":
    main('bg.png')
