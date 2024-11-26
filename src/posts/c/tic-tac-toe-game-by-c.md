---
title: 用 C 寫個 OOXX 小遊戲
date: '2024-11-26'
tags: [c]
description: 'tic tac toe game'
---

這次學習的資源是 YouTube 上的
<a target="_blank" rel="noopener noreferrer" href="https://youtu.be/87SH2Cn0s9A?si=sIiIBEo0geSrKr1s">C Programming Full Course for free</a>
與 <a target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/playlist?list=PLY_qIufNHc293YnIjVeEwNDuqGo8y2Emx">C 語言公開課</a>

第一個影片只有 4 個小時，搭配第二個影片的中文解說，加上實際動手寫程式總共花了一個禮拜的時間學習，相較於上一次學習 C# 需要一個月快了許多。

我在想是那些共通的概念讓自己在學習第三門語言加快了，也可能是這次是使用公司的 Windows 電腦學習所以少了很多奇怪的坑。

但是 C 最麻煩的地方就是指標的應用還有手動記憶體的配置，這個需要靠實作繼續往下延伸。

> 花一個禮拜熟悉 C 的語法還有重要的指標(pointer)概念後，就是自己寫一個最簡單的猜拳遊戲啦！相關教學影片可以看 C Programming Full Course for free 影片的最後一個部分。

```c
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>

// tic tac toe game

#define SIZE 3
static char board[SIZE][SIZE];
static const char PLAYER = 'X';
static const char COMPUTER = 'O';

void resetBoard();
void printBoard();
int checkFreeSpaces();
void playerMove();
void computerMove();
char checkWinner();
void printWinner(char);

int main()
{
    char winner = ' ';
    char response = ' ';

    do
    {
        winner = ' ';
        response = ' ';
        resetBoard();

        while (winner == ' ' && checkFreeSpaces() != 0)
        {
            printBoard();

            playerMove();
            winner = checkWinner();
            if (winner != ' ' || checkFreeSpaces() == 0)
            {
                break;
            }

            computerMove();
            winner = checkWinner();
            if (winner != ' ' || checkFreeSpaces() == 0)
            {
                break;
            }
        }

        printBoard();
        printWinner(winner);

        printf("\nWould you like to play again? (Y/N): ");
        scanf(" %c", &response);
        response = toupper(response);

    } while (response == 'Y');

    printf("Thanks for playing!");

    return 0;
}

void resetBoard()
{
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            board[i][j] = ' ';
        }
    }
}

void printBoard()
{
    printf(" %c | %c | %c", board[0][0], board[0][1], board[0][2]);
    printf("\n---|---|---\n");
    printf(" %c | %c | %c", board[1][0], board[1][1], board[1][2]);
    printf("\n---|---|---\n");
    printf(" %c | %c | %c\n", board[2][0], board[2][1], board[2][2]);
    printf("\n");
}

int checkFreeSpaces()
{
    int freeSpaces = 9;
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            if (board[i][j] != ' ')
            {
                freeSpaces--;
            }
        }
    }
    return freeSpaces;
}

void playerMove()
{
    int x;
    int y;

    do
    {
        printf("Enter row #(1-%d): ", SIZE);
        scanf("%d", &x);
        x--;
        printf("Enter column #(1-%d): ", SIZE);
        scanf("%d", &y);
        y--;

        if (board[x][y] != ' ')
        {
            printf("Invalid move!\n");
        }
        else
        {
            board[x][y] = PLAYER;
            break;
        }
    } while (board[x][y] != ' ');
}

void computerMove()
{
    // create a seed based on current time
    srand(time(NULL));
    int x;
    int y;

    if (checkFreeSpaces() > 0)
    {
        do
        {
            x = rand() % SIZE;
            y = rand() % SIZE;
        } while (board[x][y] != ' ');

        board[x][y] = COMPUTER;
    }
    else
    {
        printWinner(' ');
    }
}
char checkWinner()
{
    // check rows
    for (int i = 0; i < SIZE; i++)
    {
        if (board[i][0] == board[i][1] && board[i][0] == board[i][2])
        {
            return board[i][0];
        }
    }

    // check columns
    for (int i = 0; i < SIZE; i++)
    {
        if (board[0][i] == board[1][i] && board[0][i] == board[2][i])
        {
            return board[0][i];
        }
    }

    // check diagonals
    if (board[0][0] == board[1][1] && board[0][0] == board[2][2])
    {
        return board[0][0];
    }
    if (board[0][2] == board[1][1] && board[0][2] == board[2][0])
    {
        return board[0][2];
    }
    return ' ';
}

void printWinner(char winner)
{
    if (winner == PLAYER)
    {
        printf("Congratulations! You win!\n");
    }
    else if (winner == COMPUTER)
    {
        printf("The computer wins!\n");
    }
    else
    {
        printf("It's a tie!\n");
    }
}
```

> 在此做個學習紀錄。
> 記錄自己今年又學習了一門新的語言，實際了解另一個有趣的程式 :）
