# Nome completo do primeiro membro: João Pedro Perrucci Gabriel [Aluno que fez a entrega]
# RA do primeiro membro:            185204                      [Aluno que fez a entrega]
# Nome completo do segundo membro:  Bruno Fiorentino de Lima    [Segundo membro da equipe]
# RA do segundo membro:             260087                      [Segundo membro da equipe]

import random
from utils import load_words, ALL_COLORS, load_words
import math

WORDS = load_words() # Carrega a lista de palavras

guess_list = [i for i in WORDS if len(i) == 5]      # Cria uma lista só com as palavras que tem 5 letras (mais rapido que remover da original)

for i in range (len(guess_list)):           # Deixa todas as letras em maiusculo
    guess_list[i] = guess_list[i].upper()

initial_list = guess_list.copy()       

# Guarda o minimo e maximo de vezes que cada letra aparece na palavra chave
min_max = {'A':[0,5], 'B':[0,5], 'C':[0,5], 'D':[0,5], 'E':[0,5], 'F':[0,5], 'G':[0,5], 'H':[0,5], 'I':[0,5], 'J':[0,5], 'K':[0,5], 'L':[0,5], 'M':[0,5], 'N':[0,5], 'O':[0,5], 'P':[0,5], 'Q':[0,5], 'R':[0,5], 'S':[0,5], 'T':[0,5], 'U':[0,5], 'V':[0,5], 'W':[0,5], 'X':[0,5], 'Y':[0,5], 'Z':[0,5]}

in_position = {0:[], 1:[], 2:[], 3:[], 4:[]}         # Guarda letras que com certeza estão em seu respectivo indice (GREEN)
not_in_position = {0:[], 1:[], 2:[], 3:[], 4:[]}    # Guarda letras que com certeza não estão em seu respectivo indice (YELLOW)     

# Descobre a lingua
if 'LARGE' in guess_list:
    lang = 'en'
elif 'ACIER' in guess_list:
    lang = 'fr'
elif 'ADIPE' in guess_list:
    lang = 'it'
elif 'AARAO' in guess_list:
    lang = 'pt'
else:
    lang = 'sp'

def player(guess_hist, res_hist):
    #Função principal do jogador.
      
    global guess_list
    global lang
    global initial_list
    global in_position
    global not_in_position
    global min_max

    if len(guess_hist) > 0:

        # Pega apenas o resultado mais recente
        last_guess = guess_hist [-1]
        last_res = res_hist[-1]

        uptade_conditions(guess_list, last_guess, last_res, min_max, in_position, not_in_position)
        eliminate_words(guess_list, last_guess, last_res, min_max, in_position, not_in_position)

    groups = {}     # Guarda o numero de vezes que cada combinação de feedback pode aparecer
    word_score = []   # Guarda o valor de cada palpite e o palpite

    length_guess_list = len(guess_list)     # Armazena len(guess_list) para evitar repetição

    # O melhor chute inicial é sempre o mesmo, então já foi definido para acelerar o programa
    if 'SERAO' in guess_list and lang == 'pt':
        guess = 'SERAO'
    elif 'TEARS' in guess_list and lang == 'en':
        guess = 'TEARS'
    elif 'NORIA' in guess_list and lang == 'sp':
        guess = 'NORIA'
    elif 'LAINE' in guess_list and lang == 'fr':
        guess = 'LAINE'
    elif 'SERIO' in guess_list and lang == 'it':
        guess = 'SERIO'
    # Verifica qual o melhor chute, mesmo considerando palavras já descartadas (initial_list)
    elif length_guess_list>2:       # Se só podem ser duas palavras é 50/50, por isso não será verificado
        for possible_guess in initial_list:
            groups.clear()
            score = 0
            for possible_code in guess_list:    # Analisa todos os possiveis feedbacks do possible_guess
                fb = tuple(feedback (possible_guess, possible_code))
                if fb in groups:
                    groups[fb] += 1
                else:
                    groups[fb] = 1
            for i in groups:
                probability = groups[i]/length_guess_list
                score += ((probability/len(guess_list))*math.log(1/probability, 2)) # Formula para atribuir um valor para cada palavra com base em quantos feedbacks diferentes ela pode gerar
            word_score.append((score, possible_guess))  # Adiciona o possivel palpite e seu valor numa lista

        word_score.sort(reverse=True)
        guess = word_score[0][1]    # Pega a palavra com maior valor
    else:
        guess = guess_list[0]
    
    return guess 

def feedback(guess, code):
    
    colors_feedback = ["DARK_GRAY" for _ in range(5)]     # Inicializa a lista de feedback 
    code = list(code)                                     # Converte string para lista
    
    # Verifica acertos exatos (letra e posição corretas)
    for i, letter in enumerate(guess):
        if letter == code[i]:
            colors_feedback[i] = "GREEN"
            code[i] = None
    
    # Verifica acertos parciais (letra correta em posição errada)
    for i, letter in enumerate(guess):
        if letter in code and colors_feedback[i] != "GREEN":
            colors_feedback[i] = "YELLOW"
            code[code.index(letter)] = None
            
    # Define letras incorretas como "RED"
    for i, letter in enumerate(guess):
        if letter not in code and colors_feedback[i] not in ["GREEN", "YELLOW"]:
            colors_feedback[i] = "RED"
            
    return colors_feedback


# Elimina palavras com base no resultado anterior
def eliminate_words(guess_list, last_guess, last_res, min_max, in_position, not_in_position):

    # Elimina com base na posição das letras
    for word in range (len(guess_list)-1, -1, -1):
        for i in range (5):
            if guess_list[word][i] in not_in_position[i]:
                del guess_list[word]
                break
            if (len(in_position[i]) != 0) and (guess_list[word][i] not in in_position[i]):
                del guess_list[word]
                break

    # Elimina com base na quantidade de letras minimas e maximas que a palavra chave tem
    for word in range (len(guess_list)-1, -1, -1):
        for i in min_max:
            quantity = guess_list[word].count(i)
            if (quantity < min_max[i][0]) or (quantity > min_max[i][1]):
                del guess_list[word]
                break

# Atualiza as condições da palavra chave
def uptade_conditions(guess_list, last_guess, last_res, min_max, in_position, not_in_position):
    for i in last_guess:
        min_max[i][0] = 0       # Reseta o minimo da letra em zero, para depois contar quantas vezes essa letra apareceu nessa palavra (GREEN ou YELLOW)
    for i in range(5):
        if last_res[i] == 'GREEN' or last_res[i] == 'YELLOW':
            min_max[last_guess[i]][0] += 1 
        if (last_res[i] == 'YELLOW') and (last_guess[i] not in not_in_position[i]):
            not_in_position[i].append(last_guess[i])
        if (last_res[i] == 'GREEN') and (last_guess[i] not in in_position[i]):
            in_position[i].append(last_guess[i])
    for i in range(5):
        if last_res[i] == 'RED':
            min_max[last_guess[i]][1] = min_max[last_guess[i]][0]   # Significa que não tem mais essa letra na palavra, ou seja maximo = minimo