import sympy
def get_fitness(eq,val):
    eq=eq.lower()
    x=sympy.symbols("x")
    eq=sympy.simplify(eq)
    return eq.subs(x,val)

def get_fac_input():
    global eqn
    n=int(input("Enter number of facilities : "))
    fac=list()
    i=0
    while i<n:
        print ("\nEnter facility ",i+1," : ")
        f=input().upper()
        if (f not in fac):
            fac.append(f)
            i+=1
        else:
            print("\nFacility already exists! Please Retry")
    eqn=input("\n\nEnter the weight equation f(x) : ")
    return fac,eqn
def get_n_connec():
    n = int(input("\n\nEnter no of connections for the facility : "))
    if n<=0:
        print("\nInvalid Number of connections! Try Again!")
        return get_n_connec()
    else:
        return n
def get_connections(fac):
    global eqn
    Connections=list()
    for i in fac:
        print ("\n\n\nFacility ",i," : ")
        n = get_n_connec()
        j=0
        while j<n:
            try:
                print("\nConnection ",j+1," : ")
                end=input("\nEnter 'To' facility : ").upper()
                if (end==i):
                    print("\nConnection cannot be to itself! Try again")
                elif(end not in fac):
                    print("\nFacility not existent! Try again")
                else:
                    fitness=float(input("\n\n\nEnter the value of x for Weight Function : "))
                    fitness=get_fitness(eqn,fitness)
                    Connections.append((i,end,fitness))
                    j+=1
            except:
                print("\nInvalid Input! Try again!\n")        
    return Connections

def get_Slist(required_start,connections):
    Branches=list()
    start_point=0
    for every_element_connnection in connections:
        if every_element_connnection[start_point]==required_start:
            Branches.append(every_element_connnection)
    return Branches
def find_paths(start,end,Connections,prestack,covered_fac):
	global paths
	startl=get_Slist(start,Connections)
	print("startl : ",startl)
	covered_fac.append(start)
	preStack=prestack
	print("prestack:",prestack)
	for i in startl:
		print(i[0],"prestack",prestack)
		if i[0]==start and i[1]==end:
			preStack.append(i)
			print("preStack:",preStack,"p:",paths)
			paths[len(paths)]=preStack
			#paths.append(preStack)
			print("paths :",paths)
			print("preStack:",preStack)
		elif i[1] in covered_fac:
			pass
		else:
			preStack.append(i)
			print("else statement")
			preStack=find_paths(i[1],end,Connections,preStack,covered_fac)
	else:
		print("prestack in else",prestack)
		P=list(prestack)
		for k in prestack:
			print("start:",start,"k ",k)
			if k[0]== start or k[1] == start:
				P.remove(k)
		prestack=P
		preStack=P
		print("k-Prestack",prestack)
		return prestack
def find_paths2(start,end,Connections,path_travelled_so_far,covered_fac):
	global paths
	Current_Branches=get_Slist(start,Connections)
	start_point=0
	end_point=1
	for every_branch in Current_Branches:
		current=[]
		Covered_fac=list(covered_fac)#hard copy
		Covered_fac.append(start)
		path_travelled_from_current_node=list(path_travelled_so_far)
		#print("start:",start,"end:",end,"prestack:",path_travelled_so_far,"covered_fac:",Covered_fac)
		if every_branch[start_point]==start and every_branch[end_point]==end:
			path_travelled_from_current_node.append(every_branch)
			paths[len(paths)]=path_travelled_from_current_node
		elif every_branch[end_point] in Covered_fac:
			pass
		else:
			path_travelled_from_current_node.append(every_branch)
			find_paths2(every_branch[end_point],end,Connections,path_travelled_from_current_node,Covered_fac)

def compute_show_paths(paths):
    global start,end
    l=len(paths)
    paths_and_weight=dict()
    weights=list()
    if l==1:
        print("There is only 1 possible way from",start," to ",end,":")
    elif l==0:
        print("There are ",l," possible ways from",start," to ",end,":")
        return None
    else:
        print("There are ",l," possible ways from",start," to ",end,":")
    for i in range(l):
        passed_facilities=list()
        weight=0
        for j in range(len(paths[i])):
            if paths[i][j][0] not in passed_facilities:
                passed_facilities.append(paths[i][j][0])
            if paths[i][j][1] not in passed_facilities:
                passed_facilities.append(paths[i][j][1])
            weight+=paths[i][j][2]
        #passed_facilities=tuple(set(passed_facilities))
        paths_and_weight[i]=(passed_facilities,weight)
        weights.append(weight)
    for i in paths_and_weight:
        print("Path ",i+1," : \n")
        s=str()
        for j in paths_and_weight[i][0]:
            s+=str(j)+"-->"
        s=s.rstrip('-->')
        print("-="*40)
        print(s,"\n\n")
        print("Weight : ",paths_and_weight[i][1],"\n\n")
        print("-="*40)
        
    return paths_and_weight,weights


