import pygame  # استيراد مكتبة pygame لعمل الرسوميات والتفاعل مع اللعبة
import random  # استيراد مكتبة random لاختيار أماكن عشوائية للطعام
import collections  # استيراد مكتبة collections لاستخدام deque في خوارزمية البحث BFS


# إعدادات اللعبة
pygame.init()  # تهيئة pygame
WIDTH, HEIGHT = 800, 600  # تحديد عرض وطول الشاشة
GRID_SIZE = 20  # تحديد حجم الخلية في الشبكة
GRID_WIDTH = WIDTH // GRID_SIZE  # عدد الخلايا في العرض
GRID_HEIGHT = HEIGHT // GRID_SIZE  # عدد الخلايا في الطول

# الألوان
BLACK = (0, 0, 0)  # اللون الأسود
WHITE = (255, 255, 255)  # اللون الأبيض
RED = (255, 0, 0)  # اللون الأحمر
GREEN = (0, 255, 0)  # اللون الأخضر
BLUE = (0, 0, 255)  # اللون الأزرق

# إعدادات الشاشة
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # إنشاء نافذة اللعبة بحجم العرض والطول
pygame.display.set_caption('AI PROJECT')  # وضع عنوان للنافذة

# تحميل صورة الخلفية
bg_image = pygame.image.load('bg.png')  # تحميل صورة الخلفية
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  # تعديل حجم الصورة لتغطية الشاشة


# خوارزمية بحث المستوى الأول (BFS) لاكتشاف المسار
class SimplePathfinder:
    @staticmethod
    def find_path(start, goal, snake_body):
        """
        خوارزمية BFS لاكتشاف المسار
        الشرح:
        1. نبدأ من رأس الثعبان
        2. نبحث عن أقصر مسار للطعام
        3. نتجنب جسم الثعبان وحدود اللعبة
        """
        # الحركات الممكنة: اليمين، اليسار، الأسفل، الأعلى
        moves = [(1,0), (-1,0), (0,1), (0,-1)]
        
        # قائمة للاستكشاف (queue)
        queue = collections.deque([[start]])  # قائمة انتظار لتمثيل المسارات
        visited = set([start])  # تتبع الأماكن التي تم زيارتها

        while queue:
            # الحصول على المسار الحالي
            path = queue.popleft()  # أخذ المسار الحالي من القائمة
            current = path[-1]  # الحصول على آخر مكان في المسار الحالي

            # إذا وصلنا للهدف (الطعام)
            if current == goal:
                return path[1:]  # تجاهل أول موضع (الرأس الحالي)

            # تجربة جميع الحركات الممكنة
            for move in moves:
                # حساب الموضع التالي
                next_pos = (current[0] + move[0], current[1] + move[1])

                # التحقق إذا كانت الحركة صالحة:
                # 1. داخل حدود اللعبة
                # 2. ليست داخل جسم الثعبان
                # 3. لم يتم زيارته مسبقاً
                if (0 <= next_pos[0] < GRID_WIDTH and 
                    0 <= next_pos[1] < GRID_HEIGHT and 
                    next_pos not in snake_body and 
                    next_pos not in visited):
                    
                    # إنشاء مسار جديد
                    new_path = list(path)
                    new_path.append(next_pos)
                    
                    # إضافته إلى القائمة (queue) ووضعه في الأماكن التي تم زيارتها
                    queue.append(new_path)
                    visited.add(next_pos)
        
        # إذا لم نجد مساراً
        return []


