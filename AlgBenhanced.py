import os
import sys
import time
import random


def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file, 'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string


def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0, a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int


def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""  # "middle_string" and "to_index" play no role in the case of error
    to_index = -1  # but need to initialized to something as they are returned
    start = a_string.find(from_string, from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        # trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string, start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            # trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string, to_index, flag


def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        # trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1  # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0, row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag


def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1, num_cities):
        for j in range(0, i):
            distance_matrix[i][j] = distance_matrix[j][i]


# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile535.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file, 44, 122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file, 44, 122)
file_string = file_string + ","  # we need to add a final comma to find the city distances
# as we look for numbers between commas
print("I'm working with the file " + input_file + ".")

# get the name of the file

name_of_file, to_index, flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string, to_index, flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1  # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "hkxx26"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "AJ"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Sung"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "GA"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF': 'brute-force search',
                   'BG': 'basic greedy search',
                   'BS': 'best_first search without heuristic data',
                   'ID': 'iterative deepening search',
                   'BH': 'best_first search with heuristic data',
                   'AS': 'A* search',
                   'HC': 'hilling climbing search',
                   'SA': 'simulated annealing search',
                   'GA': 'genetic algorithm'}


#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

import time

# Calculates Score for tour.
def score(matrix, tour):
    tour_score = 0
    prev = tour[0]
    for x in tour:
        tour_score += matrix[prev][x]
        prev = x
    tour_score += matrix[tour[-1]][tour[0]]
    return tour_score


# Generates the initial population.
def gen_pop(matrix, city_num, size):
    pop = []
    for x in range(size):
        new_tour = random.sample(range(0, city_num), city_num)
        new_score = score(matrix, new_tour)
        pop.append((new_score, new_tour))
    return pop


# Picks a random tour from the population.
def rand_pop(pop, pop_size):
    fighter_num = int(pop_size / 4)
    fighters = random.sample(range(0, pop_size), fighter_num)
    champion = pop[fighters[0]]
    for fighter in fighters:
        if pop[fighter][0] < champion[0]:
            champion = pop[fighter]
    return champion[1]


# Mutates (AKA swaps two cities) if the threshold is passed.
def mutate(city_num, tour, mutate_prob):
    for city in range(city_num):
        if random.random() < mutate_prob:
            swap = random.randint(0, city_num - 1)
            tour[city], tour[swap] = tour[swap], tour[city]
    return tour


# Creates two children from x and y then returns the lowest scoring child.
def child(x, y, matrix, city_num, mutate_prob):
    split_a = random.randint(0, city_num)
    split_b = random.randint(0, city_num)

    if split_a < split_b:
        z1 = x[:split_a] + y[split_a:split_b] + x[split_b:]
        z2 = y[:split_a] + x[split_a:split_b] + y[split_b:]
    else:
        z1 = x[:split_b] + y[split_b:split_a] + x[split_a:]
        z2 = y[:split_b] + x[split_b:split_a] + y[split_a:]

    dup_z1 = [idx for idx, item in enumerate(z1) if item in z1[:idx]]
    dup_z2 = [idx for idx, item in enumerate(z2) if item in z2[:idx]]

    for x in range(len(dup_z1)):
        z1[dup_z1[x]], z2[dup_z2[x]] = z2[dup_z2[x]], z1[dup_z1[x]]

    z1 = mutate(city_num, z1, mutate_prob)
    z2 = mutate(city_num, z2, mutate_prob)

    z1_score = score(matrix, z1)
    z2_score = score(matrix, z2)

    if z1_score < z2_score:
        return z1_score, z1
    else:
        return z2_score, z2


# Main function for the Genetic Algorithm.
def elitism(pop, pop_size, elite):
    pop.sort()
    del pop[pop_size - elite:]
    pop += elite * [pop[0]]
    return pop


# Migrates random members of the population to the other population.
def migrate(pop_a, pop_b, pop_migrate, pop_size):
    for swap in range(pop_migrate):
        index_a = random.randint(0, pop_size - 1)
        index_b = random.randint(0, pop_size - 1)
        pop_a[index_a], pop_b[index_b] = pop_b[index_b], pop_a[index_a]
    return pop_a, pop_b


def island(matrix, city_num, pop, pop_size, mutate_prob, elite):
    new_pop = []
    for count in range(pop_size):
        x = rand_pop(pop, pop_size)
        y = rand_pop(pop, pop_size)
        z = child(x, y, matrix, city_num, mutate_prob)

        new_pop.append(z)

    return elitism(new_pop, pop_size, elite)


# Main function for the Genetic Algorithm.
def main(matrix, city_num):
    ### Set time for break
    start, timeout = time.time(), 100

    pop_size = 50
    elite = 25
    mutate_prob = .0005
    pop_migrate = 15

    pop_a = gen_pop(matrix, city_num, pop_size)
    pop_b = gen_pop(matrix, city_num, pop_size)

    # 350 x 10 = 3500 iterations (half of AlgBbasic as there is 2x populations here so makes the same number of iterations overall).
    for x in range(350):
        for y in range(10):
            pop_a = island(matrix, city_num, pop_a, pop_size, mutate_prob, elite)
            pop_b = island(matrix, city_num, pop_b, pop_size, mutate_prob, elite)
        pop_a, pop_b = migrate(pop_a, pop_b, pop_migrate, pop_size)

        ### Added Break check
        if (time.time() - start) > timeout:
            break

    if pop_a[0][0] < pop_b[0][0]:
        return pop_a[0][1], pop_a[0][0]
    else:
        return pop_b[0][1], pop_b[0][0]

tour, tour_length = main(distance_matrix, num_cities)
#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below; that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################

check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities - 1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(
        tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format; if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(
        time.localtime(time.time()))  # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
    # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name, 'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1, num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")
