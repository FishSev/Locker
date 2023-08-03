import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom"; 
import LockerComponent from "./LockerComponent";

const App = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" component={LockerComponent}/>
      </Switch>
    </BrowserRouter>
  );
};

export default App;