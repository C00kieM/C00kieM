import os

BASE_DIRECTORY = "C:\\ZebraLabels\\"  

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def send_to_printer(content):
    print(f"Send an Zebra-Printer:\n{content}")

def main():
    user_input = input("FIle Name: ") 
    file_path = os.path.join(BASE_DIRECTORY, user_input)
    try:
        label_content = read_file(file_path)
        print("LabelContent:\n", label_content)
        send_to_printer(label_content)
    except FileNotFoundError:
        print("FileNotFound")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
