#include<stdio.h>
#include<strings.h>
#include<math.h>
#include<stdlib.h>

int main(){
	//RC4
	//State Vector Implement 0-255
	int key[256];
	int keystream[256];
	int count=0;
	int S[256];
	for(count = 0;count < 0xff + 1;count++){
		S[count] = count;
	}
	//declarekey
	char *xorrer;
	xorrer = getenv("TMP");
	int lenxor = strlen(xorrer);
	int c=0;
	//T
	for(c=0; c<0xff+1; c++){
		key[c] = xorrer[c % lenxor];
		//printf("%c",key[c]);
	}
	
	//S-permutate
	int temp;
	int i=0,j=0; 
	for(i=0;i<0xff+1;i++){
		j = (j + S[i] + key[i]) % 256;
		//swap
		temp = S[i];
		S[i] = S[j];
		S[j] = temp;
	}
	
	//keystreamgen
	i = j = 0;

	int enctext[129] = {88,211,146,239,79,56,89,79,137,121,152,118,249,90,205,45,150,179,134,150,139,234,11,129,190,66,217,2,139,178,246,75,127,157,34,191,133,96,131,106,2,224,172,14,203,62,24,38,222,198,91,87,33,128,21,18,248,181,41,237,84,88,160,184,22,148,237,233,229,112,221,208,147,49,36,61,13,247,67,53,25,77,82,197,140,116,160,60,146,80,206,220,194,126,153,15,41,196,172,106,226,218,173,142,100,138,171,67,48,240,54,35,215,223,219,33,67,209,177,12,70,46,150,150,98,9,175,84};
	//FILE* strm = fopen("a8b4d3adbeef.cache","r");
	//FILE* strm = fopen("ev1lLOG.txt","r");
	//int plainlength = fread(&enctext,sizeof(char),128,strm);
	//for(int w=0;w<128;w++){
	//	printf("%c",enctext[w]);
	//}
	char plaintext[128];
	int tmp;
	
	for(size_t n=0; n < 128; n++){
		i = (i+1) % 256;
		j = (j + S[i]) % 256;
		tmp = S[i];
		S[i] = S[j];
		S[j] = tmp;
		
		int rndmize = S[(S[i] + S[j]) % 256];
		keystream[n] = S[rndmize];
	}
		

	int x=0;
	for(x=0;x<128;x++){
		//enctext[x] = keystream[x] ^ plaintext[x];
		plaintext[x] = keystream[x] ^ enctext[x];
		printf("%c", plaintext[x]);
	}
	//fclose(strm);
	
	
	
	
	
}
