import pygame
import random
import heapq
import math

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
pygame.display.set_caption('Snake Game with Pathfinding')  # تعيين عنوان النافذة

# ساعة للتحكم في سرعة اللعبة
clock = pygame.time.Clock()

class AStar:
    @staticmethod
    def heuristic(a, b):
        # حساب المسافة التقديرية باستخدام المسافة الإقليدية
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    @staticmethod
    def get_neighbors(current, snake_body):
        # الحصول على الجيران المتاحين
        neighbors = [
            (current[0]+1, current[1]),
            (current[0]-1, current[1]),
            (current[0], current[1]+1),
            (current[0], current[1]-1)
        ]
        
        # تصفية الجيران للتأكد من عدم وجودها في جسم الثعبان
        return [
            n for n in neighbors 
            if 0 <= n[0] < GRID_WIDTH and 
               0 <= n[1] < GRID_HEIGHT and 
               n not in snake_body
        ]

    @staticmethod
    def find_path(start, goal, snake_body):
        # تنفيذ خوارزمية A*
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next_node in AStar.get_neighbors(current, snake_body):
                new_cost = cost_so_far[current] + 1

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + AStar.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        # استعادة المسار
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                return []  # لا يوجد مسار
        path.append(start)
        path.reverse()
        return path[1:]  # استبعاد نقطة البداية

class Snake:
    def __init__(self):
        # جسم الثعبان يبدأ بمربع واحد في منتصف الشبكة
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # اتجاه الثعبان (يمين)
        self.grow_to = 0  # عدد المربعات التي سينمو بها الثعبان
        self.path_to_food = []  # مسار الطعام

    def calculate_path(self, food_position):
        # حساب المسار إلى الطعام باستخدام A*
        self.path_to_food = AStar.find_path(
            self.body[0],  # نقطة البداية (رأس الثعبان)
            food_position,  # نقطة النهاية (الطعام)
            self.body[1:]  # تجنب جسم الثعبان
        )

    def move_along_path(self):
        # التحرك على المسار المحسوب
        if self.path_to_food:
            next_pos = self.path_to_food[0]
            # تحديد الاتجاه
            self.direction = (
                next_pos[0] - self.body[0][0],
                next_pos[1] - self.body[0][1]
            )
            self.move()
            # إزالة أول نقطة من المسار
            self.path_to_food.pop(0)
        else:
            # إذا لم يكن هناك مسار، التحرك عشوائياً
            self.move()

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

# الدالة الرئيسية للعبة
def main():
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

        # حساب المسار إلى الطعام
        snake.calculate_path(food.position)
        
        # تحريك الثعبان
        snake.move_along_path()

        # التحقق من تناول الطعام
        if snake.body[0] == food.position:
            snake.grow()  # زيادة طول الثعبان
            food = Food(snake)  # إنشاء طعام جديد
            score += 1  # زيادة النقاط

        # التحقق من انتهاء اللعبة
        if snake.check_collision():
            running = False

        # الرسم
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

# تشغيل اللعبة
if __name__ == "__main__":
    main()