import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginReactConfig from "eslint-plugin-react/configs/recommended.js";
import reactHooks from "eslint-plugin-react-hooks";
import jest from "eslint-plugin-jest";

export default [
  ...tseslint.configs.recommended,
  ...tseslint.configs.stylistic,
  pluginReactConfig,
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    plugins: {
      "react-hooks": reactHooks,
    },
    languageOptions: { globals: { ...globals.browser, ...globals.jest } },
    rules: { 
    ...pluginJs.configs.recommended.rules,
    "react/react-in-jsx-scope": "off",     
    "@typescript-eslint/no-unused-vars": "off" // duplicated from eslint reccomended rules
  },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
  {
    files: ["**/*.test.{js,jsx,ts,tsx}", "**/__tests__/**/*.{js,jsx,ts,tsx}"], // Apply to test files
    ...jest.configs["flat/recommended"],
    plugins: {
      jest,
    },
    rules: {
      "jest/no-disabled-tests": "warn",
      "jest/no-focused-tests": "error",
      "jest/no-identical-title": "error",
      "jest/prefer-to-have-length": "warn",
      "jest/valid-expect": "error",
    },
  },
];
