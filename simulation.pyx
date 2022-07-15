# distutils: language = c++
# cython: profile=True

from libcpp.vector cimport vector
from libcpp.map cimport map
from cython.operator cimport dereference, postincrement
from libcpp.algorithm cimport unique

from cython.parallel import prange

#vectors can be used as keys in a map 

cdef extern from "<random>" namespace "std":
    # mt19937 as before
    cdef cppclass mt19937:
      mt19937() except +
      mt19937(unsigned int) except +
    cdef cppclass discrete_distribution[T]:
        discrete_distribution()
        # The following constructor is really a more generic template class
        # but tell Cython it only accepts vector iterators
        discrete_distribution(vector.iterator first, vector.iterator last)
        T operator()(mt19937 gen)


cdef class SimRand: 

    cdef:
        vector[vector[int]] liveCellsNew
        vector[vector[int]] liveCellsCurr
        vector[vector[int]] liveCellsPrev
        map[vector[int], int] changeList
        map[vector[int], int].iterator chg_it
        vector[vector[int]].iterator cells_it
        vector[int] neighbour
        vector[int] any_cell

        int numLiveCells
        int generation
        bint allDead
        int fert
        vector[int] Etuple
        int etuple_size

        vector[vector[int]] unmirrored_cells
        vector[vector[int]] mirror_cells

        int length_cell_list

        vector[int] cell_addresses
        vector[int] random_addr
        vector[vector[int]] cellsToSimulate

        vector[vector[int]] list_of_rules
    
    def __cinit__(self, rule_num, num_sims): 
        cdef int i = 0 
        cdef vector[int] cell = [1000, 1000, 1000]
        for i in range(3000): 
            self.liveCellsCurr.push_back(cell)
            self.liveCellsPrev.push_back(cell)
            self.liveCellsNew.push_back(cell)
        
        self.list_of_rules = [[2, 3, 100, 5], [2, 5, 100, 5], [2, 7, 100, 5], [3, 5, 100, 5], [3, 6, 100, 5],
                                      [3, 7, 100, 5], [3, 8, 100, 5], [4, 100, 5], [4, 7, 100, 5], [5, 7, 100, 6],
                                      [5, 8, 100, 5], [8, 100, 5]]
        self.reset()
        
        self.gen_cell_indices()
        self.cell_addresses = range(self.length_cell_list)
        self.neighbour = [0, 0, 0]

        cdef sim_num = 0 
        for sim_num in range(num_sims):
            if sim_num % 100 == 0:
                print(f"Simulation number {sim_num}")
            self.sym_rand_soup()
            #print(self.cellsToSimulate)
            self.ca_beg_to_end(self.list_of_rules[rule_num], False)
            self.cellsToSimulate.clear()
            self.random_addr.clear()
            #print(f"{self.cellsToSimulate.size()}")
            self.reset()
            #print("\n")
    
    cpdef reset(self):
        self.numLiveCells = 0 
        self.generation = 1 
        self.allDead = False

    cpdef parse_rule(self, rule):
        cdef bint store_fert = False
        cdef int i = 0 
        for i in rule:
            if store_fert:
                self.fert = i
            elif i == 100:
                store_fert = True
            else:
                self.Etuple.push_back(i)

        self.etuple_size = self.Etuple.size()

    cpdef ca_beg_to_end(self, rule, characterize = False):

        charac = characterize
        self.parse_rule(rule)
        self.numLiveCells = self.cellsToSimulate.size()

        cdef int cell_num = 0 
        for cell_num in range(self.numLiveCells):
            self.liveCellsCurr[cell_num] = self.cellsToSimulate[cell_num]

        self.ca_count_neigh()

        while not self.allDead:
            b = self.numLiveCells
            #print(f"Num cells {b}")
            #print(f"Generation {self.generation}")

            #print(self.liveCellsCurr)
            
            self.ca_loop_logic(charac)

    cpdef ca_loop_logic(self, charac): 

        self.ca_update_live()
        #self.numLiveCells = self.liveCellsCurr.size()
        #self.find_extreme_pattern

        if self.numLiveCells == 0: 
            self.allDead = True
        elif self.generation == 15: 
            self.allDead = True

        self.generation += 1
        #self.contigList.clear()
        self.ca_count_neigh()

    cpdef ca_count_neigh(self):

        cdef bint xyz_zero = False
        cdef int xcoord, ycoord, zcoord = 0
        cdef int cell_num = 0 
        cdef int j = 0 

        cdef int x = -1
        cdef int y = -1
        cdef int z = -1

        for cell_num in range(self.numLiveCells): 
            self.any_cell = self.liveCellsCurr[cell_num]
            xcoord = self.any_cell[0]
            ycoord = self.any_cell[1]
            zcoord = self.any_cell[2]

            for x in range(-1, 2):
                for y in range(-1, 2):
                    for z in range(-1, 2):
                        xyz_zero = False
                        #self.neighbour = [xcoord + x, ycoord + y, zcoord + z]
                        self.neighbour[0] = xcoord + x 
                        self.neighbour[1] = ycoord + y
                        self.neighbour[2] = zcoord + z
                        xyz_zero = x == 0 and y == 0 and z == 0
                        if not xyz_zero:
                            self.chg_it = self.changeList.find(self.neighbour)
                            if self.chg_it != self.changeList.end():
                                self.changeList[self.neighbour] += 1
                            else: 
                                self.changeList[self.neighbour] = 1

    cpdef ca_update_live(self):
        
        self.chg_it = self.changeList.begin()
        cdef int count = 0 
        cdef int vec_pos = 0
        cdef int i = 0 

        cdef bint inLiveCells = False
        cdef bint count_in_etuple = False

        self.numLiveCells = 0 

        while(self.chg_it != self.changeList.end()): 
            self.any_cell = dereference(self.chg_it).first
            count = dereference(self.chg_it).second

            inLiveCells = False 
            
            for vec_pos in range(self.numLiveCells): 
                if self.any_cell == self.liveCellsCurr[vec_pos]: 
                    inLiveCells = True
            
            if not inLiveCells and count == self.fert: 
                #self.liveCellsNew.push_back(self.any_cell)
                self.liveCellsNew[self.numLiveCells] = self.any_cell
                self.numLiveCells += 1

            else:
                count_in_etuple = False
                for i in range(self.etuple_size): 
                    if count == self.Etuple[i]:
                        count_in_etuple = True
                
                if inLiveCells and count_in_etuple: 
                    #self.liveCellsNew.push_back(self.any_cell)
                    self.liveCellsNew[self.numLiveCells] = self.any_cell
                    self.numLiveCells += 1

            postincrement(self.chg_it)

        #self.numLiveCells = self.liveCellsNew.size()
        # cdef int k = 0 
        # for k in range(self.numLiveCells):
        #     print self.liveCellsNew[k],

        cdef int j = 0 
        for j in range(self.numLiveCells): 
            self.liveCellsCurr[j] = self.liveCellsNew[j]

        #self.liveCellsNew.clear()
        self.changeList.clear()

    
    cpdef gen_cell_indices(self):
        cdef int x = 60
        cdef int y = 60
        cdef int z = 60
        cdef vector[int] reg_cell
        cdef vector[int] mirror_cell

        for x in range(60, 70):
            for y in range(60, 65):
                for z in range(60,70):
                    reg_cell = [x, y, z]
                    if y == 64:
                        mirror_cell = [x, 65, z]
                    elif y == 63:
                        mirror_cell = [x, 66, z]
                    elif y == 62:
                        mirror_cell = [x, 67, z]
                    elif y == 61:
                        mirror_cell = [x, 68, z]
                    else:
                        mirror_cell = [x, 69, z]

                    self.unmirrored_cells.push_back(reg_cell)
                    self.mirror_cells.push_back(mirror_cell)

        self.length_cell_list = len(self.unmirrored_cells)

    cpdef sym_rand_soup(self):

        # want 20 % density so 100 unmirrored cells + 100 mirrored cells
        # randomly select 100 numbers between 0 and len(self.unmirrored_cells)
        # random_addresses = random.sample(range(0, self.length_cell_list), self.num_init_cells)
        cdef mt19937 gen = mt19937(5)
        cdef discrete_distribution[int] dd = discrete_distribution[int](self.cell_addresses.begin(),self.cell_addresses.end())

        cdef int j = 0 
        cdef int addr = 0 
        cdef int k = 0 
        cdef bint duplicate = False
        for j in range(100):
            addr = dd(gen)
            duplicate = False
            for k in range(self.random_addr.size()): 
                if addr == self.random_addr[k]: 
                    duplicate = True
                
            if not duplicate:
                self.random_addr.push_back(dd(gen))
        #cdef set[int] random_add_set(self.random_addr.begin(), self.random_addr.end())
        #unique(self.random_addr.begin(), self.random_addr.end())

        cdef int i = 0
        cdef int address = 0 
        for i in range(self.random_addr.size()):
            address = self.random_addr[i]
            self.cellsToSimulate.push_back(self.unmirrored_cells[address])
            self.cellsToSimulate.push_back(self.mirror_cells[address])


cdef class CaptureSim: 

    def __cinit__(self, rule_num, num_sims): 
        super.__cinit__(rule_num, num_sims)

 

