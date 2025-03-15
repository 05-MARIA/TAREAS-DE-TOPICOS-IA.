import random
import time

class TabuSearch:
    def __init__(self, n=8, max_iterations=1000, tabu_tenure=10):
        self.n = n
        self.max_iterations = max_iterations
        self.tabu_tenure = tabu_tenure
        self.tabu_list = []

    def generate_initial_solution(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def calculate_conflicts(self, state):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self, state):
        neighbors = []
        for col in range(self.n):
            for row in range(self.n):
                if state[col] != row:
                    new_state = list(state)
                    new_state[col] = row
                    neighbors.append(new_state)
        return neighbors

    def tabu_search(self):
        current_state = self.generate_initial_solution()
        best_state = list(current_state)
        best_conflicts = self.calculate_conflicts(best_state)
        
        iteration = 0
        start_time = time.time()

        while iteration < self.max_iterations and best_conflicts > 0:
            neighbors = self.get_neighbors(current_state)
            best_candidate = None
            best_candidate_conflicts = float('inf')
            
            for neighbor in neighbors:
                if neighbor not in self.tabu_list:
                    conflicts = self.calculate_conflicts(neighbor)
                    if conflicts < best_candidate_conflicts:
                        best_candidate = neighbor
                        best_candidate_conflicts = conflicts
            
            if best_candidate is None:
                break
            
            current_state = best_candidate
            self.tabu_list.append(current_state)
            if len(self.tabu_list) > self.tabu_tenure:
                self.tabu_list.pop(0)
            
            if best_candidate_conflicts < best_conflicts:
                best_state = best_candidate
                best_conflicts = best_candidate_conflicts
            
            iteration += 1

        end_time = time.time()
        return best_state, best_conflicts, iteration, end_time - start_time

if __name__ == "__main__":
    tabu_solver = TabuSearch()
    solution, conflicts, moves, exec_time = tabu_solver.tabu_search()
    print(f"Mejor solución encontrada: {solution}")
    print(f"Conflictos restantes: {conflicts}")
    print(f"Movimientos realizados: {moves}")
    print(f"Tiempo de ejecución: {exec_time:.4f} segundos")
