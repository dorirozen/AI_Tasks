from langchain.text_splitter import CharacterTextSplitter


def get_text_chunks(text):
    text_sp = CharacterTextSplitter(chunk_size=10, chunk_overlap=2, separator=" ", length_function=len)
    chunks = text_sp.split_text(text)
    return chunks


def main():
    raw_text = "asdsadas asde"
    text_chunks = get_text_chunks(raw_text)
    print(text_chunks)


if __name__ == "__main__":
    main()
