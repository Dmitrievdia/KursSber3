from func import (
     load_data_operations,
     sort_data_operations,
     show_info)


def main():
    data = load_data_operations()
    sorted_data = sort_data_operations(data)
    for data in sorted_data:
        print(show_info(data))


main()

# if __name__ == '__main__':
#     print(main())