def display(path):
    s=''
    for i in path[0]:
        s+=str(i)+'-->'
    s=s.rstrip('-->')
    print(s)
    
def findmin(paths_and_weight,weights):
    minimum_weight=min(weights)
    print("The Minimum and optimum path(s) are : ")
    for i in paths_and_weight:
        if paths_and_weight[i][1]==minimum_weight:
            print ("\n\n")
            print('*'*20)
            display(paths_and_weight[i])
            print("With a weight/cost of ",minimum_weight)
            print('*'*20)
def reset():
	global prestack,paths,covered_fac,preStack
	prestack=[]
	paths={}
	covered_fac=[]
	preStack=[]

def testcase():
    global paths,preStack,covered_fac,fac,eqn,Connections,start,end,paths_and_weight,weights
    reset()
    Connections=[('A', 'B', 4), ('A', 'F', 5), ('A', 'H', 8), ('B', 'S', 4), ('C', 'E', 2), ('C', 'S', 3), ('D', 'C', 4), ('D', 'G', 8), ('E', 'J', 4), ('E', 'N', 4), ('F', 'A', 5), ('F', 'K', 8), ('G', 'D', 8), ('G', 'H', 4), ('G', 'O', 4), ('H', 'A', 8), ('H', 'G', 4), ('H', 'J', 5), ('H', 'S', 7), ('I', 'M', 3), ('I', 'N', 4), ('J', 'E', 6), ('J', 'H', 5), ('J', 'K', 6), ('J', 'O', 9), ('J', 'T', 9), ('K', 'F', 8), ('K', 'G', 6), ('K', 'L', 5), ('K', 'O', 3), ('L', 'K', 5), ('L', 'T', 4), ('M', 'I', 3), ('M', 'Q', 2), ('M', 'T', 6), ('N', 'E', 4), ('N', 'I', 4), ('N', 'P', 6), ('N', 'R', 3), ('N', 'S', 6), ('O', 'G', 8), ('O', 'J', 5), ('O', 'K', 3), ('O', 'P', 4), ('P', 'N', 6), ('P', 'O', 4), ('Q', 'M', 2), ('Q', 'R', 4), ('Q', 'T', 7), ('R', 'N', 3), ('R', 'Q', 4), ('S', 'B', 4), ('S', 'C', 3), ('S', 'H', 7), ('S', 'N', 6), ('T', 'J', 9), ('T', 'L', 4), ('T', 'M', 6), ('T', 'Q', 7)]
    fac=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'J', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    eqn='x**2+3'
    start = input('Enter the starting point : ').upper()
    end = input('Enter the ending point : ').upper()
    find_paths2(start,end,Connections,preStack,covered_fac)
    paths_and_weight,weights=compute_show_paths(paths)
    findmin(paths_and_weight,weights)
    ans=input("\n\n Do you want to try again ? (Y/N) ").upper()
    return ans
    
def Run():
    global paths,preStack,covered_fac,fac,eqn,Connections,start,end,paths_and_weight,weights
    paths=dict()
    preStack=list()
    covered_fac=list()
    fac,eqn=get_fac_input()
    Connections = get_connections(fac)
    start = input('Enter the starting point : ').upper()
    end = input('Enter the ending point : ').upper()
    find_paths2(start,end,Connections,preStack,covered_fac)
    paths_and_weight,weights=compute_show_paths(paths)
    findmin(paths_and_weight,weights)
    ans=input("\n\n Do you want to try again ? (Y/N) ").upper()
    return ans

def RUN():
    global paths,preStack,covered_fac,fac,eqn,Connections,start,end,paths_and_weight,weights
    ans=input("Do you want to run the predefined testcase ? (Y/N) ").upper()
    if ans=='Y':
        return testcase()
    else:
        return Run()

    return ans
    
flag = True
while(flag):
    ans= RUN() 
    if ans=='Y':
        reset()
        RUN()
    else:
        print("Exiting!")
        flag=False
