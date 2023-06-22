import Cookies from "universal-cookie";
import api from "../../service/Api";
import { GoogleLogin } from '@react-oauth/google';

const Login = ({ setIfAuthorized }) => {
  const failureResponseGoogle = (response) => {
    console.log("Login failure from google side");
    console.log(response);
  };

  const successResponseGoogle = async (response) => {
    console.log(response)
    const res = await api.request(
      "post",
      `/api/v1/users/google-login/`,
      { googleTokenId: response.credential },
      { "Content-Type": "application/json" },
      true
    );
    const cookies = new Cookies();
    const date_of_expiration = new Date();
    date_of_expiration.setTime(
      date_of_expiration.getTime() + 14 * 24 * 60 * 60 * 1000
    );
    cookies.set("jwt", res.data.jwt, {
      path: "/",
      expires: date_of_expiration,
    });

    setIfAuthorized(true);
  };

  return (
    <div className="google-button-container d-flex justify-content-center align-items-center">
      <div className="height">
        <h1>To continue, you should</h1>
          <div className="center">
            <GoogleLogin
              onSuccess={successResponseGoogle}
              onError={failureResponseGoogle}
            />
          </div>
      </div>
    </div>
  );
};

export default Login;
