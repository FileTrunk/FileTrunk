import axios from "axios";
import getJWT from "../components/subcomponent/getJWT";

const api = {
  request: async (method, url, data, headers = {}) => {
    const jwt = getJWT();
    let authHeader = {};
    if (jwt) {
      authHeader = {
        Authorization: `Bearer : ${jwt}`,
      };
    }
    return await axios({
      url: url,
      method: method,
      baseURL: process.env.REACT_APP_API_HOST || window.location.origin,
      headers: {
        ...authHeader,
        ...headers,
      },
      data: data,
    }).then((response) => {
      if (response.data.message !== "Success") {
        alert(response.data.message);
        return;
      }
      if (method === "get") {
        return response.data;
      }
      return response;
    });
  },
};

export default api;
