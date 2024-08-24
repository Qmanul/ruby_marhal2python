from rpgmaker_parser.reader import load
import pprint


def main() -> None:
    with open(r'E:\PythonProjects\ruby_marhal2python\Map182.rxdata', 'rb') as input, open('newout.txt', 'w+', encoding="utf-8") as output: 
        data = load(input)
        pprint.pprint(data, output, )
    

if __name__ == '__main__':
    main()
