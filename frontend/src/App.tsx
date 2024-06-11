import { Link, Route, Routes } from 'react-router-dom';

import About from './pages/About';
import Hero from 'pages/Hero';
import Heroes from 'pages/Heroes';
import Home from './pages/Home';
import NoPage from 'pages/NoPage';

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
        <Route path='heroes' element={<Heroes />}>
          <Route path=':heroId' element={<Hero />} />
        </Route>
        <Route path='*' element={<NoPage />} />
      </Routes>
    </div>
  );
}

export default App;
