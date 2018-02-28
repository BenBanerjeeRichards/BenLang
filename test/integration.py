import subprocess


def compileBen(input_path: str, output_path: str):
    print(subprocess.check_output(["python3", "../benlang.py", input_path, output_path]))


def main():
    compileBen("integrationData/1.ben", "mips/1.s")


if __name__=="__main__":main()