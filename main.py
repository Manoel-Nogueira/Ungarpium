import json
import random
import clearconsole
import time

# Lendo o arquivo json
with open("plants.json", "r", encoding="utf-8") as file: 
    plants_data = json.load(file)

# Função para saber se o gene já existe naquele indivíduo
def IsEqual(son, gene) :

    isEqual = False

    for aux in range(0, 2) :

        if son[aux]["name"] == gene["name"] :

            isEqual = True
            break


    return isEqual

# Função para gerar a população inicial
def GenerateIndividual(selectedPlant) :

    solution = []
    ids = list(range(0, len(plants_data)))
    aux1 = 0

    while(aux1 < 3) :

        aux2 = random.choice(ids)
        ids.remove(aux2)

        if plants_data[aux2]["name"] != selectedPlant :

            solution.append(plants_data[aux2])

            aux1 += 1

    return solution

# Função para calcular a aptidão de cada indivíduo
def Fitness(individual, input) :

    fitnessValue = 18

    for aux in individual :

        if input[1] != aux["improves_soil"] :

            fitnessValue -= 1

        if input[2] != aux["cycle"] :

            fitnessValue -= 1

        if input[0] not in aux["compatible_plants"] :

            fitnessValue -= 2

        if input[0] in aux["incompatible_plants"] :

            fitnessValue -= 2

    return [individual, fitnessValue]

# Função para selecionar os indivíduos para a reprodução com base em sua aptidão/fitness
# Usando o método de seleção por torneios
def Selection(population) :

    selecteds = []

    for _ in range(len(population)) :

        clash = random.sample(population, 2)
        winner = max(clash, key = lambda aux : aux[1])
        selecteds.append(winner)

    return selecteds

# Função para combinar os pais e gerar dois novos filhos
def Crossover(parents) :

    children = []
    ids = list(range(0, len(parents)))

    while ids :

        cut = random.randint(0, 2)

        aux1 = random.choice(ids)
        ids.remove(aux1)

        aux2 = random.choice(ids)
        ids.remove(aux2)
        
        parent1 = parents[aux1][0]
        parent2 = parents[aux2][0]

        son1 = []
        son2 = []

        aux3 = 0
        while aux3 < 3 :
            
            if aux3 <= cut :

                son1.append(parent1[aux3])
                son2.append(parent2[aux3])
            
            else :

                son1.append(parent2[aux3])
                son2.append(parent1[aux3])

            aux3 += 1

        children.append(son1)
        children.append(son2)

    return children

# Função para criar mutações aleatórias 
def Mutation(children, mutationRate, initialPopulation) : 

    mutatedChildren = []

    for son in children :

        for aux in range(0, 2) :

            if random.random() < mutationRate :
                chosen = random.choice(initialPopulation)
                gene = random.choice(chosen)

                while IsEqual(son, gene) == True :
                    chosen = random.choice(initialPopulation)
                    gene = random.choice(chosen)

                son[aux] = gene
        
        mutatedChildren.append(son)

    return mutatedChildren

