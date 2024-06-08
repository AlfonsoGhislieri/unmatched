import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginReactConfig from "eslint-plugin-react/configs/recommended.js";
import { fixupConfigRules } from "@eslint/compat";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  ...fixupConfigRules(pluginReactConfig),
  {
    plugins: {
      "react-hooks": reactHooks,
    },
    languageOptions: { globals: globals.browser },
    rules: {
      "react/react-in-jsx-scope": "off", // suppress errors for missing 'import React' in files
    },
  },
];
