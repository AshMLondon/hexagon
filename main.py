#Hexagon Puzzle Solver
#Solves wooden puzzle - hexagon with 19 tiles, numbered 1-19
#All rows must add up to 38

#original completely brute force solver needs 444k iterations and takes 3.1s (PyPy)
#slightly improved - only check rows changed, and memo-ise = 1.49s but still 444k iterations
#complete thing -- 167,752,199 iters  474.4268388748169 seconds


import time

class HexPuzzle:

    def __init__(self):
        self.cells=["." for i in range(19)]
        self.cells_per_row=[3,4,5,4,3]

        check_rows=[]
        check_rows.append([[0, 1, 2], [3, 4, 5, 6], [7, 8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18]])
        check_rows.append([[0,3,7],[1,4,8,12],[2,5,9,13,16],[6,10,14,17],[11,15,18]])
        check_rows.append([[7,12,16],[3,8,13,17],[0,4,9,14,18],[1,5,10,15],[2,6,11]])
        self.check_rows=check_rows

        self.iterate_count=0
        self.memo={}

        self.all_solutions=FalseCah



    # def _create_rows(self):
    #     rows=[]
    #     cell=0
    #     for row_count in self.cells_per_row:
    #         this_row=[]
    #         for i in range(row_count):
    #             this_row.append(cell)
    #             cell+=1
    #         rows.append(this_row)
    #     print (rows)


    def check_puzzle_valid(self):
        for check_row_set in self.check_rows:
            for row in check_row_set:
                nums_in_row=[self.cells[c] for c in row]
                if "." not in nums_in_row:
                    if sum(nums_in_row)!=38:
                        return False
        return True

    def check_changed_rows_valid(self,cell):
        #here just check the 3 rows (different directions) that contain the cell (reference) number
        #first check if the specific rows already saved in a memo
        rows_to_check=self.memo.get(cell)
        if not rows_to_check:
            rows_to_check=[]
            for check_row_set in self.check_rows:
                for row in check_row_set:
                    if cell in row:
                        rows_to_check.append(row)
            self.memo[cell]=rows_to_check
            #save in memo for next time

        for row in rows_to_check:
            nums_in_row=[self.cells[c] for c in row]
            if "." not in nums_in_row:
                if sum(nums_in_row)!=38:
                    return False
        #otherwise...
        return True



    def display(self):
        cell=0
        for row_count in self.cells_per_row:
            to_display=["     ","   ",""][row_count - 3]
            for i in range(row_count):
                cell_num= self.cells[cell]
                if cell_num==".":
                    to_display += "   . "
                else:
                    to_display+="   "+str(cell_num)
                    if cell_num<10:
                        to_display+=" "
                cell+=1
            print(to_display)


    def recurse(self,level):

        if level==19:
            if self.all_solutions:
                print("SOLUTION FOUND")
                self.display()
                return False
            else:
                return True

        # print("Level",level)
        # self.display()

        self.iterate_count+=1

        for num in range(1,20):  #needs to start with 1 here, actual numbers to add, not addressing
            if num not in self.cells:
                self.cells[level]=num
                if self.check_changed_rows_valid(level):
                    result=self.recurse(level+1)
                    if result:
                        return True
                    #otherwise, number didn't work
        self.cells[level]="."
        return False #got to end of numbers







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hex=HexPuzzle()
    hex.display()
    print(hex.check_puzzle_valid())

    start_time=time.time()
    result=hex.recurse(0)
    print(result)
    print(f"{hex.iterate_count:,}")
    print(time.time()-start_time,"seconds")
    hex.display()
    print(hex.check_puzzle_valid())
    print(hex.memo)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
