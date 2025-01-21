import random

# 設定終止條件，例如設定最大代數
max_generations = 60
generation = 0

#定義
class Course:
    def __init__(self, class_code, day_code, period_code, subject_code, teacher_code):
        self.class_code = class_code
        self.day_code = day_code
        self.period_code = period_code
        self.subject_code = subject_code
        self.teacher_code = teacher_code

    def __str__(self):
        return f"Class: {self.class_code}, Day: {self.day_code}, Period: {self.period_code}, Subject: {self.subject_code}, Teacher: {self.teacher_code}"

#!!!建立初始族群 (Initial Population)!!!
#建立空白課表：
class Timetable:
    def __init__(self, total_days, periods_per_day):
        self.timetable = [[None for _ in range(periods_per_day)] for _ in range(total_days)]
        self.total_days = total_days
        self.periods_per_day = periods_per_day
        self.timetable = [[None for _ in range(periods_per_day)] for _ in range(total_days)]

    def add_course(self, course, day, period):
        self.timetable[day][period] = course

    def get_course(self, day, period):
        return self.timetable[day][period]

    def __str__(self):
        timetable_str = ""
        for day, day_courses in enumerate(self.timetable, 1):
            timetable_str += f"Day {day}:\n"
            for period, course in enumerate(day_courses, 1):
                if course:
                    timetable_str += f"  Period {period}: {course}\n"
                else:
                    timetable_str += f"  Period {period}: Empty\n"
        return timetable_str
    def __len__(self):
        return len(self.timetable)
    def __getitem__(self, key):
        return self.timetable[key[0]][key[1]]

#填入課程：
courses = [
    Course(1, 1, 1, 101, 201),
    Course(1, 1, 2, 102, 202),
    Course(1, 1, 3, 111, 241),
    Course(1, 2, 2, 112, 212),
    Course(1, 2, 1, 141, 231),
    Course(1, 3, 2, 152, 222),
    Course(1, 1, 1, 101, 201),
    Course(1, 1, 2, 102, 202),
    Course(1, 1, 3, 111, 241),
    Course(1, 2, 2, 112, 212),
    Course(1, 2, 1, 141, 231),
    Course(1, 3, 2, 152, 222),
    Course(2, 3, 3, 103, 211),
    Course(3, 1, 4, 104, 212),
    Course(1, 4, 2, 105, 213),
    Course(2, 2, 3, 106, 214),
    Course(3, 5, 1, 107, 215),
    Course(1, 2, 4, 108, 216),
    Course(2, 4, 2, 109, 217),
    Course(3, 3, 3, 110, 218),
    Course(1, 5, 3, 111, 219),
    Course(2, 1, 2, 112, 220),
    Course(3, 2, 1, 113, 221),
    Course(1, 3, 4, 114, 222),
    Course(2, 4, 3, 115, 223),
    Course(3, 5, 2, 116, 224),
    Course(1, 1, 1, 117, 225),
    Course(2, 2, 4, 118, 226),
    Course(3, 3, 3, 119, 227),
]

# 將課程填入課表
def create_timetable(courses):
    timetable = Timetable(total_days=5, periods_per_day=7)
    random_courses = random.sample(courses, len(courses))  # 隨機排列課程
    for course in random_courses:
        added = False
        while not added:
            day = random.randint(0, 4)
            period = random.randint(0, 5)
            if not timetable.get_course(day, period):
                timetable.add_course(course, day, period)
                added = True
    return timetable

#!!!計算適應值 (Fitness Function)!!!
#設計一個懲罰函數用來評估染色體（即課表）是否違反了軟限制
#假設有一個軟限制是某個老師偏好星期一早上第一節不排課
#設計一個懲罰函數來評估違反這個條件的程度
def penalty_function(timetable):
    penalty = 0
    for day, day_courses in enumerate(timetable.timetable):
        for period, course in enumerate(day_courses):
            if course:
                # 假設教師偏好的情況
                if course.teacher_code >= 211 and course.teacher_code < 230:
                    # 星期一的第一節課
                    if day == 0 and period == 0:
                        penalty += 10  # 嚴重違反條件增加較高的懲罰值
                    # 星期一的其他時段
                    elif day == 0:
                        penalty += 1  # 較輕微違反條件增加較低的懲罰
    return penalty

