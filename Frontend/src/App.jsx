import React from "react";

import {BrowserRouter,Routes,Route,Navigate} from "react-router-dom";
import MainLayout from "./components/MainLayout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AskAssistant from "./pages/AskAssistant.jsx";


function App() {
    return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={ <Navigate to="/dashboard"/> } />
          <Route path="/dashboard" element={ <Dashboard/> } />  
          <Route path="/ask" element={ <AskAssistant/> } /> 
        </Routes>
      </MainLayout>
    </BrowserRouter> 
    );    
  }


export default App;