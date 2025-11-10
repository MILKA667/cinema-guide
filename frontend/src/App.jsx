import './App.css'
import Login from './pages/Login';
import Home from './pages/Home';
import ProtectedRoute from './components/ProtectedRoute';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Header from './components/Header';
import Footer from './components/Footer';

function MainLayout({ children }) {
  return (
    <div>
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <MainLayout>
            <Home />
          </MainLayout>
        } />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App
