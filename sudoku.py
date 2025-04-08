class Sudoku:
    def __init__(self, grid=None):
        # 初始化数独网格
        # 如果没有提供网格，创建一个空的9x9网格（0表示空单元格）
        if grid:
            self.grid = [row[:] for row in grid]  # 创建深拷贝
        else:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
    
    def print_grid(self):
        """打印数独网格，以可读格式展示"""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print('-' * 21)  # 每3行打印一条分隔线
            
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print('|', end=' ')  # 每3列打印一条分隔符
                
                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(self.grid[i][j], end=' ')
    
    def is_valid(self, num, pos):
        """检查一个数字是否可以放在特定位置上"""
        row, col = pos
        
        # 检查行
        for j in range(9):
            if self.grid[row][j] == num and j != col:
                return False
        
        # 检查列
        for i in range(9):
            if self.grid[i][col] == num and i != row:
                return False
        
        # 检查3x3宫格
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == num and (i, j) != (row, col):
                    return False
        
        return True
    
    def possible_number(self):
        """
        为未确定的单元格推断出可能的候选值集合。
        
        返回:
            一个9x9的二维数组，其中每个元素是该单元格可能的取值列表。
        """
        # 初始化可能性网格：对于每个单元格，存储可能的值列表
        possibilities = [[[] for _ in range(9)] for _ in range(9)]
        
        # 对于网格中的每个单元格
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    # 如果单元格已经有值，它是唯一可能的值
                    possibilities[i][j] = [self.grid[i][j]]
                else:
                    # 对于空单元格，从所有可能性开始（1-9）
                    possibilities[i][j] = list(range(1, 10))
                    
                    # 移除同一行中已经出现的数字
                    for col in range(9):
                        if self.grid[i][col] != 0 and self.grid[i][col] in possibilities[i][j]:
                            possibilities[i][j].remove(self.grid[i][col])
                    
                    # 移除同一列中已经出现的数字
                    for row in range(9):
                        if self.grid[row][j] != 0 and self.grid[row][j] in possibilities[i][j]:
                            possibilities[i][j].remove(self.grid[row][j])
                    
                    # 移除同一个3x3宫格中已经出现的数字
                    box_row, box_col = (i // 3) * 3, (j // 3) * 3
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if self.grid[r][c] != 0 and self.grid[r][c] in possibilities[i][j]:
                                possibilities[i][j].remove(self.grid[r][c])
        
        return possibilities
    
    def last_remaining_cell(self):
        """
        唯一剩余数，从当前数独的确定值出发，确定那些只有一个候选值的单元格。
        
        策略：
        1. 调用possible_number：获取所有单元格的候选值；
        2. 遍历行：寻找行中是否已经有8个已经填写的数字，剩下的一个空格可以确定；
        3. 遍历列：寻找列中是否已经有8个已经填写的数字，剩下的一个空格可以确定；
        4. 遍历所有九宫格：寻找宫格中是否已经有8个已经填写的数字，剩下的一个空格可以确定；
        
        返回:
            是否成功填入了新的确定值。
        """
        # 获取所有单元格当前的可能值
        possibilities = self.possible_number()
        made_progress = False  # 记录是否有进展
        
        # 1. 检查只有一个可能值的单元格
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0 and len(possibilities[i][j]) == 1:
                    self.grid[i][j] = possibilities[i][j][0]
                    made_progress = True
        
        # 2. 检查行：如果一个数字在一行中只能放在一个单元格中
        for i in range(9):
            # 对于每个可能的数字1-9
            for num in range(1, 10):
                # 如果这个数字已经在这一行中存在，跳过
                if num in [self.grid[i][j] for j in range(9)]:
                    continue
                    
                possible_positions = []
                for j in range(9):
                    if self.grid[i][j] == 0 and num in possibilities[i][j]:
                        possible_positions.append(j)
                
                # 如果这个数字在这一行中只有一个可能的位置
                if len(possible_positions) == 1:
                    j = possible_positions[0]
                    self.grid[i][j] = num
                    made_progress = True
        
        # 3. 检查列：如果一个数字在一列中只能放在一个单元格中
        for j in range(9):
            # 对于每个可能的数字1-9
            for num in range(1, 10):
                # 如果这个数字已经在这一列中存在，跳过
                if num in [self.grid[i][j] for i in range(9)]:
                    continue
                    
                possible_positions = []
                for i in range(9):
                    if self.grid[i][j] == 0 and num in possibilities[i][j]:
                        possible_positions.append(i)
                
                # 如果这个数字在这一列中只有一个可能的位置
                if len(possible_positions) == 1:
                    i = possible_positions[0]
                    self.grid[i][j] = num
                    made_progress = True
        
        # 4. 检查3x3宫格：如果一个数字在一个宫格中只能放在一个单元格中
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                # 对于每个可能的数字1-9
                for num in range(1, 10):
                    # 如果这个数字已经在这个宫格中存在，跳过
                    if num in [self.grid[i][j] for i in range(box_row, box_row + 3) 
                                             for j in range(box_col, box_col + 3)]:
                        continue
                    
                    possible_positions = []
                    for i in range(box_row, box_row + 3):
                        for j in range(box_col, box_col + 3):
                            if self.grid[i][j] == 0 and num in possibilities[i][j]:
                                possible_positions.append((i, j))
                    
                    # 如果这个数字在这个宫格中只有一个可能的位置
                    if len(possible_positions) == 1:
                        i, j = possible_positions[0]
                        self.grid[i][j] = num
                        made_progress = True
        
        return made_progress

    def apply_strategies(self, max_iterations=10):
        """
        应用策略来尽可能填入确定的值
        
        参数:
            max_iterations: 最大迭代次数，防止死循环
        
        返回:
            迭代次数和是否有变化
        """
        iterations = 0
        made_changes = False
        
        while iterations < max_iterations:
            progress = self.last_remaining_cell()
            if not progress:
                break
            made_changes = True
            iterations += 1
        
        return iterations, made_changes


def main():
    print("=== 数独策略验证测试 ===\n")
    
    # 示例1：测试基本的候选值推断功能
    print("测试1：基本的候选值推断功能")
    test_grid1 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    sudoku1 = Sudoku(test_grid1)
    print("初始数独:")
    sudoku1.print_grid()
    
    possibilities = sudoku1.possible_number()
    
    # 检查特定位置的候选值
    print("\n位置(0,3)的候选值:", possibilities[0][3])
    print("位置(1,2)的候选值:", possibilities[1][2])
    
    # 示例2：行唯一值约束测试
    print("测试2：行唯一值约束测试")
    row_test = [
        [0, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    sudoku2 = Sudoku(row_test)
    print("初始数独（第一行除了位置0以外都已填充）:")
    sudoku2.print_grid()
    
    made_progress = sudoku2.last_remaining_cell()
    print("\n应用last_remaining_cell后:")
    sudoku2.print_grid()
    
    if made_progress and sudoku2.grid[0][0] == 1:
        print("测试2通过：成功使用行约束确定单元格值！\n")
    else:
        print("测试2失败：未能使用行约束确定单元格值！\n")
    
    # 示例3：列唯一值约束测试
    print("测试3：列唯一值约束测试")
    col_test = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    sudoku3 = Sudoku(col_test)
    print("初始数独（第一列除了位置0以外都已填充）:")
    sudoku3.print_grid()
    
    made_progress = sudoku3.last_remaining_cell()
    print("\n应用last_remaining_cell后:")
    sudoku3.print_grid()
    
    if made_progress and sudoku3.grid[0][0] == 1:
        print("测试3通过：成功使用列约束确定单元格值！\n")
    else:
        print("测试3失败：未能使用列约束确定单元格值！\n")
    
    # 示例4：九宫格唯一值约束测试
    print("测试4：九宫格唯一值约束测试")
    box_test = [
        [0, 2, 3, 0, 0, 0, 0, 0, 0],
        [4, 5, 6, 0, 0, 0, 0, 0, 0],
        [7, 8, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    sudoku4 = Sudoku(box_test)
    print("初始数独（左上九宫格除了位置(0,0)以外都已填充）:")
    sudoku4.print_grid()
    
    made_progress = sudoku4.last_remaining_cell()
    print("\n应用last_remaining_cell后:")
    sudoku4.print_grid()
    
    if made_progress and sudoku4.grid[0][0] == 1:
        print("测试4通过：成功使用九宫格约束确定单元格值！\n")
    else:
        print("测试4失败：未能使用九宫格约束确定单元格值！\n")
    
    # 示例5：综合测试
    print("测试5：综合测试")
    advanced_test = [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ]
    
    sudoku5 = Sudoku(advanced_test)
    print("初始较复杂的数独:")
    sudoku5.print_grid()
    
    iterations, made_changes = sudoku5.apply_strategies()
    print(f"\n应用策略后 (迭代 {iterations} 次):")
    sudoku5.print_grid()
    
    if made_changes:
        print(f"测试5：成功应用策略并填入了确定的值，共迭代{iterations}次！\n")
    else:
        print("测试5失败：未能填入任何确定的值！\n")
    
    print("=== 所有测试完成 ===")

if __name__ == "__main__":
    main()