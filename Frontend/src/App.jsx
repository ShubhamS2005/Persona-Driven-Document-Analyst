import React from "react";

import {BrowserRouter,Routes,Route,Navigate} from "react-router-dom";
import MainLayout from "./components/MainLayout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AskAssistant from "./pages/AskAssistant.jsx";
import History from "./pages/History.jsx";
import Documents from "./pages/Documents.jsx";
import Settings from "./pages/Settings.jsx";


function App() {
    return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={ <Navigate to="/dashboard"/> } />
          <Route path="/dashboard" element={ <Dashboard/> } />  
          <Route path="/ask" element={ <AskAssistant/> } /> 
          <Route path="/history" element={ <History/> } />  
          <Route path="/documents" element={ <Documents/> } /> 
          <Route path="/settings" element={ <Settings/> } />  
          
        </Routes>
      </MainLayout>
    </BrowserRouter> 
    );    
  }


export default App;