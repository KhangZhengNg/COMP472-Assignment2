

goal_state_1 = [1, 2, 3, 4, 5, 6, 7, 0]
goal_state_2 = [1, 3, 5, 7, 2, 4, 6 ,0]


input_file = input("Enter the input file:")
# samplePuzzles.txt
file = open(input_file, "r")
input_list = list()
for x in file:
  input_list.append(x)
file.close()

print(input_list[0])
print(input_list[1])
print(input_list[2])