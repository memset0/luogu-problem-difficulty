/*

	二次修改: memset0 (https://memset0.cn)
	
	这个代码在网上流传的某个统计代码的基础上修改而来，
	主要是想资瓷更多功能，以及确保稳定性等等。
	略加了一些注释，若有疏漏请提 issue 指正。
	原作者姓名由于某些原因无法找到，如果有侵权请联系我署名 / 删除。 
	
	TODO:
	1. (DONE) 解决隐藏的题目无法被统计到 AC 数中的问题
	2. (DONE) 统计时展示当前题目难度 
	3. (    ) 统计时展示当前题目名称 
	4. ( ING) 保存结果到 TXT 文件中
	5. (    ) 解决洛谷因为过短时间的请求访问而屏蔽的问题
	6. (    ) 资瓷多个用户统计和比较 
	7. (    ) 资瓷多线程 

*/
#include <bits/stdc++.h>
#include <windows.h>
#include <conio.h>

int UserID = 122405; // 可以不填或设 0

#ifdef URLDownloadToFile // 避免 URLDownloadToFile 变量重复 
#undef URLDownloadToFile
#endif
using std::cout;
using std::endl;
using std::string;

typedef int (__stdcall *UDF) (LPVOID,LPCSTR,LPCSTR,DWORD,LPVOID);

UDF URLDownloadToFile = (UDF) GetProcAddress(LoadLibrary("urlmon.dll"), "URLDownloadToFileA");

char* strfind(char *text, char *temp) {
    int i = -1, j, l = strlen(temp);
    while (text[++i]) {
        for (j = 0; j < l; j++)
			if (text[i + j] == 0 || text[i + j] != temp[j])
				break;
        if (j == l)
			return text + i + l;
    }
    return 0;
}

void UTF8ToANSI(char *str) { // 将获取到的 UTF8 格式的网页源码转换为 ANSI 格式 
    int len = MultiByteToWideChar(CP_UTF8, 0, str, -1, 0, 0);
    WCHAR *wsz = new WCHAR[len+1];
    len = MultiByteToWideChar(CP_UTF8, 0,str,-1,wsz,len);
    wsz[len] = 0;
    len = WideCharToMultiByte(CP_ACP, 0, wsz, -1, 0, 0, 0, 0);
    len = WideCharToMultiByte(CP_ACP, 0, wsz, -1, str, len, 0, 0);
    str[len] = 0;
    delete []wsz;
}

HANDLE hOutput;
char name[32];
int count[9], sum;

int GetProblemDifficulty(char *file) { // 获得当前题目的难度 
	file = strfind(file, "\xE9\x9A\xBE\xE5\xBA\xA6");
	if (file == NULL) return 8;
	file = strfind(file, "lg-bg-");
	if (file[0] == 'r') return 0;
	if (file[0] == 'o') return 1;
	if (file[0] == 'y') return 2;
	if (file[0] == 'g' && file[2] == 'e') return 3;
	if (file[0] == 'b' && file[4] == 'l') return 4; 
	if (file[0] == 'p') return 5;
	if (file[0] == 'b' && file[4] == 'd') return 6;
	if (file[0] == 'g' && file[2] == 'a') return 7;
	return 8;
}

char DiffName[9][32] = {
	"入门难度",
	"普及-",
	"普及/提高-",
	"普及+/提高",
	"提高+/省选-",
	"省选/NOI-",
	"NOI/NOI+/CTSC",
	"尚无评定",
	"未知类型"
};
char DifficultySpace[9][32] = { "     ", "        ", "   ", "   ", "  ", "    ", "", "     ", "     " };

std::map < string, int > ProblemDifficulty;
std::map < int, std::vector < string > > ProblemCounter;

void Output(char *prob, int diff) { // 输出 
    COORD pos = {0,2};
	SetConsoleCursorPosition(hOutput, pos); 
    printf("%s 的统计: %s > %s           \n", name, prob, DiffName[diff]);
	for (int i = 0; i < 9; i++)
		printf("    %s:%s%6d\n", DiffName[i], DifficultySpace[i], count[i]);
}