# Função para pegar as escolhas do usuário
def Input() :

    userInput = []
    cycles = ["curto", "médio", "longo"]

    run = True

    # Escolher a cultura
    while run :

        try :

            # Limpando o console
            clearconsole.ClearConsole()

            # Menu
            print("\033[32m \n\n#######------->  Escolha a cultura principal <-------####### \n")
            #print("\033[31m -1 -> Sair")
            print("\033[34m Culturas: \n")

            # Listando as culturas
            aux = 1
            for x in plants_data:
                print("\033[33m", aux, "->", x["name"])
                aux += 1

            # Pegando a escolha do usuário
            escolha = input("\033[34m \nEscolha uma cultura:")
            escolha = int(escolha)

            # Verificando se o input está correto
            if escolha > aux - 1 or escolha < 1 :

                raise ValueError("\033[31m \n!!!!--->  Escolha inválida  <---!!!!")

            run = False
            userInput.append(plants_data[escolha - 1]["name"])

        except ValueError :
            
            print("\033[31m \n!!!!--->  Escolha inválida  <---!!!!")
            time.sleep(2.5)
            continue
    
    run = True

    # Escolher se melhora o solo
    while run :

        try :

            # Limpando o console
            clearconsole.ClearConsole()

            # Menu
            print("\033[32m \n\n#######------->  Quer que melhore o solo?  <-------####### \n")
            #print("\033[31m -1 -> Sair")
            print("\033[34m Escolhas: \n")
            print("\033[33m 1 -> Sim")
            print("\033[33m 2 -> Não \n")

            # Pegando a escolha do usuário
            escolha = input("\033[34m \nEscolha uma : ")
            escolha = int(escolha)

            # Verificando se o input está correto
            if escolha > 2 or escolha < 1 :

                raise ValueError("\033[31m \n!!!!--->  Escolha inválida  <---!!!!")

            run = False
            userInput.append(True if escolha == 1 else False)

        except ValueError :
            
            print("\033[31m \n!!!!--->  Escolha inválida  <---!!!!")
            time.sleep(2.5)
            continue

    run = True

    # Escolhendo o ciclo
    while run :

        try :

            # Limpando o console
            clearconsole.ClearConsole()

            # Menu
            print("\033[32m \n\n#######------->  Qual o ciclo ?  <-------####### \n")
            #print("\033[31m -1 -> Sair")
            print("\033[34m Ciclos: \n")

            # Listando os ciclos
            aux = 1
            for x in cycles:
                print("\033[33m", aux, "->", x)
                aux += 1

            # Pegando a escolha do usuário
            escolha = input("\033[34m \nEscolha uma : ")
            escolha = int(escolha)

            # Verificando se o input está correto
            if escolha > 3 or escolha < 1 :

                raise ValueError("\033[31m \n!!!!--->  Escolha inválida  <---!!!!")

            run = False
            userInput.append(cycles[escolha - 1])

        except ValueError :
            
            print("\033[31m \n!!!!--->  Escolha inválida  <---!!!!")
            time.sleep(2.5)
            continue

    return userInput

# Função para ver se os Fitnesses estão estagnados
def Stagnated(bestsFitnesses) :

    if len(bestsFitnesses) >= 3 :

        fitness = list(bestsFitnesses)

        aux1 = fitness.pop()
        aux2 = fitness.pop()
        aux3 = fitness.pop()

        return (True if aux1 == aux3 else False) if aux1 == aux2 else False
    
    else :

        return False

def Main() :

    numberGenerations = 50
    populationSize = 10
    initialPopulation = []
    mutationRate = 0.1
    bestIndividual = [[], 0]
    bestsFitnesses = []

    userInput = Input()

    # Limpando o console
    clearconsole.ClearConsole()
    print("\033[34m \n\n#######------->  Processando....  <-------####### \n")
    print("\033[0m")

    for _ in range(0, populationSize) :

       initialPopulation.append(GenerateIndividual(userInput[0]))
       
    population = initialPopulation

    counter = 0
    while counter < numberGenerations and bestIndividual[1] < 16 : 

        fitnessIndividuals = []

        for aux1 in population :

           fitnessIndividuals.append(Fitness(aux1, userInput))

        selecteds = Selection(fitnessIndividuals)

        children = Crossover(selecteds)

        population = Mutation(children, mutationRate, initialPopulation)

        bestIndividual = max(fitnessIndividuals, key = lambda aux2 : aux2[1])
        bestsFitnesses.append(bestIndividual[1])

        counter += 1

    print("Escalada do fitness -->")
    print(bestsFitnesses)

    print("\n")
    print("Melhor indivíduo -->")
    print(bestIndividual)
    print("\n")

    print("\033[32m \n\n#######------->  Junto com o seu(a) \033[33m", userInput[0], "\033[32m plante:  <-------####### \n")

    for aux3 in bestIndividual[0] :

        print("\033[33m -->", aux3["name"])

    print("\n")

Main()

# Cromossomo:{planta1, planta2, planta3}
# planta1: {name, improves_soil, cycle, compatible_plants, incompatible_plants}  