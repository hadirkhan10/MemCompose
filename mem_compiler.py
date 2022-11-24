
def create_config(mem_data):
    for key, value in mem_data.items():
        num_words = value[0]
        word_size = value[1]
        tech_name = 'scn4m_subm'
        print("Creating memory:", key, "of depth:", num_words, "and width:", word_size)
        with open(f"{key}.py", "w") as file:
            file.write(f"# this file is created by Marshal - Muhammad Hadir Khan\n"
                       f"# data word size \n"
                       f"word_size = {word_size}\n"
                       f"# num of words \n"
                       f"num_words = {num_words}\n"
                       f"# Technology to use in $OPENRAM_TECH \n"
                       f"tech_name = '{tech_name}' \n"
                       f"nominal_corner_only = True \n"
                       f"output_path = 'temp' \n"
                       f"output_name = 'sram_{word_size}_{num_words}_{tech_name}'"
                       )
