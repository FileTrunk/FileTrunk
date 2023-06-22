import "./App.css";
import { GoogleOAuthProvider } from '@react-oauth/google';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import React, { useState } from "react";
import Profile from "./components/Profile";
import Main from "./components/Main";
import Login from "./components/subcomponent/Login";
import getJWT from "./components/subcomponent/getJWT";
import ShareFile from "./components/subcomponent/ShareFile";

function App() {
  const [isAuthorized, setIfAuthorized] = useState(getJWT());
  return (
    <div className="App">
    <Router>
      <Switch>
        <Route path="/share/:token">
          <ShareFile />
        </Route>
        {isAuthorized ? (
          <div>
            <Route path="/files" exact>
              <Main />
            </Route>
            <Route path="/" exact>
              <Profile setIfAuthorized={setIfAuthorized} />
            </Route>
          </div>
        ) : (
          <Route path="/" exact>
            <GoogleOAuthProvider clientId={process.env.REACT_APP_HOST_CLIENT_ID}>
              <Login setIfAuthorized={setIfAuthorized} />
              </GoogleOAuthProvider>
          </Route>
        )}
      </Switch>
    </Router>
  </div>
  );
}
export default App;
