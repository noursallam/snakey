import random
from pathfinder import SimplePathfinder
import pygame

GRID_WIDTH = 800 // 20
GRID_HEIGHT = 600 // 20
GRID_SIZE = 20
GREEN = (0, 255, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.path_to_food = []
        self.grow_to = 0

    def find_path_to_food(self, food_position):
        """Find the path to the food using BFS"""
        self.path_to_food = SimplePathfinder.find_path(
            self.body[0],  # Start from the head
            food_position,  # Goal is the food
            self.body[1:]   # Avoid the snake's body
        )

    def move(self):
        """Move the snake in the current direction"""
        if self.path_to_food:
            next_pos = self.path_to_food[0]
            self.direction = (next_pos[0] - self.body[0][0], next_pos[1] - self.body[0][1])
            self.path_to_food.pop(0)

        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.body.pop()

    def grow(self):
        """Grow the snake by adding an extra segment"""
        self.grow_to += 1

    def check_collision(self):
        """Check if the snake has collided with itself or the walls"""
        head = self.body[0]
        if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT or
            head in self.body[1:]):
            return True
        return False

    def draw(self, screen):
        """Draw the snake on the screen"""
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))






## explain 




"""
شرح الكود بالتفصيل الممل:
تعريف الفئة:

class Snake:

    تعريف فئة Snake تمثل الثعبان في اللعبة.
    هذه الفئة تحتوي على الخصائص (Attributes) والوظائف (Methods) التي تدير حركة الثعبان، نموه، التحقق من الاصطدام، وغيرها.

الدالة المُنشئة:

def __init__(self):
    self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    self.direction = (1, 0)
    self.path_to_food = []
    self.grow_to = 0

    self.body:
        قائمة تحتوي على مواقع جسم الثعبان.
        يبدأ الثعبان من نقطة وسط الشبكة (GRID_WIDTH // 2, GRID_HEIGHT // 2).

    self.direction:
        تمثل الاتجاه الحالي لحركة الثعبان.
        (1, 0) يعني أن الثعبان يتحرك أفقيًا نحو اليمين.

    self.path_to_food:
        قائمة سيتم تخزين المسار إلى الطعام بداخلها.
        يتم تحديد المسار باستخدام خوارزمية البحث عن المسار.

    self.grow_to:
        متغير لتتبع عدد القطع الإضافية التي يجب أن ينموها الثعبان.
        يتم زيادته عندما يأكل الثعبان الطعام.

إيجاد المسار إلى الطعام:

def find_path_to_food(self, food_position):
   Find the path to the food using BFS
    self.path_to_food = SimplePathfinder.find_path(
        self.body[0],  # Start from the head
        food_position,  # Goal is the food
        self.body[1:]   # Avoid the snake's body
    )

    food_position:
        إحداثيات موقع الطعام.

    SimplePathfinder.find_path:
        استدعاء الدالة find_path من الكلاس SimplePathfinder لتحديد أقصر مسار بين رأس الثعبان (self.body[0]) والطعام (food_position).
        يتجنب المسار الاصطدام بجسم الثعبان (self.body[1:]).

    self.path_to_food:
        يتم تخزين المسار الناتج (إذا وُجد) في هذه الخاصية.

حركة الثعبان:

def move(self):
   Move the snake in the current direction

    التحقق من وجود مسار إلى الطعام:

if self.path_to_food:
    next_pos = self.path_to_food[0]
    self.direction = (next_pos[0] - self.body[0][0], next_pos[1] - self.body[0][1])
    self.path_to_food.pop(0)

    إذا كان هناك مسار في self.path_to_food:
        الحصول على الخطوة التالية (next_pos).
        تحديث اتجاه الحركة (self.direction) بناءً على الفرق بين الموقع الحالي والموقع التالي.
        إزالة الخطوة المستخدمة من المسار (pop(0)).

إضافة رأس جديد:

head = self.body[0]
new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
self.body.insert(0, new_head)

    يتم حساب موقع الرأس الجديد بناءً على الاتجاه الحالي.
    يتم إضافة الرأس الجديد في بداية قائمة الجسم (self.body).

التعامل مع النمو:

    if self.grow_to > 0:
        self.grow_to -= 1
    else:
        self.body.pop()

        إذا كان self.grow_to > 0، يتم تقليل عدد القطع التي يجب أن ينموها الثعبان.
        إذا لم يكن هناك نمو مطلوب، يتم إزالة آخر قطعة من الجسم للحفاظ على طول الثعبان.

نمو الثعبان:

def grow(self):
    Grow the snake by adding an extra segment
    self.grow_to += 1

    زيادة قيمة self.grow_to، مما يعني أن الثعبان سينمو بمقدار قطعة إضافية.

التحقق من الاصطدام:

def check_collision(self):
    Check if the snake has collided with itself or the walls

    الحصول على رأس الثعبان:

head = self.body[0]

التحقق من الاصطدام بالجدران أو الجسم:

    if (head[0] < 0 or head[0] >= GRID_WIDTH or
        head[1] < 0 or head[1] >= GRID_HEIGHT or
        head in self.body[1:]):
        return True
    return False

        يتم التحقق من:
            هل رأس الثعبان خارج حدود الشبكة؟
            هل رأس الثعبان اصطدم بجسمه؟
        إذا تحقق أي من هذه الشروط، يتم إرجاع True للإشارة إلى حدوث تصادم.

رسم الثعبان:

def draw(self, screen):
    Draw the snake on the screen
    for segment in self.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    التكرار على كل قطعة في جسم الثعبان:
        لكل قطعة في self.body (الرأس + الأجزاء الأخرى).

    رسم القطعة:

pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    يتم رسم مستطيل يمثل القطعة:
        الموقع يتم حسابه بضرب إحداثيات القطعة في حجم الشبكة GRID_SIZE.
        اللون أخضر (GREEN).
        حجم القطعة هو GRID_SIZE - 1 لتجنب التداخل بين القطع.
"""