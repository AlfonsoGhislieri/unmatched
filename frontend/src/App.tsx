import { Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import NoPage from 'pages/NoPage';
import Heroes from 'pages/Heroes';
import Hero from 'pages/Hero';

function App() {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to='/'>Home</Link>
          </li>
          <li>
            <Link to='/about'>About</Link>
          </li>
          <li>
            <Link to='/heroes'>Heroes</Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='about' element={<About />} />
        <Route path='heroes' element={<Heroes />} />
        <Route path='heroes/:heroId' element={<Hero />} />
        <Route path='*' element={<NoPage />} />
      </Routes>
    </div>
  );
}

export default App;
