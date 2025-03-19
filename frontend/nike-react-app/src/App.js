import logo from './logo.svg';
import Homes from '../src/pages/Homes'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
          <Route index element={<Homes />}></Route>
          <Route path="/home" element={<Homes />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
