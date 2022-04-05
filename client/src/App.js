import './styles/App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Main from "./pages/Main";
import Archive from "./pages/Archive";
import NavBar from "./components/NavBar";
import {ToastContainer} from "react-toastify";
import RequestTask from "./pages/RequestTask";
import JournalPage from "./pages/JournalPage";


function App() {
  return (
    <BrowserRouter>
        <ToastContainer/>
      <div className={'App'}>
        <NavBar/>
        <Routes>
          <Route path="/" element={<Main/>}/>
          <Route path="/archive" element={<Archive/>}/>
          <Route path="/request_task" element={<RequestTask/>}/>
          <Route path="/journal" element={<JournalPage/>}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
