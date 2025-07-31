file_path = 'youtube_urls.txt'

try:
    with open(file_path, 'r') as file:
        for line in file:
            print(line.strip())
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")