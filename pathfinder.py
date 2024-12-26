import collections
import random



WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE



class SimplePathfinder:
    @staticmethod
    def find_path(start, goal, snake_body):
        """Breadth-First Search (BFS) to find the shortest path to the food"""
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        queue = collections.deque([[start]])
        visited = set([start])

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == goal:
                return path[1:]  # Exclude the first element (current position)

            for move in moves:
                next_pos = (current[0] + move[0], current[1] + move[1])
                if (0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT and
                        next_pos not in snake_body and next_pos not in visited):
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append(new_path)
                    visited.add(next_pos)
        return []  # No path found





###  explain 


"""
. تعريف الكلاس:

class SimplePathfinder:

    تعريف كلاس يسمى SimplePathfinder.
    الكلاس يحتوي على منطق لإيجاد المسار باستخدام البحث في العرض (BFS).

2. تعريف الدالة find_path كدالة ثابتة:

    @staticmethod
    def find_path(start, goal, snake_body):

    @staticmethod: تجعل الدالة ثابتة، مما يعني أنها يمكن استدعاؤها بدون إنشاء كائن من الكلاس.
    المدخلات:
        start: نقطة البداية (إحداثيات رأس الثعبان مثل (x, y)).
        goal: نقطة الهدف (إحداثيات الطعام مثل (x, y)).
        snake_body: قائمة تحتوي على أجزاء جسم الثعبان لتجنب الاصطدام.

3. تعريف الاتجاهات الممكنة:

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    moves: قائمة الاتجاهات الممكنة للحركة:
        (1, 0): التحرك إلى اليمين.
        (-1, 0): التحرك إلى اليسار.
        (0, 1): التحرك إلى الأسفل.
        (0, -1): التحرك إلى الأعلى.

4. إنشاء قائمة انتظار ومجموعة للزيارات:

        queue = collections.deque([[start]])
        visited = set([start])

    queue: قائمة انتظار (Queue) تُستخدم لتتبع المسارات المحتملة.
        تبدأ بقائمة تحتوي على مسار واحد وهو [start] (موقع الرأس فقط).
        يتم استخدام collections.deque لأنه أكثر كفاءة في عمليات الإدراج والحذف من الطرفين.
    visited: مجموعة (Set) لتخزين النقاط التي تمت زيارتها.
        تبدأ بـ start لتجنب إعادة زيارتها.

5. بدء حلقة البحث BFS:

        while queue:

    طالما أن queue تحتوي على مسارات، تستمر الحلقة.
    الهدف هو استكشاف جميع المسارات الممكنة حتى يتم العثور على المسار إلى الهدف.

6. استخراج المسار الحالي من قائمة الانتظار:

            path = queue.popleft()
            current = path[-1]

    path: استخراج أول مسار من قائمة الانتظار (بداية الاستكشاف).
    current: النقطة الحالية، وهي آخر نقطة في المسار الحالي.

7. التحقق من الوصول إلى الهدف:

            if current == goal:
                return path[1:]  # Exclude the first element (current position)

    إذا كانت النقطة الحالية current هي الهدف goal:
        يتم إرجاع المسار بدون النقطة الأولى (لأنها تمثل نقطة البداية).

8. استكشاف الجيران:

            for move in moves:
                next_pos = (current[0] + move[0], current[1] + move[1])

    for move in moves: تجربة كل الاتجاهات الممكنة.
    next_pos: النقطة الجديدة (الإحداثيات) بناءً على الاتجاه.

9. التحقق من صلاحية النقطة الجديدة:

                if (0 <= next_pos[0] < GRID_WIDTH and 0 <= next_pos[1] < GRID_HEIGHT and
                        next_pos not in snake_body and next_pos not in visited):

    next_pos يجب أن:
        تكون داخل حدود الشبكة.
        لا تكون جزءًا من جسم الثعبان.
        لم تتم زيارتها من قبل.

10. إضافة المسار الجديد إلى قائمة الانتظار:

                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append(new_path)
                    visited.add(next_pos)

    new_path: نسخة جديدة من المسار الحالي مع إضافة النقطة الجديدة.
    يتم:
        إضافة المسار الجديد إلى queue.
        إضافة next_pos إلى مجموعة visited لمنع إعادة زيارتها.

11. إرجاع مسار فارغ عند الفشل:

        return []  # No path found

    إذا انتهت الحلقة دون العثور على هدف، يتم إرجاع قائمة فارغة.
"""