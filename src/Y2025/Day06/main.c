#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/_types/_ssize_t.h>

typedef struct {
    int **nums;
    bool *is_sum;
    int num_rows;
    int num_cols;
} *Problems;

void free_problems(Problems problems) {
    for (int row = 0; row < problems->num_rows; row++) {
        free(problems->nums[row]);
    }
    free(problems->nums);
    free(problems->is_sum);
    free(problems);
}

Problems p1_parser(char *filename) {
    Problems rtn = malloc(sizeof *rtn);

    FILE *file = fopen("input.txt", "r");
    if (!file) {
        printf("joever");
        exit(EXIT_FAILURE);
    }

    rtn->num_rows = 1;
    rtn->num_cols = 1;
    rtn->nums = malloc(sizeof(*rtn->nums));
    *rtn->nums = malloc(sizeof(**rtn->nums));

    char *line = NULL;
    size_t len = 0;
    ssize_t nread = getline(&line, &len, file);
    if (nread == -1) {
        printf("joever 2");
        exit(EXIT_FAILURE);
    }

    char *token = strtok(line, " ");
    int count = 0;
    while (token) {
        if (count == rtn->num_cols) {
            rtn->num_cols *= 2;
            *rtn->nums =
                realloc(*rtn->nums, rtn->num_cols * sizeof(**rtn->nums));
        }
        rtn->nums[0][count++] = atoi(token);
        token = strtok(NULL, " ");
    }
    rtn->num_cols = count;
    rtn->nums[0] = realloc(rtn->nums[0], rtn->num_cols * sizeof(**rtn->nums));

    rtn->is_sum = malloc(rtn->num_cols * sizeof(*rtn->is_sum));
    int row_count = 1;
    for (;; row_count++) {
        free(line);
        line = NULL;
        nread = getline(&line, &len, file);
        if (nread == -1) {
            printf("joever 3");
            exit(EXIT_FAILURE);
        }

        token = strtok(line, " ");
        count = 0;
        if (!strcmp(token, "*")) {
            while (*token == '*' || *token == '+') {
                rtn->is_sum[count++] = *token == '+';
                token = strtok(NULL, " ");
            }
            break;
        } else {
            if (row_count == rtn->num_rows) {
                rtn->num_rows *= 2;
                rtn->nums =
                    realloc(rtn->nums, rtn->num_rows * sizeof(*rtn->nums));
            }
            rtn->nums[row_count] = malloc(rtn->num_cols * sizeof(**rtn->nums));
            while (token) {
                rtn->nums[row_count][count++] = atoi(token);
                token = strtok(NULL, " ");
            }
        }
    }
    rtn->num_rows = row_count;
    rtn->nums = realloc(rtn->nums, row_count * sizeof(*rtn->nums));

    free(line);
    fclose(file);
    return rtn;
}

unsigned long p2_solve(char *filename, int num_rows, int num_cols) {
    FILE *file = fopen("input.txt", "r");
    if (!file) {
        printf("joever");
        exit(EXIT_FAILURE);
    }

    char **lines = calloc(num_rows, sizeof *lines);
    size_t len = 0;
    ssize_t nread;
    for (int i = 0; i < num_rows; i++) {
        nread = getline(&lines[i], &len, file);
        if (nread == -1) {
            printf("joever 2");
            exit(EXIT_FAILURE);
        }
    }

    char *line = NULL;
    nread = getline(&line, &len, file);
    if (nread == -1) {
        printf("joever 3");
        exit(EXIT_FAILURE);
    }

    int *widths = malloc(num_cols * sizeof(*widths));
    bool *is_sum = malloc(num_cols * sizeof(*is_sum));
    is_sum[0] = *line == '+';
    int count = 0;
    char *p = line + 1;
    char *prev = line;
    for (; *p != '\0'; p++) {
        if (*p == '+' || *p == '*') {
            widths[count++] = p - prev - 1;
            is_sum[count] = *p == '+';
            prev = p;
        }
    }
    widths[count] = p - prev - 1;
    free(line);

    char **ps = malloc(num_rows * sizeof *ps);
    char *buffer = malloc((num_rows + 1) * sizeof *buffer);
    buffer[num_rows] = '\0';

    for (int i = 0; i < num_rows; i++) {
        ps[i] = lines[i];
        buffer[i] = *ps[i];
    }

    unsigned long p2 = 0;
    for (int col = 0; col < num_cols; col++) {
        unsigned long res = is_sum[col] ? 0 : 1;
        for (int j = 0; j < widths[col]; j++) {
            int num = atoi(buffer);
            res = is_sum[col] ? res + num : res * num;
            for (int i = 0; i < num_rows; i++) {
                ps[i]++;
                buffer[i] = *ps[i];
            }
        }
        for (int i = 0; i < num_rows; i++) {
            ps[i]++;
            buffer[i] = *ps[i];
        }
        p2 += res;
    }

    free(ps);
    free(buffer);
    for (int i = 0; i < num_rows; i++) {
        free(lines[i]);
    }
    free(lines);
    return p2;
}

unsigned long solve(Problems problems) {
    unsigned long p1 = 0;
    for (int col = 0; col < problems->num_cols; col++) {
        unsigned long res;
        if (problems->is_sum[col]) {
            res = 0;
            for (int row = 0; row < problems->num_rows; row++) {
                res += problems->nums[row][col];
            }
        } else {
            res = 1;
            for (int row = 0; row < problems->num_rows; row++) {
                res *= problems->nums[row][col];
            }
        }
        p1 += res;
    }
    return p1;
}

int main(void) {
    Problems problems = p1_parser("input.txt");
    unsigned long p1 = solve(problems);
    unsigned long p2 =
        p2_solve("input.txt", problems->num_rows, problems->num_cols);
    printf("%lu %lu\n", p1, p2);

    free_problems(problems);
    return 0;
}
