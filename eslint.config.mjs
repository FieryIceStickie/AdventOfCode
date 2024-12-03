import eslintConfigPrettier from 'eslint-config-prettier'

export default [
    {
        rules: {
            semi: ['error', 'never'],
            'prefer-const': 'error',
            quotes: ['error', 'single', { avoidEscape: true }],
            'max-len': [
                'error',
                {
                    code: 150,
                    ignoreStrings: true,
                    ignoreRegExpLiterals: true,
                    ignoreTemplateLiterals: true,
                    ignoreComments: true,
                },
            ],
        },
    },
    eslintConfigPrettier,
]
