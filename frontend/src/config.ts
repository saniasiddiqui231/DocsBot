declare const process: {
  env: {
    REACT_APP_API_URL?: string;
  };
};

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "";

export default API_BASE_URL;