from dectree import ID3
import sys

tree = ID3()
tree_data, leaf_node, dec_node = tree.read_data('loan.dat')

ntree = tree.create_tree(tree_data, leaf_node, dec_node)

tree.printTree(ntree, ' ')


def exit_execution(message):
    print(message)
    sys.exit(1)


def start():
    risks = ['alto', 'moderado', 'baixo']
    historical = ['ruim', 'desconhecida', 'boa']
    debts = ['alta', 'baixa']
    guarantees = ['nenhuma', 'adequada']
    incoming = ['0-15 mil', '15-35 mil', 'acima de 35 mil']

    risk = input("Type the risk: ")
    historic = input("Type the historic: ")
    debt = input("Type the debt: ")
    guarantee = input("Type the guarantee: ")
    current_incoming = input("Type the incoming: ")

    if risk not in risks:
        exit_execution("Invalid risk!")

    if historic not in historical:
        exit_execution("Invalid historic!")

    if debt not in debts:
        exit_execution("Invalid debt!")

    if guarantee not in guarantees:
        exit_execution("Invalid guarantee!")

    if current_incoming not in incoming:
        exit_execution("Invalid incoming!")


start()