# فئة الثعبان مع خوارزمية BFS لاكتشاف المسار
class Snake:
    def __init__(self):
        # يبدأ الثعبان في منتصف الشاشة
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # جسم الثعبان مبدئياً يتكون من خلية واحدة
        self.direction = (1, 0)  # يبدأ الحركة إلى اليمين
        self.path_to_food = []  # مسار الوصول للطعام
        self.grow_to = 0  # متغير لتحديد ما إذا كان الثعبان يحتاج للنمو

    def find_path_to_food(self, food_position):
        """
        البحث عن المسار إلى الطعام باستخدام BFS
        الشرح:
        - البحث عن أقصر طريق للطعام
        - تجنب الاصطدام بجسم الثعبان
        """
        self.path_to_food = SimplePathfinder.find_path(
            self.body[0],  # بداية من رأس الثعبان
            food_position,  # الهدف هو الطعام
            self.body[1:]   # تجنب جسم الثعبان
        )

    def move(self):
        # إذا كان لدينا مسار، نتبعه
        if self.path_to_food:
            # تحديد الاتجاه للخطوة التالية
            next_pos = self.path_to_food[0]
            self.direction = (
                next_pos[0] - self.body[0][0],  # حساب الفرق بين الرأس الحالي والموقع التالي
                next_pos[1] - self.body[0][1]
            )
            self.path_to_food.pop(0)  # إزالة أول خطوة من المسار

        # تحريك الثعبان
        head = self.body[0]  # رأس الثعبان الحالي
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])  # حساب الموضع الجديد للرأس
        self.body.insert(0, new_head)  # إضافة الرأس الجديد إلى مقدمة الجسم

        # النمو أو التقلص
        if self.grow_to > 0:
            self.grow_to -= 1  # إذا كان هناك حاجة لنمو الثعبان، لا نقوم بحذف الجزء الأخير
        else:
            self.body.pop()  # إذا لم يكن هناك حاجة للنمو، نحذف الجزء الأخير من الجسم

    def grow(self):
        # إطالة الثعبان
        self.grow_to += 1  # زيادة عدد الأجزاء التي يجب أن يزداد بها الجسم

    def check_collision(self):
        head = self.body[0]  # رأس الثعبان
        # الاصطدام بالجدار
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True  # إذا خرج الرأس عن حدود الشاشة

        # الاصطدام بنفسه
        if head in self.body[1:]:
            return True  # إذا اصطدم الرأس بجسم الثعبان نفسه

        return False  # لا يوجد اصطدام

    def draw(self, screen):
        # رسم الثعبان على الشاشة
        for segment in self.body:  # لكل جزء من أجزاء الجسم
            pygame.draw.rect(screen, GREEN, 
                             (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                              GRID_SIZE-1, GRID_SIZE-1))  # رسم كل جزء من جسم الثعبان


# فئة الطعام
class Food:
    def __init__(self, snake):
        # إنشاء الطعام بعيداً عن جسم الثعبان
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        while True:
            position = (
                random.randint(0, GRID_WIDTH-1),  # تحديد موقع عشوائي للطعام
                random.randint(0, GRID_HEIGHT-1)
            )
            if position not in snake.body:  # التأكد من أن الطعام لا يتواجد داخل جسم الثعبان
                return position

    def draw(self, screen):
        # رسم الطعام على الشاشة
        pygame.draw.rect(screen, RED, 
                         (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE, 
                          GRID_SIZE-1, GRID_SIZE-1))  # رسم الطعام بلون أحمر


# الحلقة الرئيسية للعبة
def main():
    snake = Snake()  # إنشاء كائن الثعبان
    food = Food(snake)  # إنشاء كائن الطعام
    score = 0  # وضع النتيجة الابتدائية
    font = pygame.font.Font(None, 36)  # إعداد الخط لعرض النص

    running = True  # تشغيل اللعبة
    while running:
        for event in pygame.event.get():  # معالجة الأحداث (مثل إغلاق النافذة)
            if event.type == pygame.QUIT:
                running = False  # إنهاء اللعبة إذا أغلق المستخدم النافذة

        # البحث عن المسار للطعام
        snake.find_path_to_food(food.position)
        
        # تحريك الثعبان
        snake.move()

        # إذا وصل الثعبان إلى الطعام
        if snake.body[0] == food.position:
            snake.grow()  # زيادة طول الثعبان
            food = Food(snake)  # إعادة إنشاء طعام جديد
            score += 1  # زيادة النتيجة

        # التحقق إذا انتهت اللعبة بسبب الاصطدام
        if snake.check_collision():
            running = False

        # الرسم
        screen.fill(BLACK)  # ملء الشاشة باللون الأسود
        screen.blit(bg_image, (0, 0))  # رسم الخلفية
        snake.draw(screen)  # رسم الثعبان
        food.draw(screen)  # رسم الطعام

        # عرض النتيجة
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()  # تحديث الشاشة
        clock.tick(10)  # تحديد سرعة اللعبة

    # شاشة النهاية
    screen.fill(BLACK)  # ملء الشاشة باللون الأسود
    game_over_text = font.render('Game Over!', True, WHITE)  # نص "انتهت اللعبة"
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)  # النص الخاص بالنتيجة النهائية
    screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))  # عرض "انتهت اللعبة"
    screen.blit(final_score_text, (WIDTH//2 - 100, HEIGHT//2 + 50))  # عرض النتيجة النهائية
    screen.blit(bg_image, (0, 0))  # رسم الخلفية مرة أخرى
    pygame.display.flip()

    pygame.time.wait(2000)  # الانتظار لمدة 2 ثانية قبل إغلاق اللعبة
    pygame.quit()  # إغلاق pygame


# إنشاء الساعة وتشغيل اللعبة
clock = pygame.time.Clock()
if __name__ == "__main__":
    main()  # بدء اللعبة