# 計算適應值
def fitness_function(timetable):
    penalty = penalty_function(timetable)
    fitness = 1 / (1 + penalty)  # 適應值函數為懲罰函數的倒數
    return fitness

#!!!選擇 (Selection)!!!
#輪盤法
#population 是現有的染色體集合
#fitness_values 是對應的適應值集合
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    selected = random.choices(population, weights=probabilities)
    return selected[0]

#!!!交配 (Crossover)!!!
def single_point_crossover(parent1, parent2):#單點交配
    child1 = Timetable(parent1.total_days, parent1.periods_per_day)
    child2 = Timetable(parent2.total_days, parent2.periods_per_day)
    
    crossover_point = random.randint(1, parent1.total_days * parent1.periods_per_day - 1)

    for day in range(parent1.total_days):
        for period in range(parent1.periods_per_day):
            index = day * parent1.periods_per_day + period
            if index < crossover_point:
                child1.add_course(parent1.get_course(day, period), day, period)
                child2.add_course(parent2.get_course(day, period), day, period)
            else:
                child1.add_course(parent2.get_course(day, period), day, period)
                child2.add_course(parent1.get_course(day, period), day, period)
    
    return child1, child2

#!!!突變 (Mutation)!!!
def mutate_timetable(timetable):
    mutated_timetable = Timetable(timetable.total_days, timetable.periods_per_day)

    for day in range(timetable.total_days):
        for period in range(timetable.periods_per_day):
            if random.random() < mutation_rate:  # 根據突變率決定是否進行突變
                # 這裡可以是隨機選擇新的課程，或者改變原來課程的時間或天數等操作
                new_day = random.randint(0, timetable.total_days - 1)
                new_period = random.randint(0, timetable.periods_per_day - 1)
                mutated_timetable.add_course(timetable.get_course(day, period), new_day, new_period)
            else:
                mutated_timetable.add_course(timetable.get_course(day, period), day, period)
    
    return mutated_timetable

# 設定突變率
mutation_rate = 0.95  


# 初始化族群
example_population = [create_timetable(courses) for _ in range(10)]
# 主要演算法循環
while generation < max_generations:
    # 計算每個染色體的適應值
    example_fitness_values = [fitness_function(timetable) for timetable in example_population]
    
    # 選擇父母染色體
    parent_timetable1 = roulette_wheel_selection(example_population, example_fitness_values)
    parent_timetable2 = roulette_wheel_selection(example_population, example_fitness_values)
    
    # 交配並產生子代
    child_timetable1, child_timetable2 = single_point_crossover(parent_timetable1, parent_timetable2)
    
    # 突變子代
    mutated_child_timetable1 = mutate_timetable(child_timetable1)
    mutated_child_timetable2 = mutate_timetable(child_timetable2)
    
    # 產生新族群
    new_population = [mutated_child_timetable1, mutated_child_timetable2] + example_population[2:]
    new_fitness_values = [fitness_function(timetable) for timetable in new_population]
    
    # 更新族群和對應的適應值
    example_population = new_population
    example_fitness_values = new_fitness_values
    
    # 增加代數
    generation += 1
    
    # 列印當前代數和最佳適應值
    best_fitness = max(example_fitness_values)
    print(f"Generation {generation}: Best Fitness = {best_fitness}")

# 最後，找到最優解
best_timetable_index = example_fitness_values.index(max(example_fitness_values))
best_timetable = example_population[best_timetable_index]
print("Best Timetable:")
print(best_timetable)