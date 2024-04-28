#include <stdio.h>

#define VOID '.'

int main(int argc, char *argv[]) {
	if (argc != 3) {
		printf("Использование: %s <текстовая карта> <временный файл>\n", argv[0]);
		return 1;
	}

	printf("\nЧтение файла \"%s\"\n", argv[1]);
	FILE *in_file = fopen(argv[1], "r");

	const int width = 32;
	char map[width * width];
	for (int i=0; i< width; ++i){
		for (int j=0; j< width; ++j){
			fscanf(in_file, "%c" ,&map[i * width + j]);
		}
		fscanf(in_file, "%*c"); // \n
	}
	
	printf("\nЗапись файла \"%s\"\n", argv[2]);
	FILE *out_file = fopen(argv[2], "w");
	fprintf(out_file, "v2.0 raw\n");
	
	for (int i=0; i< width; ++i){
		for (int j=0; j< width; ++j){
			if( map[i * width + j] == VOID )
				fprintf(out_file, "0");
			else
				fprintf(out_file, "1");
			
			if(j % 8 == 7)
				fprintf(out_file, " ");
		}
		fprintf(out_file, "\n");
	}
	return 0;
}

