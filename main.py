from reader import load
import pprint

    
def main() -> None:
    with open(r'E:\PythonProjects\ruby_marhal2python\Map076.rxdata', 'rb') as input, open('out.txt', 'w+') as output:
        pprint.pprint(load(input), output)
    


if __name__ == '__main__':
    main()
