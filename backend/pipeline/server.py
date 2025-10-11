from formatter import format_data
import time
def main():
    print("Server is running...\n")


    data = format_data()
    data = str(data)
    with open("output.md", "w", encoding="utf-8", errors="ignore") as txt_file:
        txt_file.write(data)#type:ignore
    
    print("\nServer Stopped After Completing Task")


if __name__ == "__main__":
    main()