void problem(char *&str) {
    int i = 0,len;
    DWORD unused;
    char prob[32],url[128],*file,*ptr;
    HANDLE hFile;
    
    str = strfind(str, "\">");
    while (*str != '<') prob[i++] = *str++;
	str = strfind(str, "]\n");
	
    prob[i] = 0;
    sprintf(url, "https://www.luogu.org/problemnew/show/%s", prob);
    URLDownloadToFile(0, url, "download.tmp", 0, 0);
    hFile = CreateFile("download.tmp", GENERIC_READ, FILE_SHARE_READ, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
    len = GetFileSize(hFile,0);
    file = ptr = new char[len+3];
    ReadFile(hFile, file, len, &unused,0);
    file[len] = file[len + 1] = 0;
    CloseHandle(hFile);
    
	int diff = GetProblemDifficulty(file);
	ProblemDifficulty[prob] = diff;
	ProblemCounter[diff].push_back(prob);
	count[diff]++, sum++;
	Output(prob, diff);
	
    delete []ptr;
}

void SaveResult() {
	std::ofstream fout;
	char tmp[10000];
	fout.open("result.txt", std::ios::out);
	
	fout << "============================\n"
			"    洛谷题目难度统计结果    \n"
			"============================\n\n"
			"# 用户信息\n\n"
			"  用户ID: " << UserID << "\n"
			"  用户名: " << name << "\n\n"
			"# 通过题目难度分布\n\n";
	for (int i = 0; i < 9; i++) {
		sprintf(tmp, "  %s:%s%6d\n", DiffName[i], DifficultySpace[i], count[i]);
		fout << tmp;
	}
	
	fout << "\n# 题目难度清单\n";
	for (std::map < int, std::vector < string > > ::iterator it = ProblemCounter.begin(); it != ProblemCounter.end(); it++) {
		sprintf(tmp, "%s", DiffName[it->first]);
		for (std::vector < string > ::iterator u = it->second.begin(); u != it->second.end(); u++)
			sprintf(tmp, "%s%c %s", tmp, u == it->second.begin() ? ':' : ',', u->c_str());
		for (int i = 0; true; i++) {
			if (!(i % 40) || tmp[i] == '\0') fout << "\n  ";
			if (tmp[i] == '\0') break;
			fout << tmp[i];
		}
	}
	fout << "\n  ┌──────────┬──────────────┐\n"
			"  | 题目编号 |   题目编号   |\n"
			"  ├──────────┼──────────────┤\n";
	for (std::map < string, int > ::iterator it = ProblemDifficulty.begin(); it != ProblemDifficulty.end(); it++) {
		sprintf(tmp, "  | %8s | %12s |\n", it->first.c_str(), DiffName[it->second]);
		fout << tmp;
	}
	fout << "  └──────────┴──────────────┘\n";
	
	fout.close();
	system("notepad result.txt");
}

int main() {
	
    int len, i = 0;
    DWORD unused;
    char url[128], user[16], *file, *ptr;
    HANDLE hFile;
    hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    
    if (!UserID) {
		printf("请输入洛谷UID: ");
    	scanf("%d", &UserID);
	} else {
		printf("请输入洛谷UID: %d\n", UserID);
	}
	
    sprintf(url, "https://www.luogu.org/space/show?uid=%d", UserID);
    URLDownloadToFile(0,url,"download.tmp",0,0);
    hFile = CreateFile("download.tmp",GENERIC_READ,FILE_SHARE_READ,0,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);
    len = GetFileSize(hFile,0);
    file = new char[len+3];
    ReadFile(hFile,file,len,&unused,0);
    file[len] = file[len+1] = 0;
    CloseHandle(hFile);
    UTF8ToANSI(file);
    
    sprintf(user, "U%d ", UserID);
    ptr = strfind(file, user);
    if (ptr != NULL) {	
        while (ptr[0] != '<' || ptr[1] != '/' || ptr[2] != 'h')
			name[i++] = *ptr++;
        printf("\n%s 的统计: ", name);
        ptr = strfind(file, "通过题目</h2>\n[<");
        if (ptr) {
            while (*ptr != '<') problem(ptr);
            printf("总共通过的题目数: %d\n", sum);
        } else {
			printf("未找到通过的题目\n");
		}
    } else {
		printf("用户不存在\n");
	}
	
    DeleteFile("download.tmp");
    delete []file;
    
	SaveResult();
	
    return 0;
}